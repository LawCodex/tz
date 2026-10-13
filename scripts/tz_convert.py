#!/usr/bin/env python3
"""Tanzania: convert the downloaded Parliament Acts (../../_raw/tz/pdf, see tz_list.py) and the
Constitution to Markdown."""
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tz_text as T  # noqa
from tz_list import url_of  # noqa

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(os.path.dirname(REPO), "_raw", "tz")
RETRIEVED = os.environ.get("LC_RETRIEVED", "2026-10-13")
SW = {"na", "ya", "wa", "kwa", "hii", "katika", "au", "la", "cha", "za", "kama", "ambayo", "sheria"}
EN = {"the", "of", "and", "shall", "to", "in", "or", "be", "any", "by", "this", "act"}
STARTS = (r"^(I ASSENT|NAKUBALI)\b", r"^ENACTED\b", r"^IMETUNGWA\b", r"^AN ACT\b", r"^An Act\b")
OCR = "--ocr" in sys.argv


def lang_of(text):
    w = Counter(re.findall(r"[a-z]+", text.lower()))
    sw = sum(w[x] for x in SW)
    en = sum(w[x] for x in EN)
    return "sw" if sw > en else "en"


def year_of(a):
    for s in (a.get("posted") or "", a.get("title_en") or "", a.get("title_sw") or ""):
        m = re.search(r"\b(19[6-9]\d|20[0-2]\d)\b", s)
        if m:
            return m.group(1)
    return None


def clean_title(t):
    t = re.sub(r"\s+", " ", (t or "")).strip().rstrip(".")
    t = re.sub(r"\s*\((Toleo la Kiingereza|Toleo la Kiswahili)\)", "", t)
    t = re.sub(r"\s+,", ",", t)
    if t.isupper():
        small = {"and", "of", "the", "for", "to", "in", "on", "a", "an", "by", "with", "or", "ya", "wa", "na", "la", "za", "kwa"}
        t = " ".join(w if (i and w.lower() in small and w.lower() == w.lower()) and False else w for i, w in enumerate(t.split()))
        t = " ".join((w.lower() if (i and w.lower().strip("(),") in small) else w.capitalize()) for i, w in enumerate(t.split()))
    return t


def main():
    acts = json.load(open(os.path.join(RAW, "acts.json")))["data"]
    n = skipped = 0
    seen = set()
    report = []
    for a in acts:
        pdf = os.path.join(RAW, "pdf", "%s.pdf" % a["id"])
        if not os.path.exists(pdf) or not T.pdf_ok(pdf):
            report.append(("missing", a["id"], a["title_en"]))
            continue
        pages, ocr = T.pdf_text(pdf, "eng", tmpdir=RAW, ocr=OCR)
        txt = "\n".join(pages)
        good = [p for p in pages if len(p.strip()) > 150]
        if len(good) < max(1, len(pages) * 0.5) or T.text_quality(txt) < 0.75:
            report.append(("no-text", a["id"], a["title_en"]))
            skipped += 1
            continue
        lang = lang_of(txt)
        title = clean_title(a["title_en"] if lang == "en" or not a.get("title_sw") else a["title_sw"])
        if lang == "en" and re.match(r"^Sheria\b", title) and a.get("title_sw"):
            title = clean_title(a["title_sw"])
        year = year_of(a)
        num = re.sub(r"^(No\.?|Na\.?)\s*", "", (a.get("act_no") or "").strip(), flags=re.I) or None
        lines = T.clean_pages(pages)
        body = T.structure(T.drop_toc(lines, starts=STARTS), "en", art_word="Kifungu" if lang == "sw" else "Section")
        rev = re.search(r"REVISED EDITION,? ?((19|20)\d\d)", " ".join(pages[:3]).upper())
        title = re.sub(r"^(Chapter \d+\w*)\s*[-–]\s*", r"\1 – ", title)
        meta = {"title": title, "identifier": ("Act No. %s of %s" % (num, year)) if num and year else None,
                "type": "act", "jurisdiction": "tz", "language": lang, "year": int(year) if year else None,
                "status": "unknown", "source": url_of(a), "retrieved": RETRIEVED,
                "note": ("Revised edition %s (principal legislation as revised by the Attorney General)." % rev.group(1) if rev else "As enacted (Act Supplement to the Gazette); not consolidated.") + (" Text obtained by OCR (scanned PDF); may contain recognition errors." if ocr else "")}
        d = os.path.join(REPO, "acts", year or "undated")
        base = T.slug(title)
        if (year, base) in seen:
            base = base + "-" + a["id"]
        seen.add((year, base))
        T.write_md(os.path.join(d, base + ".md"), meta, title, body)
        n += 1
    json.dump(report, open(os.path.join(RAW, "convert_report.json"), "w"), indent=1)
    print("written", n, "skipped(no text)", skipped, "missing", sum(1 for r in report if r[0] == "missing"))


if __name__ == "__main__":
    main()
