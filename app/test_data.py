import unittest
import os
from pymongo import MongoClient
from certifi import where
from os import getenv
from dotenv import load_dotenv
import pandas as pd
from pandas import DataFrame
from app.data import Database


class TestDatabase(unittest.TestCase):
    """Unit tests for the Database class """

    def setUp(self):
        """Set up the test environment"""
        load_dotenv()
        self.client = MongoClient(os.getenv("DB_URL"), tlsCAFile=where())
        self.db = self.client["test_monster_database"]
        self.collection = self.db["monsters"]
        self.collection.delete_many({})
        self.database = Database()
        self.database.db = self.db
        self.database.collection = self.collection

    def test_seed(self):
        """Test seeding the database with a specified number of monsters"""
        num_monsters = 1000
        seeded_monsters = self.database.seed(num_monsters)
        self.assertEqual(seeded_monsters, num_monsters)
        self.assertEqual(self.database.count(), num_monsters)

    def test_reset(self):
        """Test resetting the database"""
        self.database.seed(1000)
        self.assertTrue(self.database.reset())
        self.assertEqual(self.database.count(),0)

    def test_count(self):
        """Test the counting of the number of monsters in the database."""
        self.database.seed(1000)
        self.assertEqual(self.database.count(), 1000)

    def test_dataframe(self):
        """Test the retrieval of data is in a dataframe and the lenght of the
        dataframe is equal to 1000"""
        self.database.seed(1000)
        df = self.database.dataframe()
        self.assertIsInstance(df, DataFrame)
        self.assertEqual(len(df), 1000)

    def test_html_table(self):
        """Test it generates a html table"""
        self.database.seed(1000)
        html_table = self.database.html_table()
        self.assertIsNotNone(html_table)
        self.assertIn("<table", html_table)

if __name__ == "__main__":
    unittest.main()

