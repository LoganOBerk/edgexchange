from collections import defaultdict

from domain_models import User, Portfolio, Stock
from persistence_layer import StoredUser, StoredPortfolio, StoredStock, StoredAccountData


# INPUT:
#   -stored_stocks(list[StoredStock]); all user stocks listed as portfolio id, stock id, ticker, quantity
# OUTPUT:
#   -stock_allocations(dict[int, list[StoredStock]]); list of stock data keyed to specific portfolio id
# PRECONDITION:
#   -stored_stocks; see Database.pull_stocks() POSTCONDITION
# POSTCONDITION:
#   -stock_allocations; each portfolio id maps to its list of stock tuples
# RAISES: None
def allocate_stocks(stored_stocks : list[StoredStock]) -> dict[int, list[StoredStock]]:
    stock_allocations = defaultdict(list)
    for stock in stored_stocks:
        stock_allocations[stock.p_id].append(stock)

    return stock_allocations


# INPUT:
#   -stored_data(StoredAccountData); all data related to user account
# OUTPUT:
#   -user(User); a fully populated user object
# PRECONDITION:
#   -stored_data; some non empty set of stored data for a real user
# POSTCONDITION:
#   -user; populated with id, username, balance, all portfolios and their stocks from database
# RAISES: None
def hydrate_account(stored_data : StoredAccountData) -> User:
    stored_user = stored_data.user
    
    u_id = stored_user.id
    u_name = stored_user.username
    u_bal = stored_user.balance

    user = User(id=u_id, username=u_name, balance=u_bal)

    hydrate_user_portfolios(user.portfolios, stored_data.portfolios, allocate_stocks(stored_data.stocks))

    return user


# INPUT:
#   -user_portfolios(dict[str,Portfolio]); user portfolios keyed by portfolio name
#   -stored_portfolios(list[StoredPortfolio]); all user portfolios listed as portfolio id, user id, name 
#   -stored_stocks(dict[int, list[StoredStock]]); all user stocks listed as stock id, portfolio id, ticker, quantity keyed by portfolio id
# OUTPUT: None
# PRECONDITION:
#   -user_portfolios; is empty
#   -stored_portfolios; see Database.pull_portfolios() POSTCONDITION
#   -stored_stocks; see Database.pull_stocks() POSTCONDITION
# POSTCONDITION:
#   -user_portfolios; populated with all portfolios and their respective stocks
# RAISES: None
def hydrate_user_portfolios(user_portfolios : dict[str, Portfolio], stored_portfolios : list[StoredPortfolio], stored_stocks : dict[int, list[StoredStock]]) -> None:
    for portfolio in stored_portfolios:

        p_id = portfolio.id
        p_name = portfolio.name

        user_portfolios[p_name] = Portfolio(id=p_id,name=p_name)

        hydrate_portfolio_stocks(user_portfolios[p_name].stocks, stored_stocks.get(p_id, []))


# INPUT:
#   -portfolio_stocks(dict[str,Stock]); a users portfolio stocks keyed by ticker 
#   -stored_portfolio_stocks(list[StoredStocks]); specific portfolios stock list
# OUTPUT: None
# PRECONDITION:
#   -portfolio_stocks; is empty
#   -stored_portfolio_stocks; contains all stocks for given portfolio
# POSTCONDITION:
#   -portfolio_stocks; populated with all stocks for the given portfolio
# RAISES: None
def hydrate_portfolio_stocks(portfolio_stocks : dict[str, Stock], stored_portfolio_stocks : list[StoredStock]) -> None:

    for stock in stored_portfolio_stocks:

        s_id = stock.id
        s_ticker = stock.ticker
        s_quantity = stock.quantity

        portfolio_stocks[s_ticker] = Stock(id=s_id, ticker=s_ticker, quantity=s_quantity)

    
