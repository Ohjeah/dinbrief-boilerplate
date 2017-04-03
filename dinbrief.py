import os
from collections import ChainMap

import yaml
import click
import delegator

THIS_DIR = os.path.dirname(__file__)
CONFIG_DIR =  os.path.join(os.path.expanduser("~"), ".config/dinbrief")

DEFAULTS = {
    "compiler": "pandoc",
    "flags": "--latex-engine=xelatex",
    "template": os.path.join(THIS_DIR, "template.tex"),
    "signature": "signatur.pdf",
}

def get_config():
    user_dir = os.path.expanduser("~")
    user_config = {}
    user_template = os.path.join(CONFIG_DIR, "template.tex")
    user_signatur = os.path.join(CONFIG_DIR, "signature.pdf")
    user_defaults = os.path.join(CONFIG_DIR, "defaults.yml")

    if os.path.exists(user_template):
        user_config["template"] = user_template

    if os.path.exists(user_template):
        user_config["signature"] = user_signatur

    if os.path.exists(user_template):
        user_config["defaults"] = user_defaults

    return ChainMap(user_config, DEFAULTS)


@click.command()
@click.option("--md", default="letter.md")
def compile_letter(md, pdf="output.pdf"):
    config = get_config()
    cmd = "{compiler} {defaults} {md} -o {pdf} --template={template}  {flags} -M signature={signature}".format(md=md, pdf=pdf, **config)
    print(cmd)
    c = delegator.run(cmd)
    print(c.out)


@click.command()
def create_defaults():
    delegator.run("mkdir -p {}".format(CONFIG_DIR))

    tpath = os.path.join(CONFIG_DIR, "template.tex")

    if not os.path.exists(tpath):
        delegator.run("cp {template} {tpath}".format(cdir=CONFIG_DIR, tpath=tpath))


    dpath = os.path.join(CONFIG_DIR, "defaults.yml")
    if not os.path.exists(dpath):
        delegator.run("cp {defaults} {dpath}".format(cdir=CONFIG_DIR, dpath=dpath))


if __name__ == '__main__':
    cli()
