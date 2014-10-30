# -*- coding: utf-8 -*-
from . import cli, config
import click

shortcuts = ['i','t','w','l','d','a']
shortcuts_type = click.Choice(shortcuts)


@cli.command()
@click.option('-s', '--source', type=shortcuts_type, default='i')
@config.pass_config
def process(config, source):
    """
    process cards from one list to another.
    """
    lists = {
        'i': config.inbox,
        't': config.today,
        'w': config.this_week,
        'l': config.later,
        'd': config.done,
        'a': config.waiting,
    }

    source = lists[source]
    session = config.get_session()

    cards_resp = session.get('https://api.trello.com/1/lists/%s/cards?fields=name,labels,dateLastActivity' % source)
    assert cards_resp.ok

    cards = sorted(
        cards_resp.json(),
        key=lambda card: card['dateLastActivity']
    )
    for card in cards:
        click.clear()
        click.echo(card['name'].strip())
        click.echo('-' * len(card['name'].strip()))
        click.echo()

        if card['labels']:
            click.echo('Labels:')

            for label in sorted(card['labels'], key=lambda l: l['name']):

                # determine color
                fg = 'black'
                note = ''
                if label['color'] == 'orange':
                    fg = 'white'
                    bg = None
                    note = ' * orange'
                elif label['color'] == 'purple':
                    bg = 'magenta'
                else:
                    bg = label['color']

                click.echo(
                    click.style(label['name'], fg=fg, bg=bg, bold=True) + note
                )

            click.echo()

        destination = lists[click.prompt(
            'move to? {%s}' % ','.join(shortcuts),
            type=shortcuts_type
        )]

        resp = session.put(
            'https://api.trello.com/1/cards/%s' % card['id'],
            json={
                'idList': destination,
                'pos': 'bottom',
            }
        )
        assert resp.ok

    click.clear()
