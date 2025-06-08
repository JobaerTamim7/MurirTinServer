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
.venv\Scripts\activate
```


### 3. Sync MurirTin Server
Install the MurirTin server using the `uv` package manager:
```bash
uv sync
```
### 4. Initialize the Database
1. Create .env file in the root directory with the following content:
   ```env
    DB_URL=sqlite:///./data/murirtin.db
   ```
2. Install the pakage to use cli tools:
    ```bash
    uv pip install -e .
    ```
3. Initialize the database:
    ```bash
    uv run init-db
    ```   