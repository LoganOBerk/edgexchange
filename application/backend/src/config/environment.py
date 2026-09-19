import os
from dotenv import load_dotenv

load_dotenv()

class Environment:

    @staticmethod
    def get_database_source():
        return os.getenv("DATABASE_SOURCE")

    @staticmethod
    def get_database_test_source():
        return os.getenv("DATABASE_TEST_SOURCE")