# -*- coding: utf-8 -*-
import click
from . import cli
from . import config


@cli.command()
@config.pass_config
@click.argument('text', nargs=-1)
def new(config, text):
    text = ' '.join(text)

    resp = config.get_session().post(
        'https://api.trello.com/1/cards',
        json={
            'idList': config.inbox,
            'name': text,
        }
    )
    assert resp.ok

    click.echo(resp.json()['url'])

# if __name__ == '__main__':
#     args = parser.parse_args()
#     if args.multi:
#         try:
#             for line in sys.stdin.readlines():
#                 print create(line.strip())
#         except KeyboardInterrupt:
#             print 'bye'
#             sys.exit(1)

#     else:
#         print create(' '.join(args.name))

#     sys.exit(0)
