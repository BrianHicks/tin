# -*- coding: utf-8 -*-
from . import cli, config
import click
import webbrowser


@cli.command()
@config.pass_config
def setup(config):
    """set up configuration for you to use tin."""
    old = config.key
    config.key = click.prompt(
        'key (from https://trello.com/1/appKey/generate)',
        default=config.key,
    )

    if config.token is None or old != config.key:
        _reauthenticate(config, save=False)

    sess = config.get_session()

    # get boards
    click.echo('getting boards...')
    boards_resp = sess.get('https://trello.com/1/members/my/boards?fields=name,id,dateLastView')
    assert boards_resp.ok

    print 'asdf'

    boards = sorted(
        boards_resp.json(),
        key=lambda board: board.get('dateLastView', None)
    )
    board = show_and_get_choice(boards, 'Which board shall we use?')
    config.board = board['id']

    # get the lists on that board to choose one...
    click.echo('getting lists')
    lists_resp = sess.get(
        'https://trello.com/1/boards/%s/lists?fields=name,id,dateLastActivity' % board['id']
    )
    assert lists_resp.ok

    lists = sorted(
        lists_resp.json(),
        key=lambda list_: list_.get('dateLastActivity', None)
    )

    show_choices(lists)
    config.inbox = get_choice(lists, 'Which list is Inbox?')['id']
    config.today = get_choice(lists, 'Which list is Today?')['id']
    config.this_week = get_choice(lists, 'Which list is This Week?')['id']
    config.later = get_choice(lists, 'Which list is Later?')['id']
    config.waiting = get_choice(lists, 'Which list is Waiting?')['id']
    config.done = get_choice(lists, 'Which list is Done?')['id']

    # ... and the labels so we can use those too
    click.echo('getting labels')
    labels_resp = sess.get(
        'https://trello.com/1/boards/%s/labels' % board['id']
    )
    assert labels_resp.ok

    labels = labels_resp.json()
    for label in labels:
        if not label['name']:
            label['name'] = label['color']

    show_choices(labels)
    config.important = get_choice(labels, 'Which label is Important?')['color']
    config.not_important = get_choice(labels, 'Which label is Not Important?')['color']
    config.urgent = get_choice(labels, 'Which label is Urgent?')['color']
    config.not_urgent = get_choice(labels, 'Which label is Not Urgent?')['color']

    print config

    config.save()


def show_and_get_choice(choices, prompt, default=-1):
    show_choices(choices)
    return get_choice(choices, prompt, default)


def show_choices(choices):
    for i, choice in enumerate(choices):
        click.echo('%d: %s' % (i, choice['name']))


def get_choice(choices, prompt, default=-1):
    return choices[int(click.prompt(
        prompt,
        type=click.Choice(map(str, range(len(choices)))),
        default=default, show_default=False
    ))]


@cli.command()
@config.pass_config
def reauthenticate(config):
    _reauthenticate(config)


def _reauthenticate(config, save=True):
    """reauthenticate when your token expires."""
    click.echo('About to open a web browser to get your new token')
    click.confirm('continue', default=True, abort=True)

    webbrowser.open(
        'https://trello.com/1/authorize?key=%s&name=tin&expiration=30days&response_type=token&scope=read,write' % (
            config.key
        )
    )

    config.token = click.prompt('token after allowing')

    if save:
        config.save()
