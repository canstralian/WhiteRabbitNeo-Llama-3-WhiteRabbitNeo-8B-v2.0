# CLAUDE.md — AI Assistant Guide for WhiteRabbitNeo Llama 3 8B v2.0

This file provides context for AI coding assistants (Claude, Copilot, etc.) working in this repository.

---

## Project Overview

This is a **Hugging Face Spaces** application that hosts and showcases the **WhiteRabbitNeo Llama 3 WhiteRabbitNeo 8B v2.0** model. The frontend is built with **Streamlit** and deployed directly to Hugging Face Spaces via the platform's Git integration.

The repository is currently in a **template/skeleton state**. The Streamlit UI scaffold and CI/CD pipelines exist, but the actual model integration in `app.py` is a placeholder that must be implemented.

---

## Repository Structure

```
WhiteRabbitNeo-Llama-3-WhiteRabbitNeo-8B-v2.0/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Full pipeline: CodeQL scan, lint, test, HF deploy
│       ├── lint.yml        # Standalone flake8 linting
│       ├── python-app.yml  # Matrix test across Python 3.8–3.11 and 3 OSes
│       └── security.yml    # Bandit security scan
├── .gitattributes          # Git LFS tracking for ML binary file types
├── README.md               # Hugging Face Space metadata + project docs
├── app.py                  # Main Streamlit application (entry point)
└── CLAUDE.md               # This file
```

### Missing files that CI/CD expects

| File | Required by | Purpose |
|---|---|---|
| `requirements.txt` | `ci.yml`, `security.yml`, `python-app.yml` | Python dependency list |
| `tests/` | `ci.yml`, `python-app.yml` | pytest test suite |
| `.flake8` or `setup.cfg` | all lint workflows | flake8 configuration |
| `mypy.ini` or `setup.cfg` | `python-app.yml` | mypy type checking config |

---

## Application Entry Point: `app.py`

The Streamlit app (`app.py`) is the **only runtime file**. Hugging Face Spaces launches it automatically because `app_file: app.py` is declared in the README frontmatter.

### Current state (skeleton)

- Sidebar with title, instructions, and model metadata placeholders
- Text area + file uploader (`.txt`, `.pdf`) for user input
- Temperature slider (0.0–1.0, default 0.7) and max tokens input (10–1000, default 50)
- "Run Model" button with a `process_input()` stub that returns a formatted string
- **No actual model loading or inference is implemented**

### What needs to be implemented

1. Load the WhiteRabbitNeo model (likely via `transformers` or `llama-cpp-python`)
2. Replace the `process_input()` stub with real inference
3. Handle PDF file parsing (the uploader accepts PDFs but `getvalue().decode("utf-8")` will fail on binary PDF bytes — use `PyPDF2` or `pdfminer`)
4. Move `process_input()` definition **above** the `st.button` call (it is currently referenced before definition — a Python runtime bug)

---

## Hugging Face Spaces Configuration

The README.md frontmatter (lines 1–12) is parsed by Hugging Face to configure the Space:

```yaml
title: WhiteRabbitNeo Llama 3 WhiteRabbitNeo 8B V2.0
emoji: 🚀
colorFrom: pink
colorTo: gray
sdk: streamlit
sdk_version: 1.41.1
app_file: app.py
pinned: true
```

**Do not remove or reformat this YAML block.** It must remain at the very top of `README.md` between `---` delimiters.

---

## CI/CD Pipelines

All four workflows trigger on push/PR to `main`.

### `ci.yml` — Primary pipeline

| Job | Tool | Notes |
|---|---|---|
| `security_scan` | CodeQL (Python) | Static analysis via GitHub's CodeQL |
| `lint` | flake8 | Syntax errors and style |
| `test` | pytest | Requires `requirements.txt` and test files |
| `deploy` | huggingface-cli | Requires `HF_TOKEN` secret and correct `--repo-id` |

**Known issue**: The deploy step uses a placeholder `<your_repo_id>` — this must be replaced with the actual HF repo ID.

### `python-app.yml` — Cross-platform matrix

Runs on Ubuntu, Windows, macOS × Python 3.8, 3.9, 3.10, 3.11 (12 combinations).

Runs: flake8 → mypy → bandit → safety → pytest with coverage → Codecov upload.

**Known issue**: References `your_project` as the module path in `mypy` and `bandit` commands — replace with the actual module/directory name.

### `lint.yml`

Standalone flake8 run. Uses older `actions/checkout@v2` (consider upgrading to v4).

### `security.yml`

Runs `bandit -r .` against the full repo. Requires `requirements.txt` to install deps first.

---

## Git and Branch Conventions

- **Primary branch**: `main` (all CI/CD targets `main`)
- **Feature branches**: `claude/<description>-<session-id>` pattern used for AI-assisted work
- **Git LFS**: All ML binary formats are tracked via LFS (see `.gitattributes`). Never commit model weights as regular git objects.

### LFS-tracked extensions

`.7z .arrow .bin .bz2 .ckpt .ftz .gz .h5 .joblib .mlmodel .model .msgpack .npy .npz .onnx .ot .parquet .pb .pickle .pkl .pt .pth .rar .safetensors .tar .tflite .tgz .wasm .xz .zip .zst tfevents*`

When adding any of these files, ensure `git lfs install` has been run in the repo.

---

## Development Workflow

### Setup

```bash
# Clone the repo
git clone <repo-url>
cd WhiteRabbitNeo-Llama-3-WhiteRabbitNeo-8B-v2.0

# Install Git LFS (required for ML files)
git lfs install

# Install Python dependencies (once requirements.txt exists)
pip install -r requirements.txt
```

### Running locally

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

### Linting

```bash
pip install flake8
flake8 .
```

### Security scan

```bash
pip install bandit
bandit -r .
```

### Tests

```bash
pip install pytest pytest-cov
pytest --cov=.
```

---

## Key Conventions for AI Assistants

### Python style

- Target **Python 3.8+** compatibility (the matrix tests 3.8–3.11)
- Follow **PEP 8** — flake8 is enforced in CI with no custom exclusions configured yet
- Use **type annotations** where practical (mypy is planned)

### Streamlit patterns

- All Streamlit calls must be at the **module top level** or inside callback functions; do not nest `st.*` calls inside loops that re-run unpredictably
- Define all helper functions **before** they are called (the current `process_input()` placement on line 61 is a bug — it works due to Python's button callback timing, but is fragile)
- Use `st.cache_resource` (not the deprecated `st.cache`) for model loading to avoid reloading on every interaction

### Security

- **Never** hard-code API tokens, HF tokens, or model credentials in source files — use `st.secrets` (Streamlit's secrets management) or environment variables
- Bandit is run in CI; avoid patterns that trigger Bandit warnings (e.g., `subprocess.call` with `shell=True`, `pickle.load` on untrusted input)

### Model files

- Do **not** commit model weights to git directly — reference them from Hugging Face Hub and load at runtime
- If storing artifacts locally for development, add them to `.gitignore` (not `.gitattributes` LFS, which is for tracked LFS objects)

### README.md

- The frontmatter YAML block at the top is mandatory for Hugging Face Spaces — do not alter its structure
- Replace all `[bracketed placeholder]` sections with real content before considering the project production-ready

---

## Known Issues and TODOs

| Issue | Location | Priority |
|---|---|---|
| `process_input()` called before definition | `app.py:54` | High (runtime bug under some conditions) |
| PDF decoding fails on binary PDF bytes | `app.py:32` | High |
| `requirements.txt` does not exist | repo root | High (breaks CI) |
| No test files exist | repo root | High (breaks CI) |
| HF deploy step has placeholder `<your_repo_id>` | `ci.yml:89` | High |
| `your_project` placeholder in mypy/bandit commands | `python-app.yml:46,49,55` | Medium |
| Model inference not implemented | `app.py:61-67` | Core feature |
| Sidebar "About" section has placeholder text | `app.py:16-18` | Low |
| README placeholders not filled in | `README.md` | Low |
| Older `actions/checkout@v2` in lint/security workflows | `lint.yml`, `security.yml` | Low |
