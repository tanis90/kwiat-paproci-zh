#!/usr/bin/env python3
"""Split the MinerU markdown into an Obsidian vault + translation jobs."""
import json, os, re

SRC = "raw/58-kwiat-paproci.md"
VAULT = "vault"
JOBS = "jobs"

PARTS = [
    ("00-版权与目录", 1, 176, "front"),
    ("10-最短夜", 177, 488, "scenario"),
    ("20-水上花环", 489, 821, "scenario"),
    ("30-蕨花AR", 822, 1152, "scenario"),
    ("40-作者", 1153, 1182, "meta"),
    ("90-后记", 1183, 1207, "meta"),
]

MAX_CHUNK = 4200  # source chars per translation job


def split_sections(lines):
    """Split a part into (heading, body) at ## headings.

    Headings with an empty body are legal (the source has several stacked
    label headings) and must be preserved, not silently dropped.
    """
    out, cur, buf = [], "(开头)", []
    for ln in lines:
        if re.match(r"^#{1,3} ", ln):
            out.append((cur, "\n".join(buf).strip()))
            cur, buf = re.sub(r"^#+\s*", "", ln).strip(), []
        else:
            buf.append(ln)
    out.append((cur, "\n".join(buf).strip()))
    return [(h, b) for h, b in out if h != "(开头)" or b]


def chunk_sections(secs):
    """Greedily group sections into chunks under MAX_CHUNK."""
    chunks, cur, size = [], [], 0
    for head, body in secs:
        blk = f"## {head}\n\n{body}\n"
        if cur and size + len(blk) > MAX_CHUNK:
            chunks.append(cur)
            cur, size = [], 0
        cur.append((head, blk))
        size += len(blk)
    if cur:
        chunks.append(cur)
    return chunks


def main():
    lines = open(SRC, encoding="utf-8").read().split("\n")
    os.makedirs(VAULT, exist_ok=True)
    os.makedirs(JOBS, exist_ok=True)
    index = []
    jobs = []

    for slug, a, b, kind in PARTS:
        body = lines[a - 1:b]
        text = "\n".join(body)
        # rewrite image refs to vault-relative
        text = text.replace("](images/", "](../raw/images/")
        note = os.path.join(VAULT, f"{slug}.md")
        secs = split_sections(body)
        toc = "\n".join(f"- {h}" for h, _ in secs if h != "(开头)")
        with open(note, "w", encoding="utf-8") as f:
            f.write(f"---\ntags: [原文, {kind}]\nsource: 58-kwiat-paproci.pdf\n"
                    f"pages: {a}-{b}\nstatus: 待译\n---\n\n")
            f.write(f"# {slug.split('-', 1)[1]}\n\n")
            f.write(f"> 原文页码 {a}–{b} · 共 {len(secs)} 节\n\n")
            if toc:
                f.write("## 本节结构\n" + toc + "\n\n---\n\n")
            f.write(text)
        index.append((slug, a, b, kind, len(text), len(secs)))

        if kind == "scenario":
            for i, grp in enumerate(chunk_sections(secs), 1):
                payload = "\n".join(blk for _, blk in grp)
                jid = f"{slug}__{i:02d}"
                jp = os.path.join(JOBS, jid + ".src.md")
                with open(jp, "w", encoding="utf-8") as f:
                    f.write(payload)
                jobs.append({"id": jid, "part": slug, "seq": i,
                             "sections": [h for h, _ in grp],
                             "chars": len(payload), "src": jp})

    json.dump(jobs, open(os.path.join(JOBS, "_jobs.json"), "w"),
              ensure_ascii=False, indent=1)
    print("notes:", len(index), "jobs:", len(jobs))
    for slug, a, b, kind, n, s in index:
        print(f"  {slug:14s} p{a}-{b}  {n:6d} chars  {s:2d} sections")
    print()
    for j in jobs:
        print(f"  {j['id']:22s} {j['chars']:5d} chars  {', '.join(j['sections'])[:60]}")


if __name__ == "__main__":
    main()
