import os
from dotenv import load_dotenv

load_dotenv()

class Environment:

    @staticmethod
    def ao_cfg():
        return os.getenv("ORIGINS").split(",")
    
    @staticmethod
    def lc_src():
        return os.getenv("LCSOURCE")
    
    @staticmethod
    def sc_src():
        return os.getenv("SCSOURCE")
    
    @staticmethod
    def pd_src():
        return os.getenv("PDSOURCE")