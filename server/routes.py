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
from bottle import static_file
from beaker.middleware import SessionMiddleware
from cork import Cork
import logging
import time
from datetime import datetime
import os

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
FILE_ROOT = "/home/foxk5/wombat/server/tmp"

@bottle.route('/api')
@bottle.route('/api/')
def api_status():
    return { 'status': 'online', 'time': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}

@bottle.post('/api/create/<filename:path>')
@authorize()
def api_create(filename):
    user = aaa.current_user.username
    user_path = os.path.join(os.path.abspath(FILE_ROOT), user)

    if not os.path.isdir(user_path):
        os.mkdir(user_path)

    payload = request.json['payload']
    print("Uploaded: " + filename)
    with open(os.path.join(os.path.abspath(FILE_ROOT), user, filename), "w") as f:
        f.write(payload.encode('ascii'))

@bottle.route('/api/delete/<filename:path>')
@authorize()
def api_delete(filename):
    user = aaa.current_user.username
    path = os.path.join(os.path.abspath(FILE_ROOT), user, filename)
    os.remove(path)

@bottle.route('/api/download/<filename:path>')
@authorize()
def api_download(filename):
    user = aaa.current_user.username
    path = os.path.join(os.path.abspath(FILE_ROOT), user, filename)
    print ("Sending: " + filename)
    root, name = os.path.split(path)
    return static_file(name, root)

@bottle.route('/api/list')
@bottle.route('/api/list/')
@bottle.route('/api/list/<directory:path>')
@authorize()
def api_list(directory = None):
    user = aaa.current_user.username
    if directory:
        root = os.path.join(os.path.abspath(FILE_ROOT), user, directory)
    else:
        root = os.path.join(os.path.abspath(FILE_ROOT), user)

    if not os.path.isdir(root):
        os.mkdir(root)

    items = os.listdir(root)

    return  { 'items': items }

### Webpage items ###
### add webpages here and stuff ###

@bottle.route('/')
@authorize()
@bottle.view('index')
def index():
    """Only authenticated users can see this"""
    #session = bottle.request.environ.get('beaker.session')
    #aaa.require(fail_redirect='/login')
    return dict(
        current_user = aaa.current_user,
    )

# Static pages

@bottle.route('/login')
@bottle.view('login_form')
def login_form():
    """Serve login form"""
    return {}


@bottle.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'


# #  Bottle methods  # #

def postd():
    return bottle.request.forms


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()

### AUTHENTICATION METHODS ###

@bottle.post('/login')
def login():
    """Authenticate users"""
    username = post_get('username')
    password = post_get('password')
    print (bottle.request.body.read(), username, password)
    aaa.login(username, password, success_redirect='/', fail_redirect='/login')

@bottle.route('/user_is_anonymous')
def user_is_anonymous():
    if aaa.user_is_anonymous:
        return 'True'

    return 'False'

@bottle.route('/logout')
def logout():
    aaa.logout(success_redirect='/login')


@bottle.post('/register')
def register():
    """Send out registration email"""
    aaa.register(post_get('username'), post_get('password'), post_get('email_address'))
    return 'Please check your mailbox.'


@bottle.route('/validate_registration/:registration_code')
def validate_registration(registration_code):
    """Validate registration, create user account"""
    aaa.validate_registration(registration_code)
    return 'Thanks. <a href="/login">Go to login</a>'


@bottle.post('/reset_password')
def send_password_reset_email():
    """Send out password reset email"""
    aaa.send_password_reset_email(
        username=post_get('username'),
        email_addr=post_get('email_address')
    )
    return 'Please check your mailbox.'


@bottle.route('/change_password/:reset_code')
@bottle.view('password_change_form')
def change_password(reset_code):
    """Show password change form"""
    return dict(reset_code=reset_code)


@bottle.post('/change_password')
def change_password():
    """Change password"""
    aaa.reset_password(post_get('reset_code'), post_get('password'))
    return 'Thanks. <a href="/login">Go to login</a>'

@bottle.route('/my_role')
def show_current_user_role():
    """Show current user role"""
    session = bottle.request.environ.get('beaker.session')
    print ("Session from simple_webapp", repr(session))
    aaa.require(fail_redirect='/login')
    return aaa.current_user.role


# Admin-only pages

@bottle.route('/admin')
@authorize(role="admin", fail_redirect='/sorry_page')
@bottle.view('admin_page')
def admin():
    """Only admin users can see this"""
    #aaa.require(role='admin', fail_redirect='/sorry_page')
    return dict(
        current_user = aaa.current_user,
        users = aaa.list_users(),
        roles = aaa.list_roles()
    )


@authorize(role="admin", fail_redirect='/sorry_page')
@bottle.post('/create_user')
def create_user():
    try:
        aaa.create_user(postd().username, postd().role, postd().password)
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_user')
@authorize(role="admin", fail_redirect='/sorry_page')
def delete_user():
    try:
        aaa.delete_user(post_get('username'))
        return dict(ok=True, msg='')
    except Exception as e:
        print (repr(e))
        return dict(ok=False, msg=e.message)


@bottle.post('/create_role')
@authorize(role="admin", fail_redirect='/sorry_page')
def create_role():
    try:
        aaa.create_role(post_get('role'), post_get('level'))
        return dict(ok=True, msg='')
    except Exception as e:
        return dict(ok=False, msg=e.message)


@bottle.post('/delete_role')
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
