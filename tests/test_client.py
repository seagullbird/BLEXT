# -*- coding: utf-8 -*-
import re
from app.models import User, Blog, Category
import time
from app import db, create_app
import unittest
from flask import url_for


class FlaskClientTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # self.client是Flask测试客户端对象
        # 在这个对象上可调用方法向程序发起请求
        # use_cookies: 使用依赖cookie的功能记住请求之间的上下文
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # 测试主页请求
    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue(b'Welcome to BLEXT' in response.data)

    # 测试新用户注册和登录
    def test_authentication(self):
        # register a new account
        response = self.client.post(url_for('auth.sign_up'), data={
            'email': 'mike@example.com',
            'username': 'mike',
            'password': 'cat',
            'password2': 'cat'
        }, follow_redirects=True)
        self.assertTrue(re.search(b'Hello,\s+mike!', response.data))
        self.assertTrue(
            b'You have not confirmed your account yet' in response.data)

        # issue a random request
        response = self.client.get(url_for('settings.profile_setting'))
        self.assertTrue(response.status_code == 302)

        # send a confirmation token
        user = User.query.filter_by(email='mike@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(
            url_for('auth.confirm', token=token), follow_redirects=True)
        self.assertTrue(b'You have confirmed your account' in response.data)

        # resend a confirmation token
        response = self.client.get(url_for('auth.resend_confirmation'))
        self.assertTrue(response.status_code == 302)

        # sign out
        response = self.client.get(
            url_for('auth.sign_out'), follow_redirects=True)
        self.assertTrue(b'You have been signed out' in response.data)

        # reset password request
        response = self.client.post(url_for('auth.password_reset_request'), data={
            'email': 'mike@example.com'
        })
        self.assertTrue(response.status_code == 302)

        # reset password
        response = self.client.post(
            url_for('auth.password_reset', token=user.generate_reset_token()), data={
                'email': 'mike@example.com',
                'password': 'dog',
                'password2': 'dog'
            }, follow_redirects=True)

        self.assertTrue(b'Sign In' in response.data)

        # re sign up with same email and username
        response = self.client.post(url_for('auth.sign_up'), data={
            'email': 'mike@example.com',
            'username': 'mike',
            'password': 'cat',
            'password2': 'cat'
        }, follow_redirects=True)
        self.assertFalse(re.search(b'Hello,\s+mike!', response.data))
        self.assertFalse(
            b'You have not confirmed your account yet' in response.data)

        # sign in
        response = self.client.post(url_for('auth.sign_in'), data={
            'email': 'mike@example.com',
            'password': 'dog'
        })
        self.assertTrue(response.status_code == 302)

        # re visit unconfirmed
        response = self.client.get(url_for('auth.unconfirmed'))
        self.assertTrue(response.status_code == 302)

    # 测试用户设置页
    def test_settings(self):
        # add a user
        u = User(email='mike@example.com', username='mike',
                 password='cat', confirmed=True)
        db.session.add(u)
        db.session.commit()

        # sign in
        response = self.client.post(url_for('auth.sign_in'), data={
            'email': 'mike@example.com',
            'password': 'cat'
        })
        self.assertTrue(response.status_code == 302)

        # setting profile
        response = self.client.get(url_for('settings.profile_setting'))
        self.assertTrue(response.status_code == 200)

        # set bio
        response = self.client.post(url_for('settings.profile_setting'), data={
            'bio': 'new bio'
        }, follow_redirects=True)
        self.assertTrue(b'new bio' in response.data)

        # set avatar_url
        response = self.client.post(url_for('settings.profile_setting'), data={
            'avatar_url': 'new avatar_url'
        }, follow_redirects=True)
        self.assertTrue(b'new avatar_url' in response.data)

        # set blog_title
        response = self.client.post(url_for('settings.profile_setting'), data={
            'blog_title': 'new blog_title'
        }, follow_redirects=True)
        self.assertTrue(b'new blog_title' in response.data)

        # set about_me
        response = self.client.post(url_for('settings.profile_setting'), data={
            'about_me': 'new about_me'
        })
        self.assertTrue(response.status_code == 302)
        response = self.client.get(url_for('user.about_me', username='mike'))
        self.assertTrue(b'new about_me' in response.data)

        # setting admin
        response = self.client.get(url_for('settings.admin_setting'))
        self.assertTrue(response.status_code == 200)

        # change password with wrong old password
        response = self.client.post(url_for('settings.admin_setting'), data={
            'old_password': 'dog',
            'password': 'cat',
            'password2': 'cat'
        }, follow_redirects=True)
        self.assertTrue(b'Invalid password' in response.data)

        # change password with correct old password
        response = self.client.post(url_for('settings.admin_setting'), data={
            'old_password': 'cat',
            'password': 'dog',
            'password2': 'dog'
        }, follow_redirects=True)
        self.assertTrue(b'Welcome to BLEXT' in response.data)

    # 测试编辑器页
    def test_editor(self):
        response = self.client.get(url_for('editor.index'))
        self.assertTrue(response.status_code == 404)

        # add a user
        u = User(email='mike@example.com', username='mike',
                 password='cat', confirmed=True)
        db.session.add(u)
        db.session.commit()

        # sign in
        response = self.client.post(url_for('auth.sign_in'), data={
            'email': 'mike@example.com',
            'password': 'cat'
        })
        self.assertTrue(response.status_code == 302)

        response = self.client.get(url_for('editor.index'))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(b'EDITOR' in response.data)

        # write a new draft blog
        blog_body = '---\ntitle: <title>\ncategory: <category>\ntags: []\n---\n<summary>\n<!-- more -->\n<Content>'
        response = self.client.post(url_for('editor.index'), data={
            'plainText': blog_body,
            'draft': 'true'
        }, follow_redirects=True)
        self.assertTrue(
            b'Your blog is successfully saved as a draft.' in response.data)

        # publish a new blog
        blog_body = '---\ntitle: <title>\ncategory: <category>\ntags: []\n---\n<summary>\n<!-- more -->\n<Content>'
        response = self.client.post(url_for('editor.index'), data={
            'plainText': blog_body,
            'draft': 'false'
        }, follow_redirects=True)
        self.assertTrue(
            b'Your blog is successfully uploaded!' in response.data)

        # edit an existing blog
        response = self.client.get(url_for('editor.edit', blog_id=1))
        self.assertTrue(response.status_code == 302)
        response = self.client.get(url_for('editor.index'))
        self.assertTrue(b'1' in response.data)
        blog_body += 'something new'
        response = self.client.post(url_for('editor.index'), data={
            'plainText': blog_body,
            'draft': 'false',
            'blog_id': '1'
        }, follow_redirects=True)
        self.assertTrue(
            b'Your blog is successfully uploaded!' in response.data)
        self.assertTrue(Blog.query.count() == 2)

        # publish a wrong format blog
        blog_body = 'wrong format'
        response = self.client.post(url_for('editor.index'), data={
            'plainText': blog_body,
            'draft': 'false'
        })
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            b'There is something wrong in your format. Committing abolished' in response.data)

        # edit a wrong format blog
        blog_body = 'wrong format'
        response = self.client.post(url_for('editor.index'), data={
            'plainText': blog_body,
            'draft': 'false',
            'blog_id': '1'
        })
        self.assertTrue(response.status_code == 200)
        self.assertTrue(
            b'There is something wrong in your format. Committing abolished' in response.data)

    # 测试用户主页
    def test_user(self):
        # add two users, two draft blogs, two categories and two tags
        u = User(email='mike@example.com', username='mike',
                 password='cat', confirmed=True)
        u2 = User(email='jack@example.com', username='jack',
                  password='dog', confirmed=True)
        db.session.add_all([u, u2])
        db.session.commit()
        blog = Blog(
            body='---\ntitle: <title1>\ncategory: cat1\ntags: [tag1]\n---\n<summary>\n<!-- more -->\n<Content>', author_id=u.id, draft=True)
        blog2 = Blog(
            body='---\ntitle: <title2>\ncategory: cat2\ntags: [tag2]\n---\n<summary>\n<!-- more -->\n<Content>', author_id=u2.id, draft=True)
        db.session.add_all([blog, blog2])
        db.session.commit()

        # for cat in Category.query.all():
        #     print(cat.author)
        # # wait for committing
        # time.sleep(2)

        # get index
        response = self.client.get(url_for('user.index', username='mike'))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(b'mike' in response.data)

        # categories page
        response = self.client.get(url_for('user.categories', username='mike'))
        self.assertTrue(response.status_code == 200)
        response = self.client.get(url_for('user.categories', username='tom'))
        self.assertTrue(response.status_code == 404)

        # tags page
        response = self.client.get(url_for('user.tags', username='mike'))
        self.assertTrue(response.status_code == 200)
        response = self.client.get(url_for('user.tags', username='tom'))
        self.assertTrue(response.status_code == 404)

        # single cat list (anonymous)
        response = self.client.get(
            url_for('user.category', username='mike', category_name='cat1'))
        self.assertTrue(response.status_code == 200)
        self.assertFalse(b'title1' in response.data)
        self.assertFalse(b'title2' in response.data)

        # single tag list (anonymous)
        response = self.client.get(
            url_for('user.tag', username='mike', tag_name='tag1'))
        self.assertTrue(response.status_code == 200)
        self.assertFalse(b'title1' in response.data)
        self.assertFalse(b'title2' in response.data)

        # sign in
        response = self.client.post(url_for('auth.sign_in'), data={
            'email': 'mike@example.com',
            'password': 'cat'
        })
        self.assertTrue(response.status_code == 302)

        # single cat list (signed in)
        response = self.client.get(
            url_for('user.category', username='mike', category_name='cat1'))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(b'title1' in response.data)
        self.assertFalse(b'title2' in response.data)

        # single tag list (signed in)
        response = self.client.get(
            url_for('user.tag', username='mike', tag_name='tag1'))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(b'title1' in response.data)
        self.assertFalse(b'title2' in response.data)

        # visit own drafts
        response = self.client.get(url_for('user.drafts', username='mike'))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(b'title1' in response.data)

        # visit others drafts
        response = self.client.get(url_for('user.drafts', username='jack'))
        self.assertTrue(response.status_code == 404)

        # visit existing blog
        response = self.client.get(
            url_for('user.blog_page', username='mike', blog_id=1))
        self.assertTrue(response.status_code == 200)

        # visit unexisting blog
        response = self.client.get(
            url_for('user.blog_page', username='mike', blog_id=10))
        self.assertTrue(response.status_code == 404)

        # visit other's draft
        response = self.client.get(
            url_for('user.blog_page', username='jack', blog_id=2))
        self.assertTrue(response.status_code == 404)

        # delete ohter's blog
        response = self.client.get(
            url_for('user.delete_blog', blog_id=2))
        self.assertTrue(response.status_code == 404)

        # delete own blog
        response = self.client.get(
            url_for('user.delete_blog', blog_id=1))
        self.assertTrue(response.status_code == 302)

        # visit unexisting about me page
        response = self.client.get(
            url_for('user.about_me', username='dsfg'))
        self.assertTrue(response.status_code == 404)
