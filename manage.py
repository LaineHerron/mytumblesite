import sys
import random
import mongoengine
import argparse
import models
from bottle import run
import routings


def make_initial_posts():
    user1 = models.User(username="user1", password="password")
    user1.save()
    user2 = models.User(username="user2", password="password")
    user2.save()
    comment1 = models.Comment(
                    author=user1,
                    content="I have something to say about that"
                    )
    comment2 = models.Comment(
                    author=user2,
                    content="Ready my comment!"
                    )
    comment3 = models.Comment(
                    author=user2,
                    content="yes you an comment on your own psot"
                    )
    post1 = models.Post(
                author=user1,
                title = "The First Post",
                content = "Yay, I'm first!",
                comments = [comment1, comment2]
                )
    post1.save()
    post2 = models.Post(
                author=user2,
                title = "The second post is still important",
                content = "Just saying",
                comments = [comment3]
                )
    post2.save()



parser = argparse.ArgumentParser()
parser.add_argument("command", type=str,
                    help="specify 'runserver' to start the server")
parser.add_argument("-host", type=str,
                    help="specify server host, defaults to localhost")
parser.add_argument("-port", type=int,
                    help="specify server port, defaults to 8080")
args = parser.parse_args()

if args.host:
    host = args.host
else:
    host = 'localhost'

if args.port:
    port = args.port
else:
    port = 8080

if args.command == "runserver":
    mongoengine.connect('mytumblelog(%s)'%str(random.randint(1,9999)))
    make_initial_posts()
    run(host='localhost', port=8080)
    
