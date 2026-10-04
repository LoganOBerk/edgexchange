import os
from dotenv import load_dotenv

load_dotenv()

class Environment:

    @staticmethod
    def ao_cfg():
        return os.getenv("ALLOWED_ORIGINS").split(",")
    
    @staticmethod
    def lc_src():
        return os.getenv("LIVE_CACHE_SOURCE")
    
    @staticmethod
    def sc_src():
        return os.getenv("SESSION_CACHE_SOURCE")
    
    @staticmethod
    def db_src():
        return os.getenv("DATABASE_SOURCE")

    @staticmethod
    def db_tsrc():
        return os.getenv("DATABASE_TEST_SOURCE")