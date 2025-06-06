# Project MurirTin Server Setup Guide

## Recommended Setup Process

### 1. Install Python and pip
Ensure Python 3.7+ is installed with pip. Verify using:
```bash
python --version
pip --version
```

### 2. Install uv Package Manager (Recommended)
Install the `uv` package manager for easier dependency management:
```bash
pip install uv
```
### 3. Activate Virtual Environment
Activate virtual enviornment before working.

for macOS:
```bash
source .venv/bin/activate
```
for Linux:
```bash
source .venv/bin/activate
```
for Windows:
```bash
venv\Scripts\activate
```


### 3. Sync MurirTin Server
Install the MurirTin server using the `uv` package manager:
```bash
uv sync
```
### 4. Running Server with uvicorn:
```bash
uvicorn src.main:app --reload --port 8000
```