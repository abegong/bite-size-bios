# 10-Minute Biographies

A series of ~10-minute biographies, each delivered as a readable web page and a podcast-style audio version.

## Output

- **Website:** One page per person, with a ~2500-word biography, links, and clean design.
- **Podcast:** Audio version in the style of NotebookLM — conversational, well-paced, optionally multi-voice.

## Directory Structure

```
projects/ongoing/10-minute-biographies/
├── README.md
├── <initial>/<slug>/
│   ├── research-links.md   # Curated credible sources
│   ├── notes.md            # Key facts, quotes, timeline
│   ├── biography.md        # ~2500-word draft
│   └── podcast-script.md   # Optional: tweaked narration script
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
- Convert `biography.md` to HTML (static site generator or hand-rolled)
- Add navigation, styling, links section
- Deploy to hosting (TBD: GitHub Pages, existing site, etc.)

### 4. Podcast Version
- Generate audio from the biography text
- Style: NotebookLM-like — conversational pacing, chapter breaks
- Optionally: multi-voice, intro/outro music
- Output: MP3 per person

## Open Questions

- **Static site generator:** Jekyll, 11ty, or plain HTML?
- **Hosting:** GitHub Pages, existing personal site, or dedicated domain?
- **Podcast voice:** Single narrator or multi-voice?
- **Audio generation:** Use `sag` (ElevenLabs TTS) or another pipeline?

## In Progress

- [ ] John Brown — `b/brown-john/`
