# Extraction Schema

The structured-extraction contract shared by `/read-pdf` default mode and `/read-pdf --split` mode. Output is a single markdown file (`<basename>_text.md`) consisting of a bibliographic metadata block followed by 8-dimension research notes.

## Bibliographic metadata (always first)

From the title page (or title section of the converted markdown), extract:

```
## Bibliographic metadata
doi: <10.xxxx/yyyy if present on the title page, else null>
authors: [LastName1, LastName2, ...]
title: <verbatim title from title page>
year: <year>
venue: <journal/working paper series/etc., verbatim>
venue_type: journal | working_paper | book_chapter | other
```

If a field is not visible on the title page, record `null`. Do not guess.

## Research dimensions

1. **Research question** — What is the paper asking and why does it matter?
2. **Audience** — Which sub-community of researchers cares about this?
3. **Method** — How do they answer the question? What is the identification strategy?
4. **Data** — What data do they use? Where precisely did they find it? What is the unit of observation? Sample size? Time period?
5. **Statistical methods** — What econometric or statistical techniques do they use? What are the key specifications?
6. **Findings** — What are the main results? Key coefficient estimates and standard errors?
7. **Contributions** — What is learned from this exercise that we didn't know before?
8. **Replication feasibility** — Is the data publicly available? Is there a replication archive? A data appendix? URLs for the underlying data?

## Tone

A structured extraction more detailed and specific than a typical summary — what a researcher needs to **build on or replicate** the work. By the time the extraction is finished, the notes should contain specific data sources, variable names, equation references, sample sizes, coefficient estimates, and standard errors. Not a summary — a structured extraction.
