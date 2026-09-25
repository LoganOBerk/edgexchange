from .environment import Environment as env
from interface_layer import Cli, Frontend
from sanitization_layer import Sanitizer
from validation_layer import Validator
from service_layer import Service
from persistence_layer import Database


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
    #	-testing; is True or False
    #	-frontend; is True or False
    # POSTCONDITION:
    #   -self.san; Sanitizer constructed
    #	-self.db; Database constructed with db source
    #	-self.serv; Service constructed with self.db injection
    #	-self.val; Validator constructed with self.serv injection
    #	-frontend=True; self.display is Frontend with serv, san, val injection
    #	-frontend=False; self.display is Cli with serv, san, val injection
    # RAISES: None
    def init(self, frontend : bool) -> None:

        self.db = Database(env.get_database_source())
        self.serv = Service(self.db)
        self.val = Validator(self.serv)
        self.san = Sanitizer()

        if frontend:
            self.display = Frontend(self.serv, self.san, self.val)
        else:
            self.display = Cli(self.serv, self.san, self.val)



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
   