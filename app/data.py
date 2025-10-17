from os import getenv
from typing import Dict, Optional
from certifi import where
from dotenv import load_dotenv
from BloomtechMonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient
import pandas as pd



class Database:
    """ Interface for database operations."""

    def __init__(self):
        """Initializing the database connection"""
        load_dotenv()
        self.client = MongoClient(getenv("DB_URL"), tlsCAFile=where())
        self.db = self.client["monster_database"]
        self.collection = self.db["monsters"]

    def seed(self, num_monsters: int) -> bool:
        """Seed the database with specified number of monsters."""
        try:
            monsters = [generate_monster() for _ in range(num_monsters)]
            self.collection.insert_many(monsters)
            return True
        except Exception as e:
            print(f"Error seeding database: {e}")
            return False
        #pass

    def reset(self):
        """Delete all monsters from the collection."""
        try:
            self.collection.delete_many({})
            return True
        except Exception as e:
            print(f"Error resetting database: {e}")
            return False
        #pass

    def count(self) -> int:
        """Return the number of monsters in the collection."""
        return self.collection.count_documents({})
        #pass

    def dataframe(self) -> DataFrame:
        """Return a DataFrame of all monsters in the collection."""
        data = list(self.collection.find({}, {'_id': 0}))
        return pd.DataFrame(data) if data else None
        #pass

    def html_table(self) -> str:
        """Return HTML table representation of monster data."""
        df = self.dataframe()
        return df.to_html() if df is not None else None
        #pass
