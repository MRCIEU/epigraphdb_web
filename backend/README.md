# `epigraphdb_web` backend

## Setup

Only the native environment setup is discussed here.
For setup via docker and the use of environment variables
check the master [README](../README.md).

Prerequsites:

- poetry (install it outside of conda)
- conda

Rough steps:

```
conda env create -f environment.yml
conda activate web_backend
poetry install
make run
```
