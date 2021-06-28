import unittest
import re

from flask import current_app
from flask_testing import TestCase

from manage import app

# TODO 此處的RE要搞清楚


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object("app.main.config.DevelopmentConfig")
        return app

    def test_app_is_development(self):
        db_pattern = "^(postgresql\\+psycopg2).*(/sd_db_dev)$"
        self.assertFalse(current_app is None)
        self.assertTrue(bool(re.match(db_pattern, app.config["SQLALCHEMY_DATABASE_URI"])))
        self.assertTrue(app.config["DEBUG"])
        self.assertFalse(app.config["TESTING"])


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object("app.main.config.TestingConfig")
        return app

    def test_app_is_testing(self):
        db_pattern = "^(postgresql\\+psycopg2).*(/Unittest)$"
        print(db_pattern)
        print(app.config["SQLALCHEMY_DATABASE_URI"])
        self.assertFalse(current_app is None)
        self.assertTrue(bool(re.match(db_pattern, app.config["SQLALCHEMY_DATABASE_URI"])))
        self.assertFalse(app.config["DEBUG"])
        self.assertTrue(app.config["TESTING"])


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object("app.main.config.HerokuConfig")
        return app

    def test_app_is_heroku_production(self):
        # db_pattern = "^(postgres\\).*(/*compute-1.amazonaws.com)$"
        db_pattern = "^(postgres).*(/ddn25333pg00bp)$"
        print(db_pattern)
        print(app.config["SQLALCHEMY_DATABASE_URI"])
        self.assertFalse(current_app is None)
        self.assertTrue(bool(re.match(db_pattern, app.config["SQLALCHEMY_DATABASE_URI"])))
        self.assertFalse(app.config["DEBUG"])
        self.assertFalse(app.config["TESTING"])


if __name__ == "__main__":
    unittest.main()
