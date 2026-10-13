#!/usr/bin/env python3
"""Tanzania: list the Acts published by the Parliament of Tanzania (Bunge, POLIS JSON feed used by
https://www.parliament.go.tz/acts) and download the PDFs to ../../_raw/tz/pdf."""
import json
import os
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tz_text as T  # noqa

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(os.path.dirname(REPO), "_raw", "tz")
FEED = "https://polis.bunge.go.tz/api/acts/async"
# polis.bunge.go.tz serves an incomplete certificate chain: TLS verification is disabled for it.
import urllib3  # noqa
urllib3.disable_warnings()


def url_of(a):
    return "https://polis.bunge.go.tz" + urllib.parse.quote(a["file_url"], safe="/()[],")


def main():
    p = os.path.join(RAW, "acts.json")
    if "--no-list" not in sys.argv or not os.path.exists(p):
        T.fetch(FEED, p + ".new", delay=1, verify=False)
        os.replace(p + ".new", p)
    acts = json.load(open(p))["data"]
    print(len(acts), "acts")
    if "--download" in sys.argv:
        for a in acts:
            r = T.fetch(url_of(a), os.path.join(RAW, "pdf", "%s.pdf" % a["id"]), delay=1.5, check_pdf=True, tries=3, verify=False)
            print("ok" if r else "FAIL", a["id"], a["title_en"], flush=True)


if __name__ == "__main__":
    main()
