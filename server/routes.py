#!/usr/bin/env python
#
# Copyright (C) 2013 Federico Ceratto and others, see AUTHORS file.
# Released under LGPLv3+ license, see LICENSE.txt
#
# Cork example web application
#
# The following users are already available:
#  admin/admin, demo/demo

import bottle
from bottle import static_file, request, route, post, view
from beaker.middleware import SessionMiddleware
from cork import Cork
import logging
import time
from datetime import datetime
import os
import json

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
bottle.debug(True)

# Use users.json and roles.json in the local example_conf directory
aaa = Cork('wombat_conf')

# alias the authorization decorator with defaults
authorize = aaa.make_auth_decorator(fail_redirect="/login", role="user")

import datetime
app = bottle.app()
session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'THIS IS THE MOST SECRET KEY OF ANY THAT EVER WERE DAMMIT!!!!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}
app = SessionMiddleware(app, session_opts)

### API FUNCTIONS ###
FILE_ROOT = "files"

@route('/api')
@route('/api/')
def api_status():
    return { 'status': 'online', 'time': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}

@post('/api/create/<filename:path>')
@authorize()
def api_create(filename):
    user = aaa.current_user.username
    user_path = os.path.join(os.path.abspath(FILE_ROOT), user, filename.strip('/'))
    path, name = os.path.split(user_path)

    if not os.path.isdir(path):
        os.makedirs(path)

    data = json.loads(request.body.read())
    payload = data[u'payload']
    print("Uploaded: " + filename)
    with open(user_path, "w") as f:
        f.write(payload.encode('ascii'))

@route('/api/delete/<filename:path>')
@authorize()
def api_delete(filename):
    user = aaa.current_user.username
    path = os.path.join(os.path.abspath(FILE_ROOT), user, filename.strip('/'))
    os.remove(path)

@route('/api/download/<filename:path>')
@authorize()
def api_download(filename):
    user = aaa.current_user.username
    path = os.path.join(os.path.abspath(FILE_ROOT), user, filename.strip('/'))
    print ("Sending: " + filename)
    root, name = os.path.split(path)
    return static_file(name, root)

@route('/api/list')
@route('/api/list/')
@route('/api/list/<directory:path>')
@authorize()
def api_list(directory = None):
    user = aaa.current_user.username
    items = []

    if directory:
        root = os.path.join(os.path.abspath(FILE_ROOT), user, directory.strip('/'))
    else:
        root = os.path.join(os.path.abspath(FILE_ROOT), user)
        if not os.path.isdir(root):
            os.makedirs(root)

    for item in os.listdir(root):
        path = os.path.join(root, item)
        it = { 't': '', 'name': str(item) }
        if os.path.isdir(path):
            it['t'] = 'dir'
        elif os.path.isfile(path):
            it['t'] = 'file'
        items.append(it);

    return  { 'items': items }

### Webpage items ###
### add webpages here and stuff ###

@route('/')
@authorize()
@view('index')
def index():
    """Only authenticated users can see this"""
    #session = request.environ.get('beaker.session')
    #aaa.require(fail_redirect='/login')
    return dict(
        current_user = aaa.current_user,
    )

# Static pages

@route('/login')
@view('login_form')
def login_form():
    """Serve login form"""
    return {}

@route('/js/<filename>')
def static_js(filename):
    return static_file(filename, 'js')

@route('/js/libs/<filename>')
def static_js(filename):
    return static_file(filename, 'js/libs')

@route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'


# #  Bottle methods  # #

def postd():
    return request.forms


def post_get(name, default=''):
    return request.POST.get(name, default).strip()

### AUTHENTICATION METHODS ###

@post('/login')
def login():
    """Authenticate users"""
    username = post_get('username')
    password = post_get('password')
    aaa.login(username, password, success_redirect='/', fail_redirect='/login')

@route('/user_is_anonymous')
def user_is_anonymous():
    if aaa.user_is_anonymous:
        return 'True'

    return 'False'

@route('/logout')
def logout():
    aaa.logout(success_redirect='/login')


@post('/register')
def register():
    """Send out registration email"""
    aaa.register(post_get('username'), post_get('password'), post_get('email_address'))
    return 'Please check your mailbox.'


@route('/validate_registration/:registration_code')
def validate_registration(registration_code):
    """Validate registration, create user account"""
    aaa.validate_registration(registration_code)
    return 'Thanks. <a href="/login">Go to login</a>'


@post('/reset_password')
def send_password_reset_email():
    """Send out password reset email"""
    aaa.send_password_reset_email(
        username=post_get('username'),
        email_addr=post_get('email_address')
    )
    return 'Please check your mailbox.'


@route('/change_password/:reset_code')
@view('password_change_form')
def change_password(reset_code):
    """Show password change form"""
    return dict(reset_code=reset_code)


@post('/change_password')
def change_password():
    """Change password"""
    aaa.reset_password(post_get('reset_code'), post_get('password'))
    return 'Thanks. <a href="/login">Go to login</a>'

@route('/my_role')
def show_current_user_role():
    """Show current user role"""
    session = request.environ.get('beaker.session')
    print ("Session from simple_webapp", repr(session))
    aaa.require(fail_redirect='/login')
    return aaa.current_user.role


# Admin-only pages

@route('/admin')
@authorize(role="admin", fail_redirect='/sorry_page')
@view('admin_page')
def admin():
    """Only admin users can see this"""
    #aaa.require(role='admin', fail_redirect='/sorry_page')
    return dict(
        current_user = aaa.current_user,
        users = aaa.list_users(),
        roles = aaa.list_roles()
    )


@authorize(role="admin", fail_redirect='/sorry_page')
@post('/create_user')
def create_user():
    try:
        aaa.create_user(postd().username, postd().role, postd().password)
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)


@post('/delete_user')
@authorize(role="admin", fail_redirect='/sorry_page')
def delete_user():
    try:
        aaa.delete_user(post_get('username'))
        return dict(ok=True, msg='')
    except Exception as e:
        print (repr(e))
        return dict(ok=False, msg=e.message)


@post('/create_role')
@authorize(role="admin", fail_redirect='/sorry_page')
def create_role():
    try:
        aaa.create_role(post_get('role'), post_get('level'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)


@post('/delete_role')
@authorize(role="admin", fail_redirect='/sorry_page')
def delete_role():
    try:
        aaa.delete_role(post_get('role'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)

# #  Web application main  # #

def main():
    # Start the Bottle webapp
    bottle.debug(True)
    bottle.run(host="0.0.0.0", app=app, quiet=False, reloader=True)

if __name__ == "__main__":
    main()
