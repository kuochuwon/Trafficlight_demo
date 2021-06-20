import unittest
import re

from flask import current_app
from flask_testing import TestCase

from manage import app


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
        db_pattern = "^(postgresql\\+psycopg2).*(/sd_db_test)$"
        self.assertFalse(current_app is None)
        self.assertTrue(bool(re.match(db_pattern, app.config["SQLALCHEMY_DATABASE_URI"])))
        self.assertFalse(app.config["DEBUG"])
        self.assertTrue(app.config["TESTING"])


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object("app.main.config.ProductionConfig")
        return app

    def test_app_is_production(self):
        db_pattern = "^(postgresql\\+psycopg2).*(/sd_db)$"
        self.assertFalse(current_app is None)
        self.assertTrue(bool(re.match(db_pattern, app.config["SQLALCHEMY_DATABASE_URI"])))
        self.assertFalse(app.config["DEBUG"])
        self.assertFalse(app.config["TESTING"])


if __name__ == "__main__":
    unittest.main()
