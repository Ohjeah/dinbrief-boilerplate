import os
from collections import ChainMap

import yaml
import click
import delegator

THIS_DIR = os.path.dirname(__file__)
CONFIG_DIR =  os.path.join(os.path.expanduser("~"), ".config/dinbrief")

DEFAULTS = {
    "compiler": "pandoc",
    "flags": "--pdf-engine=xelatex",
    "template": os.path.join(THIS_DIR, "template.tex"),
}

def get_config():
    user_dir = os.path.expanduser("~")
    user_config = {}
    user_template = os.path.join(CONFIG_DIR, "template.tex")
    user_defaults = os.path.join(CONFIG_DIR, "defaults.yml")

    if os.path.exists(user_template):
        user_config["template"] = user_template

    if os.path.exists(user_template):
        user_config["defaults"] = user_defaults

    return ChainMap(user_config, DEFAULTS)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--md", default="letter.md")
@click.option("--pdf", default=None)
def compile(md, pdf):
    if pdf is None:
        pdf = os.path.splitext(md)[0] + ".pdf"
    config = get_config()
    cmd = "{compiler} {md} -o {pdf} --template={template} {flags} ".format(md=md, pdf=pdf, **config)
    print(cmd)
    c = delegator.run(cmd)
    print(c.out)


@cli.command()
def create_defaults():
    delegator.run("mkdir -p {}".format(CONFIG_DIR))

    tpath = os.path.join(CONFIG_DIR, "template.tex")

    if not os.path.exists(tpath):
        delegator.run("cp template.tex {tpath}".format(cdir=CONFIG_DIR, tpath=tpath))


@cli.command()
@click.option("--dir", default=os.path.curdir)
def copy(dir):
    delegator.run("cp {letter} {dir}".format(letter=os.path.join(THIS_DIR, "letter.md"), dir=dir))



if __name__ == '__main__':
    cli()
