# MLOps on Hugging Face — Central Lab Repo

This folder is the single, central place for every Hugging Face–related
activity in the MLOps course: fine-tuning notebooks, the two Gradio Spaces
(vision + NLP), the text-generation/summarization microservice, and the
shared local-dev setup (dependencies, credentials, commands) they all use.

> Related reading: the course's HTML site has a companion reference sheet,
> [`Ecosysteme_HuggingFace.md`](../../../Day1-Intro-HuggingFace/Ecosysteme_HuggingFace.md)
> (Hub, Models, Datasets, Spaces, versioning, authentication) — read that
> first if the vocabulary below is unfamiliar.

## Contents

| Path | What it is |
|---|---|
| `Get_Started.ipynb` | Workshop notebook — sentiment analysis walkthrough (Hub login, `pipeline`, dataset loading, tokenizing, fine-tuning DistilBERT-style, `push_to_hub`). |
| `train_vit_beans_colab.ipynb` | Fine-tunes a Vision Transformer (ViT) on the `beans` dataset (Colab, GPU). |
| `train_distilbert_sentiment_colab.ipynb` | Fine-tunes DistilBERT on `rotten_tomatoes` for sentiment analysis (Colab, GPU). |
| `model_versioning_colab.ipynb` | Trains several model variants, publishes each as a commit, tags them, and promotes the best one — the model-versioning lab. |
| `space/` | Gradio Space — image classifier for the fine-tuned ViT model (bean leaf disease). |
| `space_nlp/` | Gradio Space — sentiment classifier for the fine-tuned DistilBERT model. |
| `summarize-microservice/` | Standalone FastAPI service: GPT-2 text generation + T5 summarization, plus a `Dockerfile` to containerize it. |
| `requirements.txt` | All Python dependencies needed to run everything in this folder locally. |
| `.env.example` | Template for the credentials each student fills in (`HF_TOKEN`, `HF_USERNAME`). Copy it to `.env`. |
| `Makefile` | Every command to set up the environment and interact with the Hugging Face Hub (see below). |

## Prerequisites

- Python 3.10 or later.
- `git-lfs` if you plan to push large model weights via plain `git`
  (`brew install git-lfs` on macOS) — not required for the `hf upload` /
  `push_to_hub()` paths used in the notebooks and the Makefile.
- A Hugging Face account and an access token with **Write** scope:
  https://huggingface.co/settings/tokens

## Setup

```bash
cd MLOps_on_HuggingFace
make install              # creates .venv and installs requirements.txt
cp .env.example .env      # then open .env and fill in HF_TOKEN + HF_USERNAME
make login                # logs the venv's `hf` CLI in using HF_TOKEN
make whoami                # sanity check — should print your HF username
```

`.env` is already excluded by this repository's top-level `.gitignore` —
it will never be committed. **Never** hard-code a real token in a notebook
cell, a script, or the Makefile itself (see *Security* below for why this
matters).

## Running each component

```bash
make notebook              # Jupyter Lab, to open the .ipynb files listed above

make run-space-vision       # launches space/app.py locally (edit MODEL_ID first)
make run-space-nlp          # launches space_nlp/app.py locally (edit MODEL_ID first)

make run-summarizer          # FastAPI microservice on http://localhost:8082
make test-gen                 # hits /generate on the running microservice
make test-sum                 # hits /summarize on the running microservice

make build                    # builds the microservice's Docker image (genapp:v1)
```

Both Spaces (`space/app.py`, `space_nlp/app.py`) ship with a placeholder
`MODEL_ID = "YOUR_USERNAME/..."` — replace it with your own model repo id
(the one you get after `push_to_hub()` or `make upload`) before running or
deploying them.

## Working with the Hub — Makefile reference

Run `make help` at any time to see this list from the terminal.

| Command | Purpose |
|---|---|
| `make install` | Create `.venv` and install `requirements.txt`. |
| `make login` / `make whoami` | Authenticate the CLI with `HF_TOKEN`; check the logged-in account. |
| `make notebook` | Launch Jupyter Lab. |
| `make run-space-vision` / `make run-space-nlp` | Run a Space locally before deploying it. |
| `make run-summarizer`, `make test-gen`, `make test-sum` | Run and smoke-test the FastAPI microservice. |
| `make download-model MODEL=org/name` | Download a model repo locally. |
| `make download-dataset DATASET=org/name` | Download a dataset repo locally. |
| `make create-model-repo NAME=my-model [PRIVATE=1]` | Create a new model repo on the Hub. |
| `make create-dataset-repo NAME=my-dataset [PRIVATE=1]` | Create a new dataset repo on the Hub. |
| `make create-space-repo NAME=my-space [SDK=gradio]` | Create a new Space repo on the Hub. |
| `make upload REPO=user/name LOCAL=./path [TYPE=model\|dataset\|space]` | Push a local folder to a Hub repo. |
| `make tag-model REPO=user/repo TAG=v1` | Tag a model revision — used in the versioning lab. |
| `make build` | Build the microservice's Docker image. |
| `make clean` | Remove `.venv` and Python caches. |

All of these wrap the `hf` CLI (from `huggingface_hub`), which the labs'
notebooks also drive via `notebook_login()` / `HfApi()` — same underlying
mechanics, two different entry points.

## Security

- A token found its way into this folder's old `makefile` in plain text
  and has since been removed as part of this cleanup. **If you are the
  owner of that token, revoke/rotate it now** at
  https://huggingface.co/settings/tokens — treat any token that was ever
  committed or shared as compromised, even after deletion, since it may
  already be cached in git history or elsewhere.
- Going forward: real credentials only ever go in your local `.env` file,
  never in the `Makefile`, a notebook cell, or `app.py`. `.env` is
  git-ignored at the repository root.
- A **Write**-scope token should be treated like a password: never
  committed, never pasted into a shared channel.

## Known issues in the existing app code (not fixed here — flagged for the instructor)

- `summarize-microservice/summarize.py` hard-codes `framework="tf"` in its
  `pipeline(...)` call, but this repo's `requirements.txt` only installs
  PyTorch (`torch`), not TensorFlow — running that specific script directly
  will fail with the current setup. `summarize-microservice/webapp/app.py`
  does not set `framework=` and already works fine with PyTorch; only the
  standalone `summarize.py` script is affected.
- The same script reads `./summarize/input.txt`, but the file actually
  lives at `summarize-microservice/input.txt` — the path assumes a
  directory layout that no longer matches this repo.
- `Dockerfile` referenced a `summarize/webapp` path that doesn't exist
  (the real folder is `summarize-microservice/webapp`) — this has been
  **fixed** as part of this setup, since `make build` depends on it.
