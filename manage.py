import sys
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
parser.add_argument("-s", "--server", type=str,
                    help="specify web server host, defaults to localhost",
                    default="localhost")
parser.add_argument("-p", "--port", type=int,
                    help="specify web server port, defaults to 8080",
                    default=8080)
parser.add_argument("-r", "--rsname", type=str,
                    help="specify mongodb replica set name. Default is single server")
parser.add_argument("command", type=str,
                    help="specify 'runserver' to start the server")
parser.add_argument("hosts", nargs=argparse.REMAINDER,
                    help="specify mongodb seed list of the form host:port")
args = parser.parse_args()

if args.rsname:
    rsname = args.rsname
    users = True
else:
    users = False
    
hostportlist = args.hosts
    
if args.command == "runserver":
    dbname = 'mytumblelog(%s)'%str(random.randint(1,9999))    
    if users:
        connectstr = 'mongodb://%(hostport)s/%(db)s?replicaSet=%(rs)s' % \
                     {'hostport': join(hostportlist,','), 'db':dbname, 'rs':rsname}
    else:
        if len(hostportlist) > 1:
            raise Exception("List of hosts not supported when not using replica set")
        if len(hostportlist) > 0:
            connectstr = 'mongodb://%(hostport)s/%(db)s' % \
                        {'hostport':hostportlist[0], 'db':dbname}
        else:
            connectstr = 'mongodb://localhost:27017/%(db)s' % \
                        {'db':dbname}
    print connectstr
    mongoengine.connect(dbname, host=connectstr)
    make_initial_posts()
    run(host=args.server, port=args.port)
