#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from collections import Counter
from pathlib import Path
import argparse
import csv


def iter_tags(path: Path):
    """Read whitespace-separated POS tags from a file (one or many lines)."""
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            for tag in line.split():
                yield tag


def main():
    ap = argparse.ArgumentParser(
        description="Compute POS frequency and percentage per file for POS-only .txt files."
    )
    ap.add_argument("input", help="A directory OR a single .txt file")
    ap.add_argument("--glob", default="*.txt", help="When input is a directory, files to include (default: *.txt)")
    ap.add_argument("--out", default="pos_stats.csv", help="Output CSV path (default: pos_stats.csv)")
    ap.add_argument(
        "--exclude",
        default="SENT,SYM,:,$",
        help="Comma-separated POS tags to exclude from denominator for percentage (default: SENT,SYM,:,$)"
    )
    args = ap.parse_args()

    in_path = Path(args.input)
    exclude = [x.strip() for x in args.exclude.split(",") if x.strip()]
    exclude_set = set(exclude)

    if in_path.is_dir():
        files = sorted(in_path.glob(args.glob))
    else:
        files = [in_path]

    if not files:
        raise SystemExit(f"No files matched. input={in_path} glob={args.glob}")

    rows = []
    for fp in files:
        counts = Counter()
        fine_total = 0
        denom_total = 0
        excluded_total = 0

        for tag in iter_tags(fp):
            fine_total += 1
            counts[tag] += 1
            if tag in exclude_set:
                excluded_total += 1
            else:
                denom_total += 1

        for pos, cnt in counts.items():
            pct = (cnt / denom_total * 100.0) if denom_total else 0.0
            rows.append({
                "file": fp.stem,
                "coarse_pos": pos,
                "count": cnt,
                "percentage": f"{pct:.4f}",
                "denominator_total": denom_total,
                "excluded_total": excluded_total,
                "excluded_tags": ",".join(exclude),
                "fine_total_including_all": fine_total,
            })

    # sort: file, count desc, pos
    rows.sort(key=lambda r: (r["file"], -int(r["count"]), r["coarse_pos"]))

    out_path = Path(args.out)
    fieldnames = [
        "file",
        "coarse_pos",
        "count",
        "percentage",
        "denominator_total",
        "excluded_total",
        "excluded_tags",
        "fine_total_including_all",
    ]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print("Wrote:", out_path.resolve())
    print("Files processed:", len(files))


if __name__ == "__main__":
    main()