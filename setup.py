import os
import sys
import ast
import re
from pathlib import Path
from setuptools import find_packages, setup

CURRENT_DIR = Path(__file__).parent


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()


def get_long_description() -> str:
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


with open(CURRENT_DIR / "requirements.txt", "r") as f:
    REQUIRED = f.readlines()


def get_version() -> str:
    black_py = CURRENT_DIR / "dinbrief.py"
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(black_py, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setup(
    name="dinbrief.py",
    version=get_version(),
    description="Dinbrief made easy",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Markus Quade",
    author_email="info@markusqua.de",
    url="https://github.com/ohjeah/dinbrief-boilerplate",
    py_modules=["dinbrief"],
    install_requires=REQUIRED,
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    entry_points={"console_scripts": ["dinbrief = dinbrief:cli"]},
)
