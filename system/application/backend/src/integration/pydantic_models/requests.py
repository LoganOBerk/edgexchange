from pydantic import BaseModel


# PURPOSE:
#   -LogoutRequest provides a deserializable abstraction for logout data
#   -defines the expected JSON body shape for the /logout endpoint
class LogoutRequest(BaseModel):
    session_id: str


# PURPOSE:
#   -CredsRequest provides a deserializable abstraction for credentials
#   -defines the expected JSON body shape for the /register and /login endpoints
class CredsRequest(BaseModel):
    username: str
    password: str


# PURPOSE:
#   -FundsRequest provides a deserializable abstraction for funds deposit data
#   -defines the expected JSON body shape for the /fund endpoint
class FundsRequest(BaseModel):
    session_id: str
    funds_requested: float


# PURPOSE:
#   -PortfolioRequest provides a deserializable abstraction for portfolio data
#   -defines the expected JSON body shape for the /portfolio/create and /portfolio/remove endpoints 
class PortfolioRequest(BaseModel):
    session_id: str
    name: str


# PURPOSE:
#   -TransactionRequest provides a deserializable abstraction for transaction data
#   -defines the expected JSON body shape for the /buy and /sell endpoints 
class TransactionRequest(BaseModel):
    session_id: str
    portfolio_name: str
    ticker: str
    quantity: int

