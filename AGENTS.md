# Agent Guidance

Notes for AI agents (and humans) working in this repository.

## Toolchain: Node, not Python

Repository scripts are written in Node.js as plain ESM JavaScript (`.mjs`) —
no TypeScript, no build step. The site toolchain is already Node/npm, so Node
is the one runtime every contributor has set up, and modern Node ships
`fetch`, `FormData`, and `Blob` natively, which covers the OpenAI API calls
these scripts make.

Do not introduce Python (or another runtime) for new scripts.

- The employee-card pipeline lives at `cards/generate-card-art.mjs`. It was
  originally written in Python and ported to Node for the reasons above.
- Exception: `research/scripts/create_bio_image.py` predates this rule and
  stays in Python until someone ports it. Do not add new Python alongside it.

Keep scripts dependency-light. Small, focused packages (for example
`smol-toml` for TOML parsing in `cards/`) are fine; frameworks and build
tooling are not.
