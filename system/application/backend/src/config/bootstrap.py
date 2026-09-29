from .environment import Environment as env
from presentation import Cli, Frontend
from interface import Api
from sanitization import Sanitizer
from validation import Validator
from orchestration import Service
from persistence import Database


# PURPOSE:
#	-App provides initialization abstraction
#	-Allows for clean dependency injection and easy swaps between display types
class App:
    def __init__(self, frontend=True):
        self.init(frontend)


    # INPUT:
    #	-frontend(bool); whether to run FastAPI frontend or CLI
    # OUTPUT: None
    # PRECONDITION:
    #	-frontend; is True or False
    # POSTCONDITION:
    #   -every key layer object is constructed with proper dependancy injection with Frontend or Cli being conditionally constructed
    # RAISES: None
    def init(self, frontend : bool) -> None:

        self.db = Database(env.get_database_source())
        self.serv = Service(self.db)
        self.val = Validator(self.serv)
        self.san = Sanitizer()
        self.api = Api(self.serv, self.san, self.val)

        if frontend:
            self.display = Frontend(self.api)
        else:
            self.display = Cli(self.api)



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
   