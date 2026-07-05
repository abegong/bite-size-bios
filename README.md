# 10-Minute Biographies

A series of ~10-minute biographies, each delivered as a readable web page and a podcast-style audio version.

## Output

- **Website:** One page per person, with a ~2500-word biography, links, and clean design.
- **Podcast:** Audio version in the style of NotebookLM — conversational, well-paced, optionally multi-voice.

## Directory Structure

```
.
├── README.md
├── hugo.toml               # Hugo site configuration
├── content/                # Public website content
│   └── biographies/
│       └── <slug>/
│           └── index.md    # Published biography page
├── bios/                   # Source archive, drafts, and research notes
│   └── <initial>/<slug>/
│       ├── research-links.md
│       ├── notes.md
│       ├── biography.md
│       └── podcast-script.md
├── assets/                 # Theme/site assets
├── static/                 # Static files copied directly into the site
└── .github/workflows/      # GitHub Pages deployment
```

## Process

### 1. Research & Notes
- Create a directory: `<initial>/<slug>/`
- Add `research-links.md` with credible sources (PBS, NPS, academic, primary docs)
- Read sources and compile `notes.md` — key facts, quotes, timeline, themes

### 2. Draft Biography
- Write `biography.md` (~2500 words) from the notes
- Iterate in the vault; editable in Obsidian
- Aim for narrative flow: hook, arc, legacy

### 3. Website Page
- Copy or adapt `bios/<initial>/<slug>/biography.md` into `content/biographies/<slug>/index.md`
- Add Hugo front matter: title, lifespan, summary, tags, topics, and draft status
- Keep research notes in `bios/` unless they are intentionally prepared for publication
- Pick and configure a Hugo theme before expecting rendered HTML pages

### 4. Podcast Version
- Generate audio from the biography text
- Style: NotebookLM-like — conversational pacing, chapter breaks
- Optionally: multi-voice, intro/outro music
- Output: MP3 per person

## Website

This project uses [Hugo](https://gohugo.io/) for the static website.

Published pages live in `content/`. Source drafts, notes, and research links stay in `bios/`.

The site uses the `diwao/hestia-pure` theme as a Git submodule in `themes/hestia-pure`.

### Local Development

```sh
make dev
```

If port `1313` is already in use, choose another fixed port:

```sh
make dev PORT=1314
```

Build the production site:

```sh
make build
```

The generated site is written to `public/`, which is ignored by Git.

Remove generated files:

```sh
make clean
```

### Theme

The theme is tracked as a Git submodule. After cloning the repository, initialize it with:

```sh
git submodule update --init --recursive
```

### Deployment

The site deploys to GitHub Pages with `.github/workflows/hugo.yml` when changes are pushed to `main`.

## Open Questions

- **Podcast voice:** Single narrator or multi-voice?
- **Audio generation:** Use `sag` (ElevenLabs TTS) or another pipeline?

## In Progress

- [ ] John Brown — `b/brown-john/`
