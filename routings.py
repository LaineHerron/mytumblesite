from bottle import route, post, redirect, template, request
import models

@route('/')
def main_page():
    return template(
            'templates/main.html',
            current_user = models.current_user,
            posts=models.Post.objects,
            show_post=False,
            show_comment=False,
           )

@route('/sign_in')
def sign_in_page(message=None):
    return template(
            'templates/sign_in.html',
            current_user = models.current_user, 
            message = message
           )

@post('/sign_in')
def sign_in_action():
    if request.forms.get("button") == "Sign in":
        username = request.forms.get("username")
        password = request.forms.get("password")
        if models.User.objects(username=username).count() == 0:
            return sign_in_page(message="username not found")
        else:
            linked_author = models.User.objects(username=username).first()
            if not password == linked_author.password:
                return sign_in_page(message="incorrect password")
            else:
                models.current_user = linked_author
                redirect('/')
                return main_page()
    else: # request.forms.get("buton") == "Create account"
        username = request.forms.get("new_username")
        password1 = request.forms.get("new_password1")
        password2 = request.forms.get("new_password2")
        if models.User.objects(username=username).count() != 0:
            return sign_in_page(message="username taken")
        elif password1 != password2:
            return sign_in_page(message="passwords do not match")
        else:
            user = models.User(username=username, password=password1)
            user.save()
            models.current_user = user
            redirect('/')
            return main_page()

@route('/account')
def account_page(message=None):
    if models.current_user==None:
        return "<b>No user logged in</b>"
    else:
        return template(
                'templates/account.html',
                current_user = models.current_user,
                message = message
               )

@post('/account')
def account_page_action():
    if request.forms.get("button") == "Update info":
        # Get fields from page
        first_name = request.forms.get('first_name')
        last_name = request.forms.get('last_name')
        email = request.forms.get('email')
        cur_pass = request.forms.get('current_password')
        new_pass1 = request.forms.get('new_password1')
        new_pass2 = request.forms.get('new_password2')

        cur_user = models.current_user
        cur_user.first_name = first_name
        cur_user.last_name = last_name
        cur_user.email = email
        if cur_pass:
            if cur_pass == cur_user.password:
                if new_pass1 == new_pass2:
                    cur_user.password = new_pass1
                else:
                    cur_user.save()
                    return account_page(message="passwords do not match")
            else:
                cur_user.save()
                return account_page(message="incorrect password")
        cur_user.save()
        return account_page(message="success") 
    else: # else request.forms.get("button") == "Sign out"
        models.current_user = None
        redirect('/')
        return main_page()

@route('/user/<username>')
def user_page(username):
    if models.User.objects(username=username).count() == 0:
        return "<b> User '%s' not found</b>"%username
    else:
        linked_author = models.User.objects(username=username).first()
        return template(
                'templates/main.html',
                current_user = models.current_user,
                posts=models.Post.objects(author=linked_author),
                show_post=linked_author==models.current_user,
                show_comment=False
           )

@post('/user/<username>')
def user_page_action(username):
    post = models.Post(
                author=models.current_user,
                title=request.forms.get("post_title"),
                content=request.forms.get("post_content"),
                )
    post.save()
    return user_page(username)

@route('/post/<username>/<title>')
def post_page(username, title):
    linked_author = models.User.objects(username=username).first()
    post = models.Post.objects(author=linked_author, title=title).first()
    return template(
            'templates/main.html',
            current_user = models.current_user,
            posts=[post],
            show_post=False,
            show_comment=models.current_user!=None
           )

@post('/post/<username>/<title>')
def post_page_action(username, title):
    linked_author = models.User.objects(username=username).first()
    post = models.Post.objects(author=linked_author, title=title).first()
    print post.content
    comment = models.Comment(
                author = models.current_user,
                content = request.forms.get("comment_area")
                )
    post.comments.append(comment)
    print post.comments
    post.save()
    return post_page(username, title)
