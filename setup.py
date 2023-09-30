from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="zmux",
    description="A tmux parameterizer",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Greg Kaleka",
    url="https://github.com/GregKaleka/zmux",
    project_urls={
        "Issues": "https://github.com/GregKaleka/zmux/issues",
        "CI": "https://github.com/GregKaleka/zmux/actions",
        "Changelog": "https://github.com/GregKaleka/zmux/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["zmux"],
    entry_points="""
        [console_scripts]
        zmux=zmux.cli:cli
    """,
    install_requires=["click"],
    extras_require={
        "test": ["pytest"]
    },
    python_requires=">=3.7",
)
