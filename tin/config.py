# -*- coding: utf-8 -*-
import click
import py
import json
import requests


class Config(object):
    def __init__(self, fname=None):
        if fname is None:
            self.conf = py.path.local(
                click.get_app_dir('tin')
            ).join('config.json')
        else:
            self.conf = py.path.local(fname)

        # access
        self.key = None
        self.token = None

        # locations
        self.board = None
        self.inbox = None
        self.today = None
        self.this_week = None
        self.later = None
        self.waiting = None
        self.done = None

        # priorities
        self.important = None
        self.not_important = None
        self.urgent = None
        self.not_urgent = None

        # meta
        self._loaded = False

    def __str__(self):
        return json.dumps(
            {
                'key': self.key,
                'token': self.token,

                'board': self.board,
                'inbox': self.inbox,
                'today': self.today,
                'this_week': self.this_week,
                'later': self.later,
                'waiting': self.waiting,
                'done': self.done,

                'important': self.important,
                'not_important': self.not_important,
                'urgent': self.urgent,
                'not_urgent': self.not_urgent,
            },
            indent=4
        )

    def __repr__(self):
        return '<Config: \n%s\n>' % self

    def load(self):
        if self._loaded:
            pass

        try:
            config = json.loads(self.conf.read())
        except py.error.ENOENT:
            return

        keys = [
            'key', 'token',

            'board', 'inbox', 'today', 'this_week', 'later', 'waiting', 'done',

            'important', 'not_important', 'urgent', 'not_urgent',
        ]

        for key in keys:
            setattr(self, key, config[key])

        self._loaded = True

    def save(self):
        self.conf.ensure()
        with self.conf.open('w') as out:
            out.write(str(self))

    def get_session(self):
        sess = requests.Session()
        sess.params = {
            'key': self.key,
            'token': self.token,
        }

        return sess

pass_config = click.make_pass_decorator(Config, ensure=True)
