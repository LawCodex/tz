# Tanzania (TZ) — legislation as Markdown

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as plain Markdown in git.

Legislation of the United Republic of Tanzania, in **English** and **Kiswahili** (the language of each Act as
published), from the **Parliament of Tanzania** (Bunge):

* the **Acts of Parliament** published on parliament.go.tz ("Sheria"), 1961–2026, as enacted (Act Supplements to
  the Gazette), including the **revised editions** (principal legislation, e.g. `Chapter 20 – The Criminal
  Procedure Act`, Revised Edition 2022) that the Parliament also publishes;
* the **Constitution of the United Republic of Tanzania, 1977** (*Katiba ya Jamhuri ya Muungano wa Tanzania ya
  Mwaka 1977*), Kiswahili text as published by the Parliament.

Retrieved 2026-10-13.

<!-- COUNTS -->
| Directory | Files |
|---|---|
| `acts/` | 1163 |
| `constitution/` | 1 |
| **Total** | **1164** |
<!-- /COUNTS -->

## Structure

```
acts/<year>/<slug>.md        year = year of the Act (Parliament's listing / title)
constitution/katiba-1977.md  Constitution (Kiswahili)
```

File names are slugs of the Act titles (English title, or Kiswahili title for Acts published in Kiswahili —
recent Acts are increasingly enacted in Kiswahili; 27 files are in Kiswahili). Front matter: `language` is `en` or `sw` (detected from the text),
`identifier` is the Act number (`Act No. N of YYYY`), `note` says whether the text is a revised edition or the Act
as enacted, and flags OCR. Divisions (`PART`/`SEHEMU`) and sections (`Section N` / `Kifungu N`) become headings;
the arrangement of sections is dropped.

## Text and OCR

Recent Acts have a text layer. Older Acts (1960s–2000s) are scanned PDFs: their text was produced by OCR
(tesseract 5, English model, 300 dpi) and is marked in `note`. OCR output was kept only when it passed a
plausibility check; it contains recognition errors.

## Sources

| Source | URL | Used for |
|---|---|---|
| Parliament of Tanzania — Acts | https://www.parliament.go.tz/acts (JSON: `https://polis.bunge.go.tz/api/acts/async`, files on polis.bunge.go.tz) | Acts |
| Parliament of Tanzania — Katiba | https://www.parliament.go.tz/documents/constitution-of-tanzania | Constitution |

`polis.bunge.go.tz` serves an incomplete TLS certificate chain; certificate verification was disabled for it.

## Not covered / known gaps

* The **Laws of Tanzania, Revised Edition** as a whole (Attorney General's Chambers / Office of the Solicitor
  General) could not be retrieved: the AGC website (agctz.go.tz) was unreachable. TanzLII (AfricanLII) was
  deliberately not used (its terms forbid bulk download). Only the revised chapters that Parliament publishes are
  included.
* No consolidation for Acts as enacted: amending Acts are separate files.
* Subsidiary legislation (*Sheria ndogo*) and Zanzibar legislation are not included.
* 9 Acts listed by Parliament could not be retrieved (no file attached in the listing, or download failures), e.g.
  the Customs Tariff Acts 1968/1976, the Civil Procedure Code Act 1966, the Petroleum Act 2015, the Railways Act
  2017 and Chapter 256 (Proceeds of Crime Act).

## Copyright

Tanzanian Acts are official public texts published by the Parliament. The Markdown conversion is provided as is,
for information; the authoritative texts are those published in the Gazette.

## Regenerate

```
python3 -m pip install -r scripts/requirements.txt   # plus poppler and tesseract
python3 scripts/tz_list.py --download   # list + PDFs into ../_raw/tz
python3 scripts/tz_ocr.py               # text extraction / OCR, cached next to the PDFs
python3 scripts/tz_convert.py
python3 scripts/tz_readme.py
```
