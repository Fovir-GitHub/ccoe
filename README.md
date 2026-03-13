# LangChain Deduplication Project

This LangChain-based deduplication/AI Agent project is used to automatically remove duplicate information from databases.

## Features

- Supports information deduplication and processing

- LLM API can be configured via `.env` files

- Supports importing Excel/CSV data

- Extensible community tools (LangChain Community)

## Installation

1. Clone the repository

```bash

git clone https://github.com/Fovir-GitHub/ccoe.git
cd ccoe
```

2. Create a virtual environment

```bash

python -m venv venv
source venv/Scripts/activate # Windows
# OR
source venv/bin/activate # Mac/Linux
```

3. Install dependencies

```bash

pip install -r requirements.txt
```

## Configuration

1. Copy .env.example to .env
```bash

cp .env.example .env
```

2. Edit `.env` file, fill in your own configuration(API KEY)

## Project Structure