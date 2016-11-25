# Test of Tag Model
import unittest
from app import create_app, db
from app.models import Tag, User

class TagModelTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_generate_tags(self):
		u = User(email='mike@example.com', password='cat')
		db.session.add(u)
		db.session.commit()
		tag_names1 = []
		tag_names2 = ['tag']
		tag_names3 = ['tag1', 'tag2', 'tag3']
		tags1 = Tag.generate_tags(tag_names1, u.id)
		tags2 = Tag.generate_tags(tag_names2, u.id)
		tags3 = Tag.generate_tags(tag_names3, u.id)
		self.assertEqual(sorted([tag.name for tag in tags1]), sorted(tag_names1))		
		self.assertEqual(sorted([tag.name for tag in tags2]), sorted(tag_names2))		
		self.assertEqual(sorted([tag.name for tag in tags3]), sorted(tag_names3))