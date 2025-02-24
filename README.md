# pyonb

> [!WARNING]  
> This repo is under construction.

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Tests status][tests-badge]][tests-link]
[![Linting status][linting-badge]][linting-link]
[![Documentation status][documentation-badge]][documentation-link]
[![License][license-badge]](./LICENSE.md)

<!-- prettier-ignore-start -->
[tests-badge]:              https://github.com/SAFEHR-data/pyonb/actions/workflows/tests.yml/badge.svg
[tests-link]:               https://github.com/SAFEHR-data/pyonb/actions/workflows/tests.yml
[linting-badge]:            https://github.com/SAFEHR-data/pyonb/actions/workflows/linting.yml/badge.svg
[linting-link]:             https://github.com/SAFEHR-data/pyonb/actions/workflows/linting.yml
[documentation-badge]:      https://github.com/SAFEHR-data/pyonb/actions/workflows/docs.yml/badge.svg
[documentation-link]:       https://github.com/SAFEHR-data/pyonb/actions/workflows/docs.yml
[license-badge]:            https://img.shields.io/badge/License-MIT-yellow.svg
<!-- prettier-ignore-end -->

Python SDK for OnBase REST API

This project is developed in collaboration with the
[Centre for Advanced Research Computing](https://ucl.ac.uk/arc), University
College London.

## About

### Project Team

Tom Roberts ([tom.roberts@ucl.ac.uk](mailto:tom.roberts@ucl.ac.uk))

<!-- TODO: how do we have an array of collaborators ? -->

### Research Software Engineering Contact

Centre for Advanced Research Computing, University College London
([arc.collaborations@ucl.ac.uk](mailto:arc.collaborations@ucl.ac.uk))

## Built With

<!-- TODO: can cookiecutter make a list of frameworks? -->

- [Framework 1](https://something.com)
- [Framework 2](https://something.com)
- [Framework 3](https://something.com)

## Getting Started

### Prerequisites

<!-- Any tools or versions of languages needed to run code. For example specific Python or Node versions. Minimum hardware requirements also go here. -->

`pyonb` requires Python 3.11&ndash;3.13.

### Installation

<!-- How to build or install the application. -->

We recommend installing in a project specific virtual environment created using
a environment management tool such as
[Conda](https://docs.conda.io/projects/conda/en/stable/). To install the latest
development version of `pyonb` using `pip` in the currently active
environment run

```sh
pip install git+https://github.com/SAFEHR-data/pyonb.git
```

Alternatively create a local clone of the repository with

```sh
git clone https://github.com/SAFEHR-data/pyonb.git
```

and then install in editable mode by running

```sh
pip install -e .
```

### Running Locally

How to run the application on your local system.

### Running Tests

<!-- How to run tests on your local system. -->

Tests can be run across all compatible Python versions in isolated environments
using [`tox`](https://tox.wiki/en/latest/) by running

```sh
tox
```

To run tests manually in a Python environment with `pytest` installed run

```sh
pytest tests
```

again from the root of the repository.

### Building Documentation

The MkDocs HTML documentation can be built locally by running

```sh
tox -e docs
```

from the root of the repository. The built documentation will be written to
`site`.

Alternatively to build and preview the documentation locally, in a Python
environment with the optional `docs` dependencies installed, run

```sh
mkdocs serve
```

## Roadmap

- [x] Initial design with Mock data and database
- [ ] Proof-of-Concept --- compatible with UCLH OnBase API 
- [ ] Minimum Viable Product

## Acknowledgements

This work was funded by NIHR UCLH/UCL Biomedical Research Centre.
