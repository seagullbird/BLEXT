import re
from app.models import User
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
	def test_register_and_confirm(self):
		# register a new account
		response = self.client.post(url_for('auth.sign_up'), data={
			'email': 'mike@example.com',
			'username': 'mike',
			'password': 'cat',
			'password2': 'cat'
			}, follow_redirects=True)
		self.assertTrue(re.search(b'Hello,\s+mike!', response.data))
		self.assertTrue(b'You have not confirmed your account yet' in response.data)

		# send a confirmation token
		user = User.query.filter_by(email='mike@example.com').first()
		token = user.generate_confirmation_token()
		response = self.client.get(url_for('auth.confirm', token=token), follow_redirects=True)
		self.assertTrue(b'You have confirmed your account' in response.data)

		# sign out
		response = self.client.get(url_for('auth.sign_out'), follow_redirects=True)
		self.assertTrue(b'You have been signed out' in response.data)

		# re sign up with same email and username
		response = self.client.post(url_for('auth.sign_up'), data={
			'email': 'mike@example.com',
			'username': 'mike',
			'password': 'cat',
			'password2': 'cat'
			}, follow_redirects=True)
		self.assertFalse(re.search(b'Hello,\s+mike!', response.data))
		self.assertFalse(b'You have not confirmed your account yet' in response.data)

		# sign in
		response = self.client.post(url_for('auth.sign_in'), data={
			'email': 'mike@example.com',
			'password': 'cat'
			})
		self.assertTrue(response.status_code == 302)
