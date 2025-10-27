import os
from typing import Dict, Optional
from certifi import where
from dotenv import load_dotenv
from BloomtechMonsterLab import Monster, MonsterLab, monster_lab, random_generator
from pandas import DataFrame
from pymongo import MongoClient
import pandas as pd
load_dotenv()


class Database:
    """ Interface for database operations."""

    def __init__(self):
        """Initializing the database connection"""
        self.client = MongoClient(os.getenv("DB_URL"), tlsCAFile=where())
        self.db = self.client["monster_database"]
        self.collection = self.db["monsters"]

    def seed(self, num_monsters: int) -> int:
        """Seed the database with specified number of monsters 
        
        Args: 
            num_monsters (int) = Number of monsters to insert
            
        Returns: 
            int: Number of monsters successfully seeded
        """
        try:
            monsters = [random_generator.RandomGenerator() for _ in range(num_monsters)]
            monster_dicts = [m.__dict__ for m in monsters]
            self.collection.insert_many(monster_dicts)
            return num_monsters
        except Exception:
            return 0

    def reset(self):
        """Delete all monsters from the collection.
        
        Returns:
            bool: True if deletion succeeded, otherwise False
        """
        try:
            self.collection.delete_many({})
            return True
        except Exception:
            return False

    def count(self) -> int:
        """Count the number of monsters in the collection.
        
        Returns:
            int: Number of monsters
        """
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        """Return a Pandas DataFrame of all monsters in the collection.
        
        Returns:
            Dataframe of monster data or None if empty
        """
        data = list(self.collection.find({}, {'_id': 0}))
        return pd.DataFrame(data) if data else None

    def html_table(self) -> str:
        """Return HTML table representation of monster data.
        
        Returns:
            HTML table string or None if empty
        """
        df = self.dataframe()
        return df.to_html() if df is not None else None
