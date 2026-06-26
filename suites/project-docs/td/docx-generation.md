# TD `.docx` Generation

Reference file for Phase 6 of the TD skill. Read this only when the user has
approved `.docx` generation. Do **not** generate a `.docx` before then.

The output is a submission-ready Word document with a centered cover page, a
dedicated Table of Contents page, justified body text, and a header/footer on
every non-cover page. The old AI-looking title block at the top of the document
is gone — the cover page replaces it.

---

## What the document looks like

**Cover page (section 1, no header/footer, not counted in page numbers):**
- Logo, centered, at the top (omitted if no logo is available).
- Title below it, Title Case, bold, large, centered.
- Authors below that, one per row in a borderless centered table, smaller font, body-text color.
- A subtitle "Technology Disclosure (TD)" below the authors, centered (italic, gray).
- The institute / organization name below the subtitle, centered.
- Date near the bottom, centered.

**Table of Contents (section 2, page 1):** on its own dedicated page.

**Body (section 2):** justified, with forced page breaks so the major
boundaries land cleanly:
- the **Abstract** starts on a fresh page (the TOC keeps its own page);
- the **main content** starts on a fresh page after the Abstract (page break
  before the section following the Abstract, i.e. the Introduction);
- the **References** section starts on a fresh page (page break before it), and
  its entries are **left-aligned** rather than justified. Everything else in the
  body stays justified.

**Every non-cover page:**
- Header: TD title top-left, logo top-right (scaled small), black border on the bottom edge only.
- Footer: page number centered (just the number, e.g. `3`), black border on the top edge only.

**Page numbering starts at the Table of Contents, not the cover.** The cover is
section 1; the TOC and body are section 2 with numbering restarted at 1, so the
TOC is page 1 and the cover is never counted.

---

## The generator

A tested script ships with this skill: `build_td_docx.py`, in the same directory
as `SKILL.md`. It runs `pandoc` to convert the markdown body (and build the Word
TOC field), then uses `python-docx` to add the cover, sections, header, footer,
justification, and page numbering. Do not hand-roll the OOXML — call the script.

Both `pandoc` and `python-docx` must be installed; Step 1 checks for them.

### Step 1 — Check prerequisites (and offer to install what's missing)

Probe both dependencies before doing anything else:

```bash
python3 -c "import docx" 2>/dev/null && echo "python-docx OK" || echo "python-docx MISSING"
pandoc --version >/dev/null 2>&1 && echo "pandoc OK" || echo "pandoc MISSING"
```

If both report OK, go to Step 2. Otherwise tell the user exactly what's missing
and offer to install it. **Ask before running any install command** (it needs
the user's approval, and on locked-down machines may not be permitted at all).
If the user declines or an install fails, stop here with a clear message — do
not run the build and let it crash with a traceback.

**`python-docx`** (a pip package). Try, in order, until one succeeds:

```bash
python3 -m pip install python-docx \
  || python3 -m pip install --user python-docx \
  || python3 -m pip install --break-system-packages python-docx
```

The fallbacks handle PEP 668 "externally-managed-environment" errors on modern
Debian/Ubuntu and Homebrew Python. If the project already uses a virtualenv,
install into that instead. On Windows, use `py -m pip install python-docx`.

**`pandoc`** (a standalone binary, *not* a pip package) — the command depends on
the OS, and some need elevated rights you may not have in the sandbox:

- macOS: `brew install pandoc`
- Debian/Ubuntu: `sudo apt-get install -y pandoc`
- Windows: `winget install --id JohnMacFarlane.Pandoc` or `choco install pandoc`

If you can't determine the OS, ask. After any install, re-run the probe above to
confirm before continuing.

### Step 2 — Gather cover metadata

Reuse the author list from pre-flight if it was captured there; otherwise ask
now. Confirm everything with the user before building:

- **Title** — the TD title (the script applies Title Case automatically).
- **Authors** — the full list, in order. Each becomes one row on the cover.
- **Institute / organization name** — printed on the cover under the
  "Technology Disclosure (TD)" subtitle. **You must ask the user for this.** If
  `../project_context.md` suggests a likely name (project owner, organization,
  affiliation), offer it as a suggestion — but the user has to confirm it or
  type the correct one. Do not silently fill it in from a guess.
- **Date** — defaults to today unless the user wants a specific submission date.

The subtitle line itself is fixed ("Technology Disclosure (TD)") and is not asked.

### Step 3 — Resolve the logo

Logos live in `docs/assets/logos/` at the project root (raster files: `.png`,
`.jpg`, `.jpeg`). This is a shared asset directory created at bootstrap, not a
file inside the skill — other skills can use the same logos.

1. List the image files there.
2. **Exactly one** → use it; tell the user which one.
3. **More than one** → ask the user which to use. Do not guess.
4. **None** → tell the user no logo was found in `docs/assets/logos/`, and ask whether to:
   (a) continue without a logo (cover and header simply omit it), or
   (b) pause so they can add a logo file to `docs/assets/logos/` first.
   Do not proceed until they answer.

### Step 4 — Build

Run the script (it ships next to `SKILL.md`). Quote the authors as a single
semicolon-separated string. Pass an empty `--logo ""` when continuing without one.

```bash
python3 <skill-dir>/build_td_docx.py \
  --md   "docs/td/<PROJECT>_TD_<slug>_<YYYY-MM-DD>.md" \
  --output "docs/td/<PROJECT>_TD_<slug>_<YYYY-MM-DD>.docx" \
  --title "<the TD title>" \
  --authors "First Author; Second Author; Third Author" \
  --institute "<institute name the user confirmed>" \
  --date  "<YYYY-MM-DD>" \
  --logo  "docs/assets/logos/<chosen>.png"
```

The script reads the markdown draft, drops everything before the first
**Abstract** heading (the title and author block belong on the cover, not the
body), and writes the styled `.docx` next to the draft.

> The body therefore begins at the `Abstract` heading. Keep `# Abstract` as the
> first real section in the draft. A title or author line above it is fine for
> reading the markdown standalone — the script excludes it from the body.

**Figures.** Write image paths in the draft relative to the draft's own location
(e.g. `![Figure 1](../assets/fig1.png)` for a file in `docs/assets/`). The script
runs `pandoc` from the draft's directory, so those paths resolve correctly no
matter what working directory you launch the script from — no need to `cd` first.
If a path is wrong, pandoc drops the image but still exits 0; the script catches
that and prints a loud `WARNING: pandoc could not fetch these images` listing
each one. If you see it, fix the path and rebuild. As a final check, confirm the
embedded image count (figures + 1 for the logo):

```bash
python3 -c "import zipfile,sys; print(len([n for n in zipfile.ZipFile(sys.argv[1]).namelist() if n.startswith('word/media/')]))" "docs/td/<file>.docx"
```

### Step 5 — Tell the user to update fields

The TOC and the page numbers are Word fields. They are marked dirty, so Word
updates them when the document opens (it may show an "update fields" prompt —
answer yes). If the TOC or page numbers look empty or stale, the user can force
a refresh: select all (`Ctrl/Cmd+A`) then press `F9`. Mention this in the
hand-off so they aren't mistaken for a bug.

---

## If you must adapt the generator

The script is intentionally small and commented. The pieces that are easy to get
wrong in OOXML, and that the script already handles correctly:

- **Two sections.** A `sectPr` carried in the last cover paragraph ends section 1
  (cover); the body's final `sectPr` is section 2. Section 1 has no header/footer
  references, so the cover is blank. Section 2 gets `pgNumType w:start="1"`.
- **Page number.** Footer uses a single `PAGE` field. With section 2's
  `pgNumType w:start="1"`, it reads 1 at the TOC and counts up; the cover is
  excluded because it is a separate section that is never numbered.
- **Borders.** Header bottom edge and footer top edge use a single-edge `w:pBdr`.
- **Logo at right in the header.** A right-aligned tab stop at the usable page
  width, then the image, keeps the title left and the logo hard-right.
- **Justification.** The `Normal`, `Body Text`, and `First Paragraph` styles are
  set to justified; heading styles keep their own alignment. References entries
  are then overridden to left-aligned.
- **Page breaks.** Forced before the Abstract (TOC keeps its page), before the
  section after the Abstract (main content), and before References.
- **Figure paths.** pandoc runs with the draft's directory as its working
  directory, so relative image links resolve regardless of caller CWD; unfetched
  images are surfaced as a loud warning instead of being dropped silently.

Verify any change by reopening the output with `python-docx` and checking:
`len(doc.sections) == 2`, section 0 has no header/footer reference, section 1 has
`pgNumType` start `1` plus header and footer references.
