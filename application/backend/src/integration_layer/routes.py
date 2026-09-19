from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from .sessioncache import SessionCache as scac
from common.errors import ServiceError, ValidationError, SessionCacheError
from .pydantic_models.requests import LogoutRequest, CredsRequest, FundsRequest, PortfolioRequest, TransactionRequest
from .pydantic_models.responses import UserData, PortfolioData


api = None
router = APIRouter()

# INPUT:
#   -interface(Api); functional interface
# OUTPUT: None
# PRECONDITION:
#   -interface; fully constructed Api instance
# POSTCONDITION:
#   -api; passed interface is assigned to global module memory
# RAISES: None
def connect(interface) -> None:
    global api
    api = interface


# INPUT:
#   -req(CredsRequest); HTTP credential payload
# OUTPUT:
#   -response(dict[str,str]); success confirmation sent to client
# PRECONDITION:
#   -router; exists as a valid router
#   -api; contains control flow pipeline methods
# POSTCONDITION:
#   -api; see Api.create_account() POSTCONDITION
#   -response; contains key "message" with value "account created"
# RAISES:
#   -HTTPException(400); a ValidationError is raised, malformed credentials
#   -HTTPException(500); a ServiceError is raised, server side error
@router.post("/register", status_code = 201)
def register(req : CredsRequest) -> dict[str, str]:

    creds = (req.username, req.password)

    try:
    
        api.create_account(creds)
        
    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))

    except ServiceError as e:
        raise HTTPException(status_code = 500, detail = str(e))

    response = {"message" : "account created"}

    return response


# INPUT:
#   -req(CredsRequest); HTTP credential payload
# OUTPUT:
#   -response(dict[str,str|UserData]); session id and user data sent to client
# PRECONDITION:
#   -router; exists as a valid router
#   -api; contains control flow pipeline methods
# POSTCONDITION:
#   -api; see Api.find_account() POSTCONDITION
#   -active_sessions; see start_session() POSTCONDITION
#   -response; contains session_id and UserData for authenticated user
# RAISES:
#   -HTTPException(400); a ValidationError is raised, malformed credentials
#   -HTTPException(401); a ServiceError is raised, account not found
@router.post("/login", status_code = 200)
def login(req : CredsRequest) -> dict[str, str | UserData]:

    creds = (req.username, req.password)

    try:

        user = api.find_account(creds)

        if scac.cached(user.id):
            user = scac.find_active_user(user.id) 
        

    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))

    except ServiceError as e:
        raise HTTPException(status_code = 401, detail = str(e))

    session_id = scac.start_session(user)
    
    response = {"session_id" : session_id, "user" : UserData.convert(user)}

    return response


# INPUT:
#   -req(LogoutRequest); HTTP logout payload
# OUTPUT:
#   -response(dict[str,str]); success confirmation sent to client
# PRECONDITION:
#   -router; exists as a valid router
#   -active_sessions; contains all active sessions
# POSTCONDITION:
#   -active_sessions; matching session id from payload is removed
#   -active_users; user removed if no remaining sessions exist
# RAISES:
#   -HTTPException(404); session id is not found in active sessions
@router.post("/logout")
def logout(req : LogoutRequest) -> dict[str, str]:

    try:

        scac.terminate_session(req.session_id)

    except SessionCacheError as e:
        raise HTTPException(status_code = 401, detail = str(e))
    
    response = {"message" : "logged out"}

    return response


# INPUT:
#   -req(FundsRequest); HTTP funds to add payload
# OUTPUT:
#   -response(dict[str,UserData]); user data JSON payload
# PRECONDITION:
#   -router; exists as a valid router
#   -api; contains control flow pipeline methods
# POSTCONDITION:
#   -api; see Api.fund_account() POSTCONDITION
#   -response; contains updated UserData
# RAISES:
#   -HTTPException(400); a ValidationError is raised, invalid funds request
#   -HTTPException(401); unauthorized, user session does not exist
#   -HTTPException(500); a ServiceError is raised, server side error
@router.post("/fund")
def fund(req : FundsRequest) -> dict[str, UserData]:
    try:

        user = scac.find_sessions_user(req.session_id)

        with user.lock:
            api.fund_account(user, req.funds_requested)
            response = {"user" : UserData.convert(user)}

    except SessionCacheError as e:
        raise HTTPException(status_code = 401, detail = str(e))
    
    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))

    except ServiceError as e:
        raise HTTPException(status_code = 500, detail = str(e))

    return response


# INPUT:
#   -req(PortfolioRequest); HTTP portfolio creation payload
# OUTPUT:
#   -response(dict[str,UserData]); user data JSON payload 
# PRECONDITION:
#   -router; exists as a valid router
#   -api; contains control flow pipeline methods 
# POSTCONDITION:
#   -api; see Api.create_portfolio() POSTCONDITION
#   -response; contains updated UserData
# RAISES:
#   -HTTPException(400); a ValidationError is raised, invalid portfolio name
#   -HTTPException(401); unauthorized, user session does not exist
#   -HTTPException(500); a ServiceError is raised, server side error
@router.post("/portfolio/create", status_code = 201)
def create_portfolio(req : PortfolioRequest) -> dict[str, UserData]:
    try:

        user = scac.find_sessions_user(req.session_id)

        with user.lock:
            api.create_portfolio(user, req.name)
            response = {"user" : UserData.convert(user)}

    except SessionCacheError as e:
        raise HTTPException(status_code = 401, detail = str(e))
    
    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))

    except ServiceError as e:
        raise HTTPException(status_code = 500, detail = str(e))

    return response


# INPUT:
#   -req(PortfolioRequest); HTTP portfolio removal payload
# OUTPUT:
#   -response(dict[str,UserData]); user data JSON payload 
# PRECONDITION:
#   -router; exists as a valid router
#   -api; contains control flow pipeline methods 
# POSTCONDITION:
#   -api; see Api.remove_portfolio() POSTCONDITION
#   -response; contains updated UserData
# RAISES:
#   -HTTPException(400); a ValidationError is raised, invalid portfolio name
#   -HTTPException(401); unauthorized, user session does not exist
#   -HTTPException(500); a ServiceError is raised, server side error
@router.post("/portfolio/remove")
def remove_portfolio(req : PortfolioRequest) -> dict[str, UserData]:
    try:

        user = scac.find_sessions_user(req.session_id)

        with user.lock:
            api.remove_portfolio(user, req.name)
            response = {"user" : UserData.convert(user)}    

    except SessionCacheError as e:
        raise HTTPException(status_code = 401, detail = str(e))
    
    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))

    except ServiceError as e:
        raise HTTPException(status_code = 500, detail = str(e))

    return response 


# INPUT:
#   -req(TransactionRequest); HTTP transaction payload
# OUTPUT:
#   -response(dict[str,PortfolioData]); portfolio data JSON payload 
# PRECONDITION:
#   -router; exists as a valid router
#   -api; contains control flow pipeline methods 
# POSTCONDITION:
#   -api; see Api.execute_buy() POSTCONDITION
#   -response; contains updated PortfolioData
# RAISES:
#   -HTTPException(400); a ValidationError is raised, invalid ticker, quantity or insufficient balance
#   -HTTPException(401); unauthorized, user session does not exist
#   -HTTPException(404); portfolio is not found
#   -HTTPException(500); a ServiceError is raised, server side error
@router.post("/buy")
def buy(req : TransactionRequest) -> dict[str, PortfolioData]:
    try:

        user = scac.find_sessions_user(req.session_id)
        shares_requested = (req.ticker, req.quantity)
        
        with user.lock:
            portfolio = user.portfolios.get(req.portfolio_name)

            if portfolio is None:
                raise HTTPException(status_code = 404, detail = "Portfolio not found")

            api.execute_buy(user, portfolio, shares_requested)
            response = {"portfolio" : PortfolioData.convert(portfolio)}

    except SessionCacheError as e:
        raise HTTPException(status_code = 401, detail = str(e))
    
    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))

    except ServiceError as e:
        raise HTTPException(status_code = 500, detail = str(e))

    return response


# INPUT:
#   -req(TransactionRequest); HTTP transaction payload
# OUTPUT:
#   -response(dict[str,PortfolioData]); portfolio data JSON payload 
# PRECONDITION:
#   -router; exists as a valid router
#   -api; contains control flow pipeline methods 
# POSTCONDITION:
#   -api; see Api.execute_sell() POSTCONDITION
#   -response; contains updated PortfolioData
# RAISES:
#   -HTTPException(400); a ValidationError is raised, invalid ticker or quantity
#   -HTTPException(401); unauthorized, user session does not exist
#   -HTTPException(404); portfolio is not found
#   -HTTPException(500); a ServiceError is raised, server side error
@router.post("/sell")
def sell(req : TransactionRequest) -> dict[str, PortfolioData]:
    try:

        user = scac.find_sessions_user(req.session_id)
        shares_requested = (req.ticker, req.quantity)
        
        with user.lock:
            portfolio = user.portfolios.get(req.portfolio_name)

            if portfolio is None:
                raise HTTPException(status_code = 404, detail = "Portfolio not found")

            api.execute_sell(user, portfolio, shares_requested)
            response = {"portfolio" : PortfolioData.convert(portfolio)}

    except SessionCacheError as e:
        raise HTTPException(status_code = 401, detail = str(e))
    
    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))

    except ServiceError as e:
        raise HTTPException(status_code = 500, detail = str(e))



    return response 


# INPUT:
#   -session_id(str); a session id
# OUTPUT:
#   -response(dict[str,UserData]); user data JSON payload 
# PRECONDITION:
#   -router; exists as a valid router
#   -api; contains control flow pipeline methods 
# POSTCONDITION:
#   -response; contains UserData for the requesting session
# RAISES:
#   -HTTPException(401); unauthorized, user session does not exist
@router.get("/user")
def get_user(session_id : str) -> dict[str, UserData]:
    try:

        user = scac.find_sessions_user(session_id)

    except SessionCacheError as e:
        raise HTTPException(status_code = 401, detail = str(e))

    response = {"user": UserData.convert(user)}

    return response


# INPUT:
#   -ticker(str); a stock ticker symbol
# OUTPUT:
#   -response(dict[str, dict]); stock quote JSON payload containing stock info fields
# PRECONDITION:
#   -router; exists as a valid router
#   -api; contains control flow pipeline methods
# POSTCONDITION:
#   -response; contains detailed stock data for the requested ticker, check Api.quote()
# RAISES:
#   -HTTPException(400); a ValidationError is raised, invalid ticker
#   -HTTPException(500); a ServiceError is raised, server side error
@router.get("/quote")
async def get_quote(ticker : str) -> dict[str, dict]:
    try:

        live_data = api.make_quote_stream(ticker)
        
    except ValidationError as e:
        raise HTTPException(status_code = 400, detail = str(e))

    except ServiceError as e:
        raise HTTPException(status_code = 500, detail = str(e))

    return StreamingResponse(live_data, media_type = "application/x-ndjson")


# INPUT:
#   -session_id(str); a session id
# OUTPUT:
#   -return(StreamingResponse); a streaming response object
# PRECONDITION: None
# POSTCONDITION:
#   -StreamingResponse; streams each yielded chunk of the async generator directly to client
# RAISES:
#   -HTTPException(401); unauthorized, user session does not exist
#   -HTTPException(404); portfolios are not found   
@router.get("/portfolios")
async def get_live_portfolio_data(session_id : str) -> StreamingResponse:

    try:
    
        user = scac.find_sessions_user(session_id)
    
    except SessionCacheError as e:
        raise HTTPException(status_code = 401, detail = str(e))

    portfolios = list(user.portfolios.values())
    
    if not portfolios:
        raise HTTPException(status_code = 404, detail = "Portfolios not found")
    
    live_data = api.make_portfolio_stream(portfolios)

    return StreamingResponse(live_data, media_type = "application/x-ndjson")

