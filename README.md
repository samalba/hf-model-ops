# 🤗 MLOps with Hugging Face Spaces and Dagger

## Overview

This project shows how to automate a full ML Application with build, test and deploy, using Dagger pipelines.

All pipelines are written in Python, using the [Dagger Python SDK](https://docs.dagger.io/sdk/python).

## Dependencies

The project uses the following technologies:

- [Dagger](https://dagger.io/) - for the programmable pipelines
- Hugging Face Hub - for pulling the model and weights (using the Transformers library)
- Hugging Face Space - for running the Application

## How to run the pipelines

The pipeline `deploy_space.py` will run the `linter` and the `test` pipelines before deploying the code.

```sh
cd ci/
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd ..
dagger run python ./ci/deploy_space.py
```

It's possible to only run the linter:

```sh
dagger run python ./ci/lint.py
```

Or the model tests:

```sh
dagger run python ./ci/test.py
```

## Pipelines

TODO (lint, test, deploy)

## Why Dagger

- cache (model weights and python deps)
- running locally
- github action integration
- DAG: only run what's needed and in parallel whenever possible

## Future

- Fine-tune model
- Swap a model with another
