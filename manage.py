import sys
import random
import mongoengine
import argparse
import models
from bottle import run
import routings


def make_initial_posts():
    user1 = models.User(username='user1', password='password')
    user1.save()
    user2 = models.User(username='user2', password='password')
    user2.save()
    comment = models.Comment(author=user2, content='Ready my comment!')
    post = models.Post(author=user1, title='The First Post',
                        content="Yay, I'm first!", comments=[comment])
    post.save()


# Specify and get command line arguments

parser = argparse.ArgumentParser()
parser.add_argument('command', type=str,
                    help="specify 'runserver' to start the server")
parser.add_argument('-host', type=str,
                    help='specify server host, defaults to localhost')
parser.add_argument('-port', type=int,
                    help='specify server port, defaults to 8080')
parser.add_argument('-mongo_host', type=str,
                    help='specify MongoDB host, defaults to localhost')
parser.add_argument('-mongo_port', type=int,
                    help='specify MongoDB port, defaults to 27017')
args = parser.parse_args()

# Use command line arguments / run servers

host = (args.host if args.host else 'localhost')
port = (args.port if args.port else 8080)
mongo_host = (args.mongo_host if args.mongo_host else 'localhost')
mongo_port = (args.mongo_port if args.mongo_port else 27017)

if args.command == 'runserver':
    mongoengine.connect('mytumblelog(%s)' % str(random.randint(1,
                        9999)))
    make_initial_posts()
    run(host='localhost', port=8080)

