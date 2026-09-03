# ==========================================================================
# Makefile — MLOps_on_HuggingFace
# Central commands for local dev and for interacting with the Hugging Face
# Hub, for every activity in this folder (notebooks, Spaces, microservice).
#
# First time setup:
#   make install              # creates .venv and installs requirements.txt
#   cp .env.example .env      # then fill in HF_TOKEN and HF_USERNAME
#   make login
#
# Run `make help` to list every command.
# ==========================================================================

-include .env
export

VENV    := .venv
PY      := $(VENV)/bin/python
PIP     := $(VENV)/bin/pip
HF      := $(VENV)/bin/hf
JUPYTER := $(VENV)/bin/jupyter

.DEFAULT_GOAL := help

.PHONY: help init install login whoami notebook \
        run-space-vision run-space-nlp run-summarizer test-gen test-sum \
        download-model download-dataset \
        create-model-repo create-dataset-repo create-space-repo \
        upload tag-model build clean

help: ## Show this help
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

# --- Setup -----------------------------------------------------------------

init: ## Create the local virtual environment (.venv)
	python3 -m venv $(VENV)

install: init ## Create .venv and install all requirements
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo ""
	@echo "Done. Next steps:"
	@echo "  1) cp .env.example .env   (then fill in HF_TOKEN and HF_USERNAME)"
	@echo "  2) make login"

# --- Hugging Face authentication --------------------------------------------

login: ## Log in to the Hugging Face Hub using HF_TOKEN from .env
	@test -n "$$HF_TOKEN" || (echo "HF_TOKEN is not set. Copy .env.example to .env and fill it in." && exit 1)
	$(HF) auth login --token $$HF_TOKEN --add-to-git-credential

whoami: ## Show which Hugging Face account is currently logged in
	$(HF) auth whoami

# --- Notebooks & demos -------------------------------------------------------

notebook: ## Launch Jupyter Lab on the course notebooks
	$(JUPYTER) lab

run-space-vision: ## Run the vision (ViT) Gradio Space locally — edit space/app.py MODEL_ID first
	$(PY) space/app.py

run-space-nlp: ## Run the NLP (DistilBERT) Gradio Space locally — edit space_nlp/app.py MODEL_ID first
	$(PY) space_nlp/app.py

run-summarizer: ## Run the FastAPI text-generation/summarization microservice locally (port 8082)
	$(PY) summarize-microservice/webapp/app.py

test-gen: ## Quick manual test hitting the running microservice's /generate endpoint
	$(PY) summarize-microservice/try_generate.py

test-sum: ## Quick manual test hitting the running microservice's /summarize endpoint
	$(PY) summarize-microservice/try_summarize.py

# --- Interacting with the Hub ------------------------------------------------

download-model: ## Download a model repo locally. Usage: make download-model MODEL=org/model-name
	@test -n "$(MODEL)" || (echo "Usage: make download-model MODEL=org/model-name" && exit 1)
	$(HF) download $(MODEL)

download-dataset: ## Download a dataset repo locally. Usage: make download-dataset DATASET=org/dataset-name
	@test -n "$(DATASET)" || (echo "Usage: make download-dataset DATASET=org/dataset-name" && exit 1)
	$(HF) download $(DATASET) --repo-type dataset

create-model-repo: ## Create a model repo on the Hub. Usage: make create-model-repo NAME=my-model [PRIVATE=1]
	@test -n "$(NAME)" || (echo "Usage: make create-model-repo NAME=my-model [PRIVATE=1]" && exit 1)
	$(HF) repos create $(NAME) $(if $(PRIVATE),--private,)

create-dataset-repo: ## Create a dataset repo on the Hub. Usage: make create-dataset-repo NAME=my-dataset [PRIVATE=1]
	@test -n "$(NAME)" || (echo "Usage: make create-dataset-repo NAME=my-dataset [PRIVATE=1]" && exit 1)
	$(HF) repos create $(NAME) --repo-type dataset $(if $(PRIVATE),--private,)

create-space-repo: ## Create a Space on the Hub. Usage: make create-space-repo NAME=my-space [SDK=gradio]
	@test -n "$(NAME)" || (echo "Usage: make create-space-repo NAME=my-space [SDK=gradio]" && exit 1)
	$(HF) repos create $(NAME) --repo-type space --sdk $(if $(SDK),$(SDK),gradio)

upload: ## Upload a local folder to a repo. Usage: make upload REPO=user/name LOCAL=./path [TYPE=model|dataset|space]
	@test -n "$(REPO)" && test -n "$(LOCAL)" || (echo "Usage: make upload REPO=user/repo LOCAL=./path [TYPE=model|dataset|space]" && exit 1)
	$(HF) upload $(REPO) $(LOCAL) . $(if $(TYPE),--repo-type $(TYPE),)

tag-model: ## Tag a model version (used in the versioning lab). Usage: make tag-model REPO=user/repo TAG=v1
	@test -n "$(REPO)" && test -n "$(TAG)" || (echo "Usage: make tag-model REPO=user/repo TAG=v1" && exit 1)
	$(HF) repos tag create $(REPO) $(TAG)

# --- Docker (summarization microservice) ------------------------------------

build: ## Build the summarization microservice Docker image
	docker build -t genapp:v1 -f Dockerfile .

# --- Housekeeping -------------------------------------------------------------

clean: ## Remove the virtual environment and Python caches
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
