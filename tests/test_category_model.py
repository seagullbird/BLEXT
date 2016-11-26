# -*- coding: utf-8 -*-
# Test of Category Model
import unittest
from app import create_app, db
from app.models import Category, User


class CategoryModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_generate_category(self):
        u = User(email='mike@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        cat_name1 = ''
        cat_name2 = 'test_cat'
        cat1 = Category.generate_category(cat_name1, u.id)
        cat2 = Category.generate_category(cat_name2, u.id)
        self.assertTrue(cat_name1 == cat1.name)
        self.assertTrue(cat_name2 == cat2.name)

    def test_to_json(self):
        cat = Category(name='cat')
        db.session.add(cat)
        db.session.commit()
        json_cat = cat.to_json()
        self.assertTrue('cat' == json_cat['name'])

    def test_repr(self):
        cat = Category(name='cat')
        db.session.add(cat)
        db.session.commit()
        self.assertTrue(repr(Category.query.first()) == "<Category 'cat'>")
