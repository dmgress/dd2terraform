#! /usr/bin/env python

from datadog import initialize, api
from jinja2 import Environment, PackageLoader, select_autoescape
from dotenv import load_dotenv

import os
import json
import click

@click.command()
@click.option('--time_board', prompt='Which board(s)?', help='Time board to convert')
@click.option('--tf_path', default='../modules/dashboards/no_category', help='Destination folder')
@click.option('--env_path', default='./.env', help='Location of the .env file to use for credentials')
def convert_boards(time_board,tf_path,env_path):
    env = Environment(
            loader=PackageLoader('dd2tf', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
            )

    load_dotenv(verbose=True,dotenv_path=env_path)

    API_KEY = os.getenv("DD_API_KEY")
    APP_KEY = os.getenv("DD_APP_KEY")

    options = {
            'api_key': API_KEY,
            'app_key': APP_KEY
            }

    initialize(**options)

    if time_board == 'all':
        all_boards = [ dash['id'] for dash in api.Timeboard.get_all()['dashes']]
    else:
        all_boards = [ time_board ]

    for board in all_boards:
        time_board = api.Timeboard.get(board)
        if 'dash' not in time_board.keys():
            print("Board with ID {} doesn't exist for this account".format(board))
            continue
        title = time_board['dash']['title']
        filetitle = title.lower().replace(' ','_').replace('.','_')
        if not os.path.exists(tf_path):
                os.makedirs(tf_path)

        with open("{}/{}.json".format(tf_path, filetitle), 'w') as f:
            print("Dumping board '{}' (id: {}) to JSON".format(title, board))
            json.dump(time_board,f, indent=2)

        template = env.get_template('dd2tf.tf.j2')
        with open("{}/{}.tf".format(tf_path, filetitle), 'w') as f:
            print("Converting board '{}' (id: {}) to Terraform".format(title, board))
            template.stream(time_board).dump(f)

    env = Environment(
            loader=PackageLoader('dd2tf', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
            )

if __name__ == '__main__':
    convert_boards()
