# zmux

[![PyPI](https://img.shields.io/pypi/v/zmux.svg)](https://pypi.org/project/zmux/)
[![Changelog](https://img.shields.io/github/v/release/GregKaleka/zmux?include_prereleases&label=changelog)](https://github.com/GregKaleka/zmux/releases)
[![Tests](https://github.com/GregKaleka/zmux/workflows/Test/badge.svg)](https://github.com/GregKaleka/zmux/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/GregKaleka/zmux/blob/master/LICENSE)

A tmux parameterizer

Zmux provides a simple way to parameterize commands across several tmux panes. A simple example:

    $ zmux launch "ls {directory}"
    Supply up to 6 values for directory: ., zmux

    💅 Creating tmux layout
    
    🚀 Sending command to pane 1/2
    🚀 Sending command to pane 2/2

[//]: #

    % ls .
    LICENSE         setup.py        zmux
    README.md       tests           zmux.egg-info
    
    ______________________________________________________

    % ls zmux
    __init__.py     __main__.py     __pycache__     cli.py

## Installation

Installation using `pipx` is recommended:

    pipx install zmux

Or using `pip`:

    pip install zmux

## Usage

For help, run:

    zmux --help

You can also use:

    python -m zmux --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd zmux
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
