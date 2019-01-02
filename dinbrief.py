import logging
import os
import pathlib
from collections import ChainMap

import click
import click_log
import crayons
import delegator
import yaml
from click_default_group import DefaultGroup
from halo import Halo

__version__ = "0.1.0"

THIS_DIR = pathlib.Path(__file__).parent
CONFIG_DIR = pathlib.Path.home() / ".config/dinbrief"

DEFAULTS = {"compiler": "pandoc", "flags": "--pdf-engine=xelatex", "template": THIS_DIR / "template.tex"}

logger = logging.getLogger("dinbrief")
click_log.basic_config(logger)

LOG_LEVELS = {
    "fatal": logging.CRITICAL,
    "error": logging.ERROR,
    "warn": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}

def log(msg, level="info"):
    colors = {
    "debug": crayons.yellow,
    "error": crayons.red,
    }
    fmter = colors.get(level, crayons.black)
    logger.log(LOG_LEVELS.get(level, 0), fmter(msg))


def get_config():
    user_dir = pathlib.Path.home()
    user_config = {}
    user_template = CONFIG_DIR / "template.tex"
    user_defaults = CONFIG_DIR / "defaults.yml"

    if user_template.exists():
        user_config["template"] = user_template

    if user_defaults.exists():
        user_config["defaults"] = user_defaults

    config = ChainMap(user_config, DEFAULTS)
    log("Using config:", "debug")
    for k, v in sorted(config.items()):
        log(f"\t{k}:\t{v}", "debug")
    return config


@click.group(cls=DefaultGroup, default="compile", default_if_no_args=True)
@click_log.simple_verbosity_option(logger)
def cli():
    pass

def run(cmd, text=""):
    text = text or f"Running {cmd.split(' ')[0]}"
    with Halo(text=text, spinner="dots") as spinner:
        log("Running:", "debug")
        log(f"\t$ {cmd}", "debug")
        c = delegator.run(cmd)
        if c.out:
            log(c.out)
        if c.err:
            log(c.err, "error")
            spinner.fail()
        else:
            spinner.succeed()


@cli.command()
@click.option("--md", default="letter.md")
@click.option("--pdf", default=None)
@click.pass_context
def compile(ctx, md, pdf):
    if pdf is None:
        pdf = pathlib.Path(md).with_suffix(".pdf")

    config = get_config()
    cmd = "{compiler} {md} -o {pdf} --template={template} {defaults} {flags}".format(md=md, pdf=pdf, **config)
    run(cmd, text=f"Compiling {md}")


@cli.command()
def create_defaults():
    pathlib.Path(CONFIG_DIR).mkdir(exist_ok=True, parents=True)
    tpath = CONFIG_DIR / "template.tex"
    if not tpath.exists():
        cmd = f"cp {DEFAULTS['template']} {tpath}"
        run(cmd)


@cli.command()
@click.option("--dir", default=os.path.curdir)
def copy(dir):
    letter = THIS_DIR / "letter.md"
    cmd = f"cp {letter} {dir}"
    run(cmd)


if __name__ == "__main__":
    cli()
