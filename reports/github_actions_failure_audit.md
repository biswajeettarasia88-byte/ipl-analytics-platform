# GitHub Actions Failure Audit

## Workflow
.github/workflows/tests.yml

## Commit
38982a2

## Exact Failure
`ModuleNotFoundError: No module named 'matplotlib'` during Pytest test collection of `tests/test_streamlit.py`.

## Failed Step
`Run Pytest Test Suite`

## Root Cause
The GitHub Actions pipeline is executed on an isolated Ubuntu runner (`ubuntu-latest`). The Streamlit application (`streamlit/app.py`) imports `matplotlib.pyplot` for rendering charts. However, `matplotlib` was missing from `requirements.txt`. During local testing, the tests passed because `matplotlib` had been implicitly installed globally in the local environment, hiding the dependency gap. In the clean CI environment, Pytest attempts to parse the tests which imports the application, triggering the fatal `ModuleNotFoundError`.

## Why Local Tests Passed
The local Windows environment possessed a cached, globally installed or cross-dependency-installed instance of `matplotlib`. Pytest locally could resolve the import path flawlessly, returning 22 successful passes.

## Correct Fix
1. Explicitly appended `matplotlib==3.11.1` and `flake8==7.3.0` to `requirements.txt` to strictly capture all runtime and testing bounds.
2. Modified the `tests.yml` CI workflow. Cleaned up the redundant parallel `pip install pytest flake8 shap xgboost scikit-learn streamlit` line, and forced the CI to rely entirely and singularly on `pip install -r requirements.txt`. This guarantees perfect symmetry between the developer environment dependencies and the CI environment.

## Files That Must Change
- `requirements.txt`
- `.github/workflows/tests.yml`

## Files That Must NOT Change
- Any ML logic files (`src/ml/*`)
- Any database logic or models (`sql/*`)
- Any Streamlit code (`streamlit/app.py`)
- Tests (`tests/*`)
