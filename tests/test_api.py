# -*- coding: utf-8 -*-
import unittest
import json
from base64 import b64encode
from flask import url_for
from app import create_app, db
from app.models import User, Blog


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_404(self):
        response = self.client.get(
            '/wrong/url', headers=self.get_api_headers('email', 'password'))
        self.assertTrue(response.status_code == 404)

    def test_no_auth(self):
        response = self.client.get(url_for('api.get_blogs'),
                                   content_type='application/json')
        self.assertTrue(response.status_code == 401)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'unauthorized')

    def test_bad_auth(self):
        # add a user
        u = User(email='mike@example.com', password='cat', confirmed=True)
        db.session.add(u)
        db.session.commit()

        # authenticate with bad password
        response = self.client.get(
            url_for('api.get_blogs'),
            headers=self.get_api_headers('mike@example.com', 'dog'))
        self.assertTrue(response.status_code == 401)

    def test_token_auth(self):
        # add a user
        u = User(email='mike@example.com', password='cat', confirmed=True)
        db.session.add(u)
        db.session.commit()

        # issue a request with a bad token
        response = self.client.get(
            url_for('api.get_blogs'),
            headers=self.get_api_headers('bad-token', ''))
        self.assertTrue(response.status_code == 401)

        # get a token
        response = self.client.get(
            url_for('api.get_token'),
            headers=self.get_api_headers('mike@example.com', 'cat'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        # issue a request with the token
        response = self.client.get(
            url_for('api.get_blogs'),
            headers=self.get_api_headers(token, ''))
        self.assertTrue(response.status_code == 200)

        # get a token again (before expriration)
        response = self.client.get(
            url_for('api.get_token'),
            headers=self.get_api_headers(token, ''))
        self.assertTrue(response.status_code == 401)

    def test_unconfirmed_account(self):
        # add an unconfirmed user
        u = User(email='mike@example.com', password='cat', confirmed=False)
        db.session.add(u)
        db.session.commit()

        # get list of blogs with the unconfirmed account
        response = self.client.get(
            url_for('api.get_blogs'),
            headers=self.get_api_headers('mike@example.com', 'cat'))
        self.assertTrue(response.status_code == 403)

    def test_blogs(self):
        # add a user
        u = User(email='mike@example.com', password='cat', confirmed=True)
        db.session.add(u)
        db.session.commit()

        # write an empty blog
        response = self.client.post(
            url_for('api.new_blog'),
            headers=self.get_api_headers('mike@example.com', 'cat'),
            data=json.dumps({'body': ''}))
        self.assertTrue(response.status_code == 400)

        # write a wrong format blog
        response = self.client.post(
            url_for('api.new_blog'),
            headers=self.get_api_headers('mike@example.com', 'cat'),
            data=json.dumps({'body': 'wrong format.', 'draft': 'false'}))
        self.assertTrue(response.status_code == 400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response[
                        'message'] == 'There is something wrong in your format. Committing abolished.')

        # write a blog without 'draft' value
        response = self.client.post(
            url_for('api.new_blog'),
            headers=self.get_api_headers('mike@example.com', 'cat'),
            data=json.dumps({'body': 'wrong format.'}))
        self.assertTrue(response.status_code == 400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response[
                        'message'] == 'blog does not have a draft value')

        # write a blog
        response = self.client.post(
            url_for('api.new_blog'),
            headers=self.get_api_headers('mike@example.com', 'cat'),
            data=json.dumps({'body': '---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n**markdown** Content.', 'draft': 'false'}))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        # get the new blog
        response = self.client.get(
            url,
            headers=self.get_api_headers('mike@example.com', 'cat'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['url'] == url)
        self.assertTrue(json_response[
                        'body'] == '---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n**markdown** Content.')

        # get the new blog's category
        blog_id = json_response.get('id')
        new_blog = Blog.query.filter_by(id=blog_id).first()
        self.assertIsNotNone(blog_id)
        response = self.client.get(url_for('api.get_blog_category', blog_id=blog_id),
                                   headers=self.get_api_headers('mike@example.com', 'cat'))
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('name'))
        self.assertTrue(json_response['name'] == new_blog.category.name)

        # get the new blog's tags
        response = self.client.get(url_for('api.get_blog_tags', blog_id=blog_id),
                                   headers=self.get_api_headers('mike@example.com', 'cat'))
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('tags'))
        self.assertEqual(
            sorted([tag.name for tag in new_blog.tags]), sorted([tag['name'] for tag in json_response['tags']]))

        # edit blog
        response = self.client.put(
            url,
            headers=self.get_api_headers('mike@example.com', 'cat'),
            data=json.dumps({'body': '---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n**Updated markdown** Content.', 'draft': 'false'}))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['url'] == url)
        self.assertTrue(json_response[
                        'body'] == '---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n**Updated markdown** Content.')

        # edit wrong format draft
        response = self.client.put(
            url,
            headers=self.get_api_headers('mike@example.com', 'cat'),
            data=json.dumps({'body': 'wrong format', 'draft': 'true'}))
        self.assertTrue(response.status_code == 400)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response[
                        'message'] == 'There is something wrong in your format. Committing abolished.')

    def test_user(self):
        # add a user
        u = User(email='mike@example.com', password='cat', confirmed=True)
        db.session.add(u)
        db.session.commit()

        # get user information
        response = self.client.get(url_for(
            'api.get_user'), headers=self.get_api_headers('mike@example.com', 'cat'))
        json_response = json.loads(response.data.decode('utf-8'))
        expected_keys = ['url', 'username', 'blogs',
                         'categories', 'tags', 'avatar_url', 'blog_count']
        self.assertEqual(sorted(expected_keys), sorted(json_response.keys()))
        self.assertTrue('/user/' in json_response['url'])

        # get user categories
        response = self.client.get(url_for(
            'api.get_user_categories'), headers=self.get_api_headers('mike@example.com', 'cat'))
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('categories'))

        # get user tags
        response = self.client.get(url_for(
            'api.get_user_tags'), headers=self.get_api_headers('mike@example.com', 'cat'))
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(json_response.get('tags'))
