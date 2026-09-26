from pydantic import BaseModel


# PURPOSE:
#   -StockData provides a serializable abstraction for a Stock object
#   -defines the JSON response body for a Stock
class StockData(BaseModel):
    ticker: str
    quantity: int


# PURPOSE:
#   -PortfolioData provides a serializable abstraction for a Portfolio object
#   -defines the JSON response body for a Portfolio 
class PortfolioData(BaseModel):
    name: str
    stocks: dict[str, StockData]


    # INPUT:
    #   -portfolio(Portfolio); a user portfolio
    # OUTPUT:
    #   -portfolio_data(PortfolioData); an object representing serializable data of portfolio
    # PRECONDITION:
    #   -portfolio; fully populated and up to date
    # POSTCONDITION:
    #   -portfolio_data; properly represents the JSON response body of a portfolio
    # RAISES: None
    @classmethod
    def convert(cls, portfolio):
        
        stocks = {}

        for ticker, stock in portfolio.stocks.items():
            stocks[ticker] = StockData(ticker = ticker, quantity = stock.quantity)

        portfolio_data = cls(name = portfolio.name, stocks = stocks)

        return portfolio_data
       

# PURPOSE:
#   -UserData provides a serializable abstraction for a User object
#   -defines the JSON response body for a User
class UserData(BaseModel):
    username: str
    balance: float
    portfolios: dict[str, PortfolioData]


    # INPUT:
    #   -user(User); current user account
    # OUTPUT:
    #   -user_data(UserData); an object representing serializable data of user
    # PRECONDITION:
    #   -user; fully populated and up to date
    # POSTCONDITION:
    #   -user_data; properly represents the JSON response body of a user
    # RAISES: None
    @classmethod
    def convert(cls, user):

        portfolios = {}

        for name, portfolio in user.portfolios.items():
            portfolios[name] = PortfolioData.convert(portfolio)
        
        user_data = cls(username = user.username, balance = user.balance, portfolios = portfolios)

        return user_data