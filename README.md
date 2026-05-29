# Treasure Hunt (1D) — Mesocosm environment

Toy Mesocosm environment for SWECCathon: a 1D “treasure hunt” game where the agent replies `left`/`right`/`stay`.

## Setup

```bash
/opt/homebrew/bin/python3.11 -m venv .venv
./.venv/bin/pip install -U pip
./.venv/bin/pip install swecc-mesocosm
./.venv/bin/mesocosm --version
```

## Authoring loop (local)

1. Start Ollama (if not already running).
2. Pull a model (example):

```bash
ollama pull llama3.2
```

3. Terminal A — start your environment adapter:

```bash
./.venv/bin/python adapter.py
```

4. Terminal B — run local episodes:

```bash
./.venv/bin/mesocosm run local
```

## Next steps

- Edit `env.py` (your environment logic).
- Edit `benchanything.json` (manifest / domain config). Domain id is `treasure-hunt-1d`.
- Validate your manifest locally:
  - `./.venv/bin/mesocosm validate benchanything.json`
- When ready to submit, push this repo to GitHub and run:
  - `./.venv/bin/mesocosm env submit --name "…" --github-url https://github.com/...`
