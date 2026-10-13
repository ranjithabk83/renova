# ReuseAI

ReuseAI is a semantic code-reuse prototype using real open-source Python functions from the CodeSearchNet corpus.

## Data integrity

This project does **not** ship fabricated component records. The included downloader retrieves real CodeSearchNet-derived records from the public Hugging Face dataset `Nan-Do/code-search-net-python`.

The dataset contains real Python functions, repository/path metadata, documentation, commit SHA and source URLs. The dataset card reports 455,243 training rows and identifies the source as CodeSearchNet. See `DATASET_SOURCE.md` for references.

## Setup

Activate your virtual environment, then from this folder:

```powershell
pip install -r requirements.txt
python training/download_real_dataset.py
streamlit run app.py
```

The downloader defaults to 10,000 real records so the prototype is manageable on a normal laptop. Change `LIMIT` in `training/download_real_dataset.py` if you want more.

## What the score means

The displayed score is cosine similarity between the natural-language query embedding and the embedding of the indexed function's documentation/name/code. It is **not** a claim that the function is automatically compatible or safe to reuse.

## Dataset location

After downloading:

`data/components.csv`

Raw/large dataset material can be kept under:

`datasets/raw/`

## Run

```powershell
streamlit run app.py
```
