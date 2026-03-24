# CCOE AI Deduplication Pipeline

An AI Agent to automatically clean the deduplication registration information comes from one individual.

## Table of Contents

- [Introduction](#introduction)
- [Preperation](#preperation)
- [Installation](#installation)
- [Environment Settings](#environment-settings)
- [Run the Pipeline](#run-the-pipeline)
- [Project Structure](#project-structure)
- [Output](#output)
- [Technology Stack](#technology-stack)

## Introduction

Registration datasets often contain duplicate information for the same individual. Manual deduplication is very slow. **CCOE AI Deduplication Pipeline** automates this by:

1. **Normalising** phone numbers and country codes for consistent comparison.
2. **Embedding** each participant record as a dense vector using a configurable embedding model.
3. **Deduplicating** by computing cosine similarity of all record information pairs and remoiving nearest-matches above a standard threshold.
4. **Reporting** through an LLM agent that reads the deduplicated records and outputs the final result.

## Preperation

- Python **3.10** or higher
- One of the following for the LLM and embedding backend (or you can deploy your local LLM and embedding models using Ollama):
  - **NVIDIA NIM** API key (or any OpenAI-compatible endpoint)
  - **Ollama** running locally
  - **HuggingFace** model weights accessible

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Fovir-GitHub/ccoe.git
cd ccoe

# 2. Create and activate a virtual environment through conda or venv
# Conda
conda create -n my_ccoe python=3.10
conda activate my_ccoe

# Venv
python -m venv .venv
.venv\Scripts\activate # Windows
source .venv/bin/activate # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

## Environment Settings

Copy the `.env.example` to `.env`, and modify the environment variables.

```bash
cp .env.example .env
```

### Using Ollama locally

Go to [Ollama](https://ollama.com/) to deploy your local LLM, then point the pipeline to the correct endpoint and model name.

```dotenv
APP_AGENT__PROVIDER=ollama
APP_AGENT__MODEL=llama3.1:8b
APP_AGENT__ENDPOINT=http://localhost:11434

APP_EMBEDDING__PROVIDER=ollama
APP_EMBEDDING__MODEL_NAME=nomic-embed-text
```

> **Tips**: Run `ollama list` to get the model name.

## Run the Pipeline

Use the following command to run the pipeline, replacing `/path/to/data.xlsx` and `/path/to/result.xlsx` with the actual path to your input or output `.xlsx` file:

```bash
python -m src.ccoe_ai.main /path/to/data.xlsx /path/to/result.xlsx
```

## Project Structure

```
.
├── .github/workflows/  # GitHub Actions
├── data/               # Data files
├── src/ccoe_ai
│   ├── config/         # Configuration
│   ├── normalization/  # Normalization functions
│   ├── services/       # Embedding generator and similarity calculator
│   ├── tools/          # Tools for agent
│   ├── utils/          # Utils
│   ├── workflow/       # Agent workflow
│   ├── __init__.py
│   └── main.py         # Entrypoint
├── tests/              # Test cases
├── .env.example
├── .envrc
├── .gitignore
├── flake.lock
├── flake.nix
├── README.md
└── requirements.txt
```

## Output

The final output printed to terminal is a CSV-formatted list of reduplicates participants, produced by the LLM. The whole cleaned dataset is saved as `.xlsx` in the `data/deduplicated.xlsx`.

## Technology Stack

### Language & Runtime

| Item              | Detail                                      |
| ----------------- | ------------------------------------------- |
| Language          | Python 3.10+                                |
| Package structure | Namespace package under `src/ccoe_ai/`      |
| Entry point       | `python -m src.ccoe_ai.main <path_to.xlsx>` |

### Core Framework: LangChain (LCEL)

| Component          | Role                                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------- |
| `langchain-core`   | `RunnableLambda`, `RunnableSerializable`, `ChatPromptTemplate`, `StrOutputParser`, `HumanMessage` |
| `langchain-ollama` | `ChatOllama` — local LLM via Ollama daemon                                                        |
| `langchain-openai` | `ChatOpenAI`                                                                                      |
| `langchain.tools`  | `@tool` decorator to expose `build_embeddings` as an LLM-callable tool                            |

The chain is assembled in `workflow/workflow.py`:

### LLM / Agent

| Item                      | Detail                                                                   |
| ------------------------- | ------------------------------------------------------------------------ |
| Abstraction               | `BaseChatModel` (LangChain)                                              |
| Ollama                    | `ChatOllama` — points to local Ollama (default `http://localhost:11434`) |
| OpenAI-compatible backend | `ChatOpenAI` — works with OpenAI, NVIDIA NIM, Azure OpenAI, etc.         |
| Tool binding              | `llm.bind_tools(TOOL_LIST)` — enables structured function-calling        |
| Prompt style              | System + Human `ChatPromptTemplate` + Role Play Style                    |

### Data Pipeline:

### Raw Data Ingestion

| Library  | Usage                                                     |
| -------- | --------------------------------------------------------- |
| `pandas` | `read_excel()` reads `.xlsx` input; column name stripping |

### Normalization

| Library        | Usage                                                                   |
| -------------- | ----------------------------------------------------------------------- |
| `pycountry`    | ISO 3166-1 alpha-2 country code lookup and validation; defaults to `MY` |
| `phonenumbers` | Parses and formats phone numbers to E.164 standard                      |
| `pandas`       | DataFrame row-wise transformations via `.apply()`                       |

### Embedding & Deduplication

| Library        | Usage                                                       |
| -------------- | ----------------------------------------------------------- |
| `numpy`        | Converts embedding lists to 2D ndarray                      |
| `scikit-learn` | `cosine_similarity()` — computes full N×N similarity matrix |
| `tqdm`         | Progress bar during batched embedding generation            |

### Persistence

| Library    | Usage                                                                           |
| ---------- | ------------------------------------------------------------------------------- |
| `pandas`   | `df.to_parquet()` / `pd.read_parquet()` — stores embeddings + metadata          |
| `pyarrow`  | Parquet engine used by pandas                                                   |
| `tempfile` | OS-managed temp files for intermediate normalized `.xlsx` and output `.parquet` |
