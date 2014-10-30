# -*- coding: utf-8 -*-
import click
from . import config


@click.group()
@config.pass_config
def cli(config):
    config.load()

from . import new
from . import setup
