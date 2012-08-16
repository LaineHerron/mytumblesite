===================================================================
Write a Tumblelog Application with Python 3, Bottle and MongoEngine
===================================================================

Introduction
------------

This tutorial describes how to make a simple tumblelog application using Python 3, the lightweight `Bottle`_ Python web-framework, and `MongoEngine`_.

.. admonition:: Where to get help

   If you're having trouble going through this tutorial, please post
   a message to `mongodb-user`_ or join the IRC chat in *#mongodb* on
   `irc.freenode.net`_ to chat with other MongoDB users who might be
   able to help.

.. _Bottle: http://bottlepy.org/
.. _MongoEngine: http://mongoengine.org/
.. _mongodb-user: http://groups.google.com/group/mongodb-user
.. _irc.freenode.net: http://freenode.net/

Prerequesite
------------

This tutorial assumes you have installed Python 3, MongoDB, and MongoEngine

- `installing Python 3`_
- `installing MongoDB`_
- `installing Mongoengine`_

.. _installing Python 3: http://www.python.org/getit/releases/3.2.3/
.. _installing MongoDB: http://www.mongodb.org/display/DOCS/Quickstart
.. _installing Mongoengine: http://mongoengine.org

Getting Started
---------------

Begin by creating an empty directory named 'tumblelog', which you will use to hold the project.  Download bottle.py into this directory by navigating terminal to 'tumblelog' and executing the following command: 

.. code-block:: bash

   curl -O https://raw.github.com/defnull/bottle/master/bottle.py

Next add an empty file named 'manage.py' to the tumblelog directory.  manage.py will be used to as an interface to start the web server.  Paste the following code into manage.py:

.. code-block:: python

   import sys
   import mongoengine
   import argparse
   #import models
   from bottle import run
   #import routings


   def make_initial_posts():
       pass

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
       dbname = 'mytumblelog(%s)'    
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
       print(connectstr)
       mongoengine.connect(dbname, host=connectstr)
       make_initial_posts()
       run(host=args.server, port=args.port)


You can now run a simple test server.  Begin by running a 'mongod' instance with its default settings (host=localhost, port=27017), then start the web site server by executing the following command:

.. code-block:: bash

   python3.2 manage.py runserver

There should be no errors, and you can visit http://localhost:8080/ in your browser to view a page with a "404" message.

Define the Schema
-----------------

Next define "models" or in MongoDB's terminology, "documents".  In this application, you will define the documents for Post, Comment, and User.  Each Post will contain a list of Comments.  Posts and Comments will have a User specified as their author.  Paste the following code into a new file /tumblelog/models.py:

.. code-block:: python

   from mongoengine import *
   import datetime


   class User(Document):

       username = StringField(required=True, max_length=30)
       password = StringField(required=True, max_length=30)
       first_name = StringField(max_length=30)
       last_name = StringField(max_length=30)
       email = StringField(max_length=30)


   class Comment(EmbeddedDocument):

       author = ReferenceField(User)
       content = StringField(max_length=120, required=True)
       created_at = DateTimeField(default=datetime.datetime.now,
                                  required=True)
       meta = {'ordering': ['-created_at']}


   class Post(Document):

       author = ReferenceField(User)
       title = StringField(required=True, max_length=50)
       content = StringField(max_length=120)
       comments = ListField(EmbeddedDocumentField(Comment))
       created_at = DateTimeField(default=datetime.datetime.now,
                                  required=True)
       meta = {'ordering': ['-created_at']}


   current_user = None


Add Initial Data
----------------

Next we will uncomment the line 'import models' in manage.py, then add a few initial posts and comments.  Complete the 'make_initial_posts()' function in manage.py so that the file looks like this:

.. code-block:: python

   import sys
   import mongoengine
   import argparse
   import models
   from bottle import run
   #import routings


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
       dbname = 'mytumblelog(%s)'    
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
       print(connectstr)
       mongoengine.connect(dbname, host=connectstr)
       make_initial_posts()
       run(host=args.server, port=args.port)


Add HTML Templates
------------------

In this step we will add HTML templates for our website.  We will have one template as header, and three others for main page, sign in page, and account information page. make a new directory within the tumblelog directory and name it "templates".  populate templates with the following files:

tumblelog/templates/header.html

.. code-block:: html

    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>My Tumblelog</title>
        <link href="http://twitter.github.com/bootstrap/1.4.0/bootstrap.css" rel="stylesheet">
        <style>.content {padding-top: 80px;}</style>
      </head>

      <body>
        <div class="topbar">
          <div class="fill">
            <div class="container">
              <h2>
                <a href="/" class="brand">My Tumblelog</a> <small>Starring Bottle, MongoEngine and Python 3</small>
                %if current_user==None:
                  <ul class="nav secondary-nav">
                    <a href="/sign_in" class="btn primary">Sign in</a>
                  </ul>
                %else:
                  <ul class="nav secondary-nav">
                    <small>Signed in as {{ current_user.username }}</small>
                  </ul>
                  <ul class="nav secondary-nav">
                    <a href="/user/{{ current_user.username }}" class="btn primary">Create new post</a>
                  </ul>
                  <ul class="nav secondary-nav">
                    <a href="/account" class="btn primary">Account</a>
                  </ul>
                %end

              </h2>
          
            </div>
          </div>
        </div>

        <div class="container">
          <div class="content">
            %include
          </div>
        </div>
      </body>
    </html>


tumblelog/templates/main.html

.. code-block:: html

   %rebase templates/header.html current_user=current_user

   %if show_post:
     <form method="POST">
       <input type="text" name="post_title" placeholder="Post Title"><br />
       <textarea name="post_content" placeholder="Enter post here." cols=40 rows=6></textarea><br />
       <input type="submit" name="post_submit" class="btn primary" value="Submit">
     </form>
     <hr>
   %end

   %for post in posts:
     <div class="page-header">
       <h1><a href="/post/{{ post.author.username }}/{{ post.title }}">{{ post.title }}</a></h1>
     </div>
     <p>{{ post.content }}<p>
     <p>{{ post.created_at.strftime('%H:%M %Y-%m-%d') }}</p>
     <p><strong><a href="/user/{{ post.author.username }}">{{ post.author.username }}</a></strong> <small>on {{ post.created_at.strftime('%H:%M %Y-%m-%d') }}</small></p>
     <h2>Comments</h2>
     %if post.comments:
       %for comment in post.comments:
          <p>{{ comment.content }}</p>
          <p><strong><a href="/user/{{ comment.author.username }}">{{ comment.author.username }}</a></strong> <small>on {{ comment.created_at.strftime('%H:%M %Y-%m-%d') }}</small></p>
       %end
     %else:
       <p> No comments. </p>
     %end
   %end

   %if show_comment:
     <hr>
     <h2>Add a comment</h2>
     <form method="POST">
       <div class="actions">
         <textarea name="comment_area" placeholder="Enter comment here." cols=40 rows=6></textarea><br />
         <input type="submit" name="comment_button" class="btn primary" value="comment">
       </div>
     </form>
   %end

tumblelog/templates/sign_in.html

.. code-block:: html

   %rebase templates/header.html current_user=current_user

   <form method="POST">
     <h1> Sign in: </h1><br />
     username: <input type="text" name="username" placeholder="Enter username"/><br />
     password: <input type="password" name="password" /><br />
     <input type="submit" name="button" class="btn primary" value="Sign in" />
   </form>

   <hr>
   <form method="POST">
     <h1> or Create account: </h1><br />
     username: <input type="text" name="new_username" placeholder="Enter username"/><br />
     password: <input type="password" name="new_password1" /><br />
     password (again): <input type="password" name="new_password2" /><br />
     <input type="submit" name="button" class="btn primary" value="Create account" />
   </form>

   %if message:
     <b>{{ message }}</b>
   %end

tumblelog/templates/account.html

.. code-block:: html

   %rebase templates/header.html current_user=current_user

   <form method="POST">
     username: <input type="text" name="username" value={{ current_user.username }} readonly/><br />
     First name: <input type="text" name="first_name" value={{ current_user.first_name }} /><br />
     Last name: <input type="text" name="last_name" value={{ current_user.last_name }} /><br />
     email: <input type="text" name="email" value={{ current_user.email }} /><br />
     current password: <input type="password" name="current_password"/><br />
     new password: <input type="password" name="new_password1"/><br />
     new password (again): <input type="password" name="new_password2"/><br />
     <input type="submit" name="button" class="btn primary" value="Update info" />
     <hr>
     <input type="submit" name="button" class="btn primary" value="Sign out">
   </form>

   %if not message==None:
     <b>{{ message }}</b>
   %end

Open these file in your browser to get an idea of what the site will look like.  You should see multiple lines of text starting with '%'.  These lines represent embedded python code that will be executed by bottle.py

Add Routings
------------

Now create a new file in the 'tumblelog' directory and call it routings.py.  routings.py will contain instructions for what to do when a user visits different pages on your site, including which HTML template to use.  Add the following to the new file, /tumblelog/routings.py:

.. code-block:: python

   from bottle import route, post, redirect, template, request
   import models


   @route('/')
   def main_page():
       return template('templates/main.html',
                       current_user=models.current_user,
                       posts=models.Post.objects, show_post=False,
                       show_comment=False)


   @route('/sign_in')
   def sign_in_page(message=None):
       return template('templates/sign_in.html',
                       current_user=models.current_user, message=message)


   @route('/account')
   def account_page(message=None):
       if models.current_user == None:
           return '<b>No user logged in</b>'
       else:
           return template('templates/account.html',
                           current_user=models.current_user,
                           message=message)


   @route('/user/<username>')
   def user_page(username):
       if models.User.objects(username=username).count() == 0:
           return "<b> User '%s' not found</b>" % username
       else:

           # Show posts from user in url

           linked_author = models.User.objects(username=username).first()
           return template('templates/main.html',
                           current_user=models.current_user,
                           posts=models.Post.objects(author=linked_author),
                           show_post=linked_author == models.current_user,
                           show_comment=False)


   @route('/post/<username>/<title>')
   def post_page(username, title):

       # show a specific post and its comments

       linked_author = models.User.objects(username=username).first()
       post = models.Post.objects(author=linked_author,
                                  title=title).first()
       return template('templates/main.html',
                       current_user=models.current_user, posts=[post],
                       show_post=False, show_comment=models.current_user
                       != None)


Uncomment the line 'import routings' in manage.py, and try running the server again.  You should see a start page with our initial posts and a Sign in button in the corner.  However, if you try to sign in or make a new account you will encounter a "Method Not Allowed" error.  To make this work we will have to tell routing.py what to do with the post requests sent out by the pressing buttons.

Add Post handling
-----------------

Append the following code to routings.py

.. code-block:: python

   # Handle Posts ( events sent from HTML templates )

   @post('/sign_in')
   def sign_in_action():

       # Get fields from HTML form

       username = request.forms.get('username')
       password = request.forms.get('password')
       new_username = request.forms.get('new_username')
       new_password1 = request.forms.get('new_password1')
       new_password2 = request.forms.get('new_password2')

       # Do logic for the forms

       if request.forms.get('button') == 'Sign in':
           if models.User.objects(username=username).count() == 0:
               return sign_in_page(message='username not found')
           else:
               linked_author = \
                   models.User.objects(username=username).first()
               if not password == linked_author.password:
                   return sign_in_page(message='incorrect password')
               else:
                   models.current_user = linked_author
                   redirect('/')
                   return main_page()
       else:

           # else if request.forms.get("buton") == "Create account"

           if models.User.objects(username=new_username).count() != 0:
               return sign_in_page(message='username taken')
           elif new_password1 != new_password2:
               return sign_in_page(message='passwords do not match')
           else:
               user = models.User(username=new_username,
                                  password=new_password1)
               user.save()
               models.current_user = user
               redirect('/')
               return main_page()


   @post('/account')
   def account_page_action():
       if request.forms.get('button') == 'Update info':

           # Get fields from page

           first_name = request.forms.get('first_name')
           last_name = request.forms.get('last_name')
           email = request.forms.get('email')
           cur_pass = request.forms.get('current_password')
           new_pass1 = request.forms.get('new_password1')
           new_pass2 = request.forms.get('new_password2')

           # Set current_user attributes (except password)

           cur_user = models.current_user
           cur_user.first_name = first_name
           cur_user.last_name = last_name
           cur_user.email = email

           # Set current_user password attribute

           if cur_pass:
               if cur_pass == cur_user.password:
                   if new_pass1 == new_pass2:
                       cur_user.password = new_pass1
                   else:
                       cur_user.save()
                       return account_page(message='passwords do not match'
                               )
               else:
                   cur_user.save()
                   return account_page(message='incorrect password')
           cur_user.save()
           return account_page(message='success')
       else:

           # else if request.forms.get("button") == "Sign out"

           models.current_user = None
           redirect('/')
           return main_page()


   @post('/user/<username>')
   def user_page_action(username):

       # handle new post

       post = models.Post(author=models.current_user,
                          title=request.forms.get('post_title'),
                          content=request.forms.get('post_content'))
       post.save()
       return user_page(username)


   @post('/post/<username>/<title>')
   def post_page_action(username, title):

       # handle new comment on a post

       linked_author = models.User.objects(username=username).first()
       post = models.Post.objects(author=linked_author,
                                  title=title).first()
       comment = models.Comment(author=models.current_user,
                                content=request.forms.get('comment_area'))
       post.comments.append(comment)
       post.save()
       return post_page(username, title)


You should now have a fully functional Tumblelog!
All of the code for this project can be found at https://github.com/LaineHerron/mytumblesite
