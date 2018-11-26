import json
import logging

import click
from vk_api import VkApi

from vk.vk_wrapper import VkWrapper


@click.group()
def cli():
    """A collection of CLI utilities for VK"""
    pass


@cli.command()
@click.argument('username')
@click.option('--password', prompt='Account password', hide_input=True)
def auth(username, password):
    """Saves auth info. USERNAME can be a phone number or an email"""
    session = VkApi(username, password)
    session.auth()
    json.dump({'usernames': [username]}, open('./tmp/vk.json', 'w'))
    print("Auth successful, token saved to vk_config.json")


@cli.command()
@click.option('-oid', help='object id (i.e. 123 for a user or -123 for a community, or string for a handle)')
@click.option('--limit', type=int, help='post limit, by default entire wall is fetched', required=False, default=None)
@click.option('-f', '--format', type=click.Choice(['text', 'json']), help='output format', default='text')
@click.argument('file', type=click.File('w'))
def get_wall_text(oid, limit, format, file):
    """Fetches all wall post texts and saves to FILE"""
    wall = api.get_wall(oid, limit)
    if format == 'text':
        file.write("\n".join([p['text'] for p in wall]))
    pass


if __name__ == '__main__':
    logging.basicConfig(level='INFO')

    api = VkWrapper()
    cli()
