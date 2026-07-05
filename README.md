# Bite-Size Bios

A series of bite-size bios, each delivered as a readable web page and a podcast-style audio version.

## Output

- **Website:** One page per person, with a ~2500-word biography, links, and clean design.
- **Podcast:** Audio version in the style of NotebookLM — conversational, well-paced, optionally multi-voice.

## Directory Structure

```
.
├── README.md
├── hugo.toml               # Hugo site configuration
├── netlify.toml            # Netlify build and preview configuration
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
└── static/                 # Static files copied directly into the site
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
- Add Hugo front matter: title, lifespan, summary, tags, categories, and draft status
- Keep research notes in `bios/` unless they are intentionally prepared for publication
- Preview the page locally with `make dev`

### 4. Podcast Version
- Generate audio from the biography text
- Style: NotebookLM-like — conversational pacing, chapter breaks
- Optionally: multi-voice, intro/outro music
- Output: MP3 per person

## Website

This project uses [Hugo](https://gohugo.io/) for the static website.

Published pages live in `content/`. Source drafts, notes, and research links stay in `bios/`.

The site uses the `opera7133/Blonde` theme as a Git submodule in `themes/Blonde`.

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

Blonde uses Tailwind CSS through Hugo, so install Node dependencies before building:

```sh
npm install
```

### Deployment

The site deploys with [Netlify](https://www.netlify.com/).

Netlify reads `netlify.toml` from the repository root:

- **Build command:** `hugo --gc --minify --cleanDestinationDir`
- **Publish directory:** `public`
- **Hugo version:** `0.163.3`

Connect the GitHub repository in Netlify and set `main` as the production branch. Netlify will automatically build production deploys from `main` and Deploy Previews for pull requests. Preview URLs use Netlify's standard format:

```text
https://deploy-preview-<PR_NUMBER>--<SITE_NAME>.netlify.app
```

The Netlify build command overrides Hugo's `baseURL` with Netlify's `DEPLOY_PRIME_URL`, so production, branch deploys, and PR previews all generate links for their own deployed URL.

If the Netlify site name or production custom domain changes, update `baseURL` in `hugo.toml` to match the production URL used outside Netlify builds.

## Open Questions

- **Podcast voice:** Single narrator or multi-voice?
- **Audio generation:** Use `sag` (ElevenLabs TTS) or another pipeline?

## In Progress

- [ ] John Brown — `b/brown-john/`
