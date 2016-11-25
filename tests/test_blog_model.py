# Test of Blog Model
import unittest
from app import create_app, db
from app.models import User, Blog, Tag, Category


class BlogModelTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_on_changed_body(self):
		blog = Blog(title='origin', summary_text='origin', summary='origin', html='<origin></origin>')
		origin_title = blog.title
		origin_summary_text = blog.summary_text
		origin_summary = blog.summary
		origin_html = blog.html
		origin_category_id = blog.category_id
		origin_tags = blog.tags

		blog.body = '---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n<Content>'
		db.session.add(blog)
		db.session.commit()
		self.assertTrue(origin_title != blog.title)
		self.assertTrue(origin_summary_text != blog.summary_text)
		self.assertTrue(origin_summary != blog.summary)
		self.assertTrue(origin_html != blog.html)
		self.assertTrue(origin_tags != blog.tags)
		self.assertTrue(origin_category_id != blog.category_id)

	def test_change_tags(self):
		blog = Blog(body='---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n<Content>')
		new_tags = [Tag(name=tagname) for tagname in ['tag2', 'tag3', 'tag4']]
		blog.change_tags(new_tags)
		self.assertTrue(blog.tags == new_tags)

	def test_change_category(self):
		blog = Blog(body='---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n<Content>')
		new_cat = Category(name='new_cat')
		blog.change_category(new_cat)
		db.session.add(new_cat)
		db.session.add(blog)
		db.session.commit()
		self.assertTrue(blog.category_id == new_cat.id)
		self.assertFalse(blog.category.name == '<summary>')

	def test_delete_tags(self):
		blog = Blog(body='---\ntitle: <title>\ncategory: <new_cat>\ntags: [nt1, nt2, nt3]\n---\n<summary>\n<!-- more -->\n<Content>')
		db.session.add(blog)
		db.session.commit()
		blog.delete_tags()
		db.session.delete(blog)
		db.session.commit()
		self.assertFalse(Blog.query.all())
		self.assertFalse(Tag.query.all())

	def test_delete_category(self):
		blog = Blog(body='---\ntitle: <title>\ncategory: <new_cat>\ntags: [nt1, nt2, nt3]\n---\n<summary>\n<!-- more -->\n<Content>')
		db.session.add(blog)
		db.session.commit()
		blog.delete_category()
		db.session.delete(blog)
		db.session.commit()
		self.assertFalse(Blog.query.all())
		self.assertFalse(Category.query.all())

	def test_to_json(self):
		blog = Blog(body='---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n<Content>')
		u = User(email='mike@example.com', password='cat')
		blog.author = u
		db.session.add(u)
		db.session.add(blog)
		db.session.commit()
		json_blog = blog.to_json()
		expected_keys = ['url', 'id', 'title', 'summary_text', 'body', 'timestamp', 'draft', 'author', 'category', 'tags']
		self.assertEqual(sorted(json_blog.keys()), sorted(expected_keys))
		self.assertTrue('api/v1.0/blogs/' in json_blog['url'])
