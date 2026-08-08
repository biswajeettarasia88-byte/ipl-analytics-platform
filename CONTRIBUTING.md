# Contributing Guide

First off, thank you for considering contributing to the IPL Analytics & Decision Intelligence Platform!

## 1. Local Setup
1. Fork and clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Download raw Cricsheet JSON data into `data/raw/` (do not commit this data).

## 2. Coding Standards
- **Python**: Follow PEP-8 guidelines. We enforce style via `flake8`.
- **SQL**: Use uppercase for SQL keywords (e.g., `SELECT`, `FROM`, `WHERE`) and snake_case for tables/columns.
- **Paths**: Never use absolute local paths (e.g., `C:\Users\...`). Always use relative paths resolved via `pathlib.Path`.

## 3. Testing Requirements
Before opening a Pull Request, you **must** ensure the test suite passes locally.
```bash
pytest tests/
```
If you are adding a new feature (e.g., a new ML model or SQL view), you must add corresponding tests to the `tests/` directory.

## 4. Pull Request Process
1. Create a branch using the format `feature/your-feature-name` or `bugfix/issue-description`.
2. Commit your changes with clear, descriptive commit messages.
3. Push to your fork and open a Pull Request against the `main` branch.
4. Ensure the GitHub Actions CI pipeline passes (it will automatically run `pytest` and `flake8`).
5. A maintainer will review your code and merge it upon approval.
