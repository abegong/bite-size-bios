# Bite-Size Bios

Bite-Size Bios is a Hugo site plus a research workspace for drafting short narrative biographies.

The repository is organized around two main project directories:

- `site/` contains the public Hugo website.
- `research/` contains source notes, drafts, and reusable writing skills.

Root-level files such as `Makefile`, `netlify.toml`, and `.gitmodules` are repository and deployment plumbing.

## Directory Structure

```text
.
├── Makefile
├── README.md
├── netlify.toml
├── research/
│   ├── biographies/
│   │   └── <initial>/<slug>/
│   │       ├── biography.md
│   │       └── research-links.md
│   └── skills/
│       ├── research-bio.md
│       └── write-bio.md
└── site/
    ├── archetypes/
    ├── content/
    │   └── biographies/<slug>/index.md
    ├── hugo.toml
    ├── layouts/
    ├── package.json
    ├── static/
    └── themes/Blonde/
```

## Research Workflow

1. Create a folder at `research/biographies/<initial>/<slug>/`.
2. Use `research/skills/research-bio.md` to add `research-links.md` with credible primary, institutional, academic, or otherwise reliable sources.
3. Draft the working biography in `biography.md`.
4. Use `research/skills/write-bio.md` as the reusable drafting guide.
5. Publish by adapting the draft into `site/content/biographies/<slug>/index.md`.

Keep research notes in `research/` unless they are intentionally prepared for publication.

## Site Development

Initialize the theme submodule after cloning:

```sh
git submodule update --init --recursive
```

Install the site dependencies:

```sh
cd site
npm ci
```

Run the site locally from the repository root:

```sh
make dev
```

Use a different port if `1313` is already busy:

```sh
make dev PORT=1314
```

Build the production site:

```sh
make build
```

Clean generated Hugo output:

```sh
make clean
```

Generated site output is written under `site/public/` and ignored by Git.

## Content Validation

This repository uses Katalyst to validate the biography content model:

- `site/content/biographies/` is checked as published Hugo content.
- `research/biographies/` is checked as source research content.

Run validation from the repository root:

```sh
katalyst check
```

Research files include a small front matter marker so Katalyst can distinguish
draft biographies from source-link notes:

```yaml
---
kind: biography
---
```

or:

```yaml
---
kind: research-links
---
```

## Deployment

The site deploys with Netlify. The root `netlify.toml` sets `site/` as the build base, installs from `site/package-lock.json`, and publishes `site/public/`.

Netlify build settings:

- Base directory: `site`
- Build command: `hugo --gc --minify --cleanDestinationDir`
- Publish directory: `public`
- Hugo version: `0.163.3`

Production builds use Hugo's `baseURL`, which is set to `https://bite-size-bios.com/`. Branch deploys and PR previews override `baseURL` with Netlify's `DEPLOY_PRIME_URL`, so preview links still point at their own deployed URL.

## Current Content

Published biographies:

- Elizabeth Báthory
- John Brown
- Mahatma Gandhi

Research folders mirror the published slugs under `research/biographies/`.

## Future Work

- Decide whether podcast versions should use a single narrator or a multi-voice format.
- Choose and document the audio generation pipeline.
- Add audio output paths once podcast files are produced.
