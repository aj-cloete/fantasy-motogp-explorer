# Fantasy MotoGP Explorer
Tools to explore Fantasy MotoGP data

## Installation

### Using poetry
Clone the repo and then install
[poetry](https://python-poetry.org/docs#installing-with-pipx).
You can install the poetry environment using `poetry install` within the root of the repo

### Other virtual environments
If you prefer to use [pipenv](https://pipenv.pypa.io) or another virtual environment manager,
you can look in the [pyproject.toml](pyproject.toml) file for the dependencies and install them
in your virtual environment

## Getting Started

### Streamlit app online
The easiest way to interact with the current version of the tool is to navigate to the
[Fantasy MotoGP Explorer]() app online

### Exploring the app locally
The easiest way to interact with the data is to run the [streamlit](https://streamlit.io/) app
(from the root of the repo):
```python
streamlit run fantasy_motogp_explorer/Welcome.py
```

## Contributing
Feel free to fork and create pull requests!

> Please remember to run `pre-commit install` for linting and for cleaner pull requests.
