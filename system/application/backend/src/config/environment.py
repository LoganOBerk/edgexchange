import os
from dotenv import load_dotenv

load_dotenv()

class Environment:

    @staticmethod
    def db_src():
        return os.getenv("DATABASE_SOURCE")

    @staticmethod
    def db_tsrc():
        return os.getenv("DATABASE_TEST_SOURCE")