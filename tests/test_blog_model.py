# -*- coding: utf-8 -*-
# Test of Blog Model
import unittest
from app import create_app, db
from app.models import User, Blog, Tag, Category
from app.exceptions import ParsingError


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

    # 测试 on_change_body 方法
    def test_on_changed_body(self):
        blog = Blog(title='origin', summary_text='origin',
                    summary='origin', html='<origin></origin>')
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

    # 测试文章解析错误
    def test_body_parsing_error(self):
        try:
            blog = Blog(body='wrong format')
            self.assertTrue(False)
        except ParsingError as e:
            self.assertTrue(str(e) == 'wrong when parsing input')
        try:
            blog = Blog(
                body='---wrong header---\n<summary>\n<!-- more -->\n<Content>')
            self.assertTrue(False)
        except ParsingError as e:
            self.assertTrue(str(e) == 'wrong when parsing header')
        try:
            blog = Blog(
                body='---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<Content>')
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)

    def test_change_tags(self):
        blog = Blog(
            body='---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n<Content>')
        blog2 = Blog(
            body='---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag5, tag3]\n---\n<summary>\n<!-- more -->\n<Content>')
        new_tags = [Tag(name=tagname) for tagname in ['tag5', 'tag3', 'tag4']]
        blog.change_tags(new_tags)
        self.assertTrue(blog.tags == new_tags)

    def test_change_category(self):
        blog = Blog(
            body='---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n<Content>')
        db.session.add(blog)
        db.session.commit()
        cat = blog.category
        blog.change_category(cat)
        self.assertTrue(blog.category_id == cat.id)
        self.assertFalse(blog.category.name == '<summary>')
        blog2 = Blog(
            body='---\ntitle: <title>\ncategory: <category2>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n<Content>')
        db.session.add(blog2)
        db.session.commit()
        cat2 = blog2.category
        blog.change_category(cat2)
        db.session.commit()
        self.assertTrue(Category.query.count() == 1)
        self.assertTrue(Category.query.first().name == '<category2>')
        cat = Category(name='new_cat')
        blog.change_category(cat)
        db.session.commit()
        self.assertTrue(Category.query.count() == 2)

    def test_delete_tags_and_category(self):
        blog = Blog(
            body='---\ntitle: <title>\ncategory: <new_cat>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n<Content>')
        blog2 = Blog(
            body='---\ntitle: <title>\ncategory: <category2>\ntags: [tag1, tag4, tag3]\n---\n<summary>\n<!-- more -->\n<Content>')
        blog3 = Blog(
            body='---\ntitle: <title>\ncategory: <category2>\ntags: [tag1, tag4, tag3]\n---\n<summary>\n<!-- more -->\n<Content>')
        blog.delete_tags()
        blog.delete_category()
        db.session.delete(blog)
        db.session.commit()
        self.assertTrue(Tag.query.count() == 3)
        self.assertTrue(Category.query.count() == 1)
        blog2.delete_category()
        db.session.commit()
        self.assertTrue(Category.query.count() == 1)

    def test_to_json(self):
        blog = Blog(
            body='---\ntitle: <title>\ncategory: <category>\ntags: [tag1, tag2, tag3]\n---\n<summary>\n<!-- more -->\n<Content>')
        u = User(email='mike@example.com', password='cat')
        blog.author = u
        db.session.add(u)
        db.session.add(blog)
        db.session.commit()
        json_blog = blog.to_json()
        expected_keys = ['url', 'id', 'title', 'summary_text',
                         'body', 'timestamp', 'draft', 'author', 'category', 'tags']
        self.assertEqual(sorted(json_blog.keys()), sorted(expected_keys))
        self.assertTrue('api/v1.0/blogs/' in json_blog['url'])

    def test_repr(self):
        blog = Blog(title='title')
        db.session.add(blog)
        db.session.commit()
        self.assertTrue(repr(Blog.query.first()) == "<Blog 'title'>")
