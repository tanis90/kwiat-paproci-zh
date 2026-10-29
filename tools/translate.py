#!/usr/bin/env python3
"""Dispatch translation jobs to open-design mimo, concurrency-limited."""
import json, os, re, sys, time, threading, queue, urllib.request

PROXY = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
BASE = "https://amr-link.open-design.ai/v1"
KEY = os.environ.get("OPEN_DESIGN_API_KEY", "")
if not KEY:
    raise SystemExit("set OPEN_DESIGN_API_KEY first")
MODEL = "mimo-v2.6-flash"
CONC = 4                      # user: ~5 max, more crashes
JOBDIR = "jobs"
OUTDIR = "out"
GLOSSARY = "glossary/译名对照表.md"

if PROXY:
    op = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
else:
    op = urllib.request.build_opener()

SYS = """你是资深 TRPG 模组译者，专精《克苏鲁的呼唤》(Call of Cthulhu)，母语中文。
本次任务：把波兰语跑团模组《Kwiat Paproci》（蕨花）译为简体中文。这是出版社 Black Monk 经 Chaosium 授权、免费公开发行的正版模组，仅供跑团桌上使用。

硬性要求：
1. 严格遵守随附的《译名对照表》，表内词条一字不改。
2. 保留 Markdown 结构：## 标题层级、项目符号、加粗、斜体、图片占位 `![](../raw/images/...)` 全部原样保留。
3. 规则数据保持数字不变，属性缩写按对照表换成中文（如 "S 30" → "力量 30"）。
4. 第二人称朗读段落用"你"，保持代入感；守秘人提示用"守秘人"。
5. 中文要像人写的中文，避免机翻腔：长句拆开、被动改主动、少用"的的的"。
6. 只输出译文，不要前言、不要说明、不要"以下是译文"。
"""


def load_glossary():
    t = open(GLOSSARY, encoding="utf-8").read()
    # keep the tables only, drop the meta prose
    return t


def call(prompt, timeout=300, tries=3):
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "system", "content": SYS},
                     {"role": "user", "content": prompt}],
        "max_tokens": 16000,
        "temperature": 0.25,
        "reasoning_effort": "low",
        "stream": False,
    }).encode()
    last = ""
    for i in range(tries):
        req = urllib.request.Request(f"{BASE}/chat/completions", data=body, headers={
            "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
        try:
            t0 = time.time()
            d = json.loads(op.open(req, timeout=timeout).read())
            el = time.time() - t0
            if "error" in d:
                last = str(d["error"])[:160]
                time.sleep(3 * (i + 1))
                continue
            ch = d["choices"][0]
            msg = ch["message"]
            txt = (msg.get("content") or "").strip()
            if not txt:
                last = f"empty content, finish={ch.get('finish_reason')}"
                time.sleep(3 * (i + 1))
                continue
            u = d.get("usage", {})
            return {"ok": True, "text": txt, "secs": el,
                    "in": u.get("prompt_tokens"), "out": u.get("completion_tokens"),
                    "reasoning": (u.get("completion_tokens_details") or {}).get("reasoning_tokens")}
        except Exception as e:
            last = f"{type(e).__name__}: {e}"[:160]
            time.sleep(3 * (i + 1))
    return {"ok": False, "err": last}


def main():
    jobs = json.load(open(os.path.join(JOBDIR, "_jobs.json"), encoding="utf-8"))
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    if only:
        jobs = [j for j in jobs if any(o in j["id"] for o in only)]
    os.makedirs(OUTDIR, exist_ok=True)

    gloss = load_glossary()
    q = queue.Queue()
    for j in jobs:
        if os.path.exists(os.path.join(OUTDIR, j["id"] + ".zh.md")) and \
           os.path.getsize(os.path.join(OUTDIR, j["id"] + ".zh.md")) > 200:
            continue
        q.put(j)

    results, lock = {}, threading.Lock()
    total = q.qsize()
    done = [0]

    def worker():
        while True:
            try:
                j = q.get_nowait()
            except queue.Empty:
                return
            src = open(j["src"], encoding="utf-8").read()
            prompt = (f"【译名对照表】\n{gloss}\n\n"
                      f"【待译原文】\n{src}")
            r = call(prompt)
            with lock:
                done[0] += 1
                tag = f"[{done[0]}/{total}] {j['id']}"
                if r["ok"]:
                    with open(os.path.join(OUTDIR, j["id"] + ".zh.md"), "w", encoding="utf-8") as f:
                        f.write(r["text"])
                    results[j["id"]] = {"ok": True, "secs": round(r["secs"], 1),
                                        "in": r["in"], "out": r["out"],
                                        "reasoning": r["reasoning"],
                                        "chars": len(r["text"])}
                    print(f"{tag} OK {r['secs']:.0f}s in={r['in']} out={r['out']} "
                          f"zh={len(r['text'])}字", flush=True)
                else:
                    results[j["id"]] = {"ok": False, "err": r["err"]}
                    print(f"{tag} FAIL {r['err']}", flush=True)
            q.task_done()

    ts = [threading.Thread(target=worker) for _ in range(min(CONC, max(1, total)))]
    for t in ts:
        t.start()
    for t in ts:
        t.join()

    p = os.path.join(OUTDIR, "_results.json")
    old = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    old.update(results)
    json.dump(old, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    ok = sum(1 for v in results.values() if v["ok"])
    print(f"\n=== done {ok}/{len(results)} ok")
    if ok:
        t = [v["secs"] for v in results.values() if v["ok"]]
        i = sum(v["in"] or 0 for v in results.values() if v["ok"])
        o = sum(v["out"] or 0 for v in results.values() if v["ok"])
        print(f"    total {sum(t):.0f}s, avg {sum(t)/len(t):.0f}s/job, tokens in={i} out={o}")


if __name__ == "__main__":
    main()
