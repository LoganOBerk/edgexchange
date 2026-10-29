from .linker import Database, Cache, Config
from presentation import Cli, Frontend
from interface import Api
from sanitization import Sanitizer
from validation import Validator
from orchestration import Service


# PURPOSE:
#	-App provides initialization abstraction
#	-Allows for clean dependency injection and easy swaps between display types
class App:
    
    # INPUT:
    #	-frontend(bool); whether to run FastAPI frontend or CLI
    # OUTPUT: None
    # PRECONDITION:
    #	-frontend; is True or False
    # POSTCONDITION:
    #   -every key layer object is constructed with proper dependancy injection with Frontend or Cli being conditionally constructed
    # RAISES: None
    def __init__(self, frontend=True):
        db, ch, cfg = Database(), Cache(), Config()

        serv = Service(db.acc, ch.lc)
        val = Validator(serv)
        san = Sanitizer()
        api = Api(serv,san,val)

        if frontend:
            self.display = Frontend(api, ch.sc, cfg.ao)
        else:
            self.display = Cli(api)

    
    # INPUT: None
    # OUTPUT: None
    # PRECONDITION:
    #	-self.display; initialized via init()
    # POSTCONDITION:
    #	-frontend=True; uvicorn serves app on 0.0.0.0:8000
    #	-frontend=False; Cli drives execution on terminal
    # RAISES: None
    def run(self) -> None:
        self.display.execute()
   