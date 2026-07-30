# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
"Dr. Greenthumb" — a small garden-mapping demo. Only one piece is actually runnable end-to-end:
- `server.py` — a **Streamlit** app (click a garden photo to "plant" crops). This is the app to run.
- `App.js` — a standalone React component that expects a FastAPI backend at `http://localhost:8000/scan-garden`. That backend is **not implemented** in this repo, and there is no `package.json`/bundler, so this path is not runnable as-is. The `fastapi`/`uvicorn`/`opencv-python-headless` entries in `requirements.txt` correspond to that missing backend.

### Running the Streamlit app
Streamlit installs to `~/.local/bin`, which is not on `PATH`. Run it via the module form:

```
python3 -m streamlit run server.py --server.port 8501 --server.headless true
```

Then open http://localhost:8501 (health check: `curl http://localhost:8501/_stcore/health` → `ok`).

### Gotchas
- The app requires an image named `garden.jpg` in the working directory (repo root). Without it the map shows a "Missing Photo" error and there's nothing to click. A sample `garden.jpg` is committed for this purpose; replace it with a real garden photo if desired.
- `server.py` contains **two concatenated Streamlit apps** (roughly lines 1–43 and 45–97). Streamlit executes the file top-to-bottom, so the second `st.set_page_config(...)`/layout wins and only one interactive map renders. This is expected given the current file; don't "fix" it unless asked.
- There are no automated tests and no lint config in this repo.
