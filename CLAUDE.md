# CLAUDE.md — AI Assistant Guide for WhiteRabbitNeo Llama 3 8B v2.0

This file provides context for AI coding assistants (Claude, Copilot, etc.) working in this repository.

---

## Project Overview

This is a **Hugging Face Spaces** application that hosts and showcases the **WhiteRabbitNeo Llama 3 8B v2.0** model.

The repository is currently in a **template/skeleton state**. The Streamlit UI scaffold and CI/CD pipelines exist, but the actual model integration in `app.py` is a placeholder that must be implemented.

---

## Repository Structure

```
WhiteRabbitNeo-Llama-3-WhiteRabbitNeo-8B-v2.0/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Full pipeline: CodeQL scan, lint, test, HF deploy
│       ├── lint.yml        # Standalone flake8 linting
│       ├── python-app.yml  # Matrix test across Python 3.9–3.12 and 3 OSes
│       └── security.yml    # Bandit security scan
├── .flake8                 # flake8 configuration (max-line-length=79)
├── .gitattributes          # Git LFS tracking for ML binary file types
├── .gitignore              # Excludes __pycache__, .pytest_cache, .env, etc.
├── README.md               # Hugging Face Space metadata + project documentation
├── app.py                  # Main Streamlit application (entry point)
├── requirements.txt        # Python dependencies (streamlit, bandit)
├── tests/
│   ├── __init__.py
│   └── test_app.py         # Smoke tests for process_input()
└── CLAUDE.md               # This file
```

### Files still missing that CI/CD expects

| File | Required by | Purpose |
|---|---|---|
| `mypy.ini` or `setup.cfg` | `python-app.yml` | mypy type checking config (currently uses `--ignore-missing-imports` flag) |

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

Runs on Ubuntu, Windows, macOS × Python 3.9, 3.10, 3.11, 3.12 (12 combinations).

Runs: flake8 → mypy → bandit → safety → pytest with coverage → Codecov upload.

### `lint.yml`

Standalone flake8 run.

### `security.yml`

Runs `bandit -r .` against the full repo. Installs from `requirements.txt` first (which includes `bandit`).

---

## Git and Branch Conventions

- **Primary branch**: `main` (all CI/CD targets `main`)
- **Feature branches**: `claude/<description>-<session-id>` pattern used for AI-assisted work
- **Git LFS**: All ML binary formats are tracked via LFS (see `.gitattributes`). Never commit model weights as regular git objects.

### LFS-tracked extensions

The authoritative list of Git LFS–tracked file patterns is defined in `.gitattributes`. Refer to that file for the exact patterns (for example, model weight files, archives, and training artifacts).

When adding any files that match those patterns, ensure `git lfs install` has been run in the repo.

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

- Target **Python 3.9+** compatibility (the matrix tests 3.9–3.12; 3.8 is EOL and streamlit >=1.29 requires >=3.9)
- Follow **PEP 8** — flake8 is enforced in CI with no custom exclusions configured yet
- Use **type annotations** where practical (mypy runs in CI via `python-app.yml`)

### Streamlit patterns

- All Streamlit calls must be at the **module top level** or inside callback functions; do not nest `st.*` calls inside loops that re-run unpredictably
- Define all helper functions **before** they are called (`process_input()` is correctly defined at the top of `app.py` before any `st.*` calls that reference it)
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
| HF deploy step has placeholder `<your_repo_id>` | `ci.yml:89` | High — replace with actual HF repo ID and set `HF_TOKEN` secret |
| PDF decoding fails on binary PDF bytes | `app.py` | High — use `PyPDF2` or `pdfminer` instead of `.decode("utf-8")` |
| Model inference not implemented | `app.py` | Core feature — replace `process_input()` stub with real model call |
| `safety check` may fail on new vulnerability disclosures | `python-app.yml` | Medium — pin or audit deps regularly |
| README placeholders not filled in | `README.md` | Low |
