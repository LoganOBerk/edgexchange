from collections import defaultdict

from .user import User
from .portfolio import Portfolio
from .stock import Stock


# INPUT:
#   -stored_data(tuple[tuple, list[tuple], list[tuple]]); all data related to user account
# OUTPUT:
#   -user_account(User); a fully populated user account object
# PRECONDITION:
#   -stored_data; some non empty set of stored data for a real user
# POSTCONDITION:
#   -user_account; populated with id, username, balance, all portfolios and their stocks from database
# RAISES: None
def hydrate_account(stored_data : tuple[tuple, list[tuple], list[tuple]]) -> User:
    stored_user, stored_portfolios, stored_stocks = stored_data

    u_id = stored_user[0]
    u_name = stored_user[1]
    u_bal = stored_user[3]

    user_account = User(id=u_id, username=u_name, balance=u_bal)

    hydrate_user_portfolios(user_account.portfolios, stored_portfolios, stored_stocks)

    return user_account


# INPUT:
#   -stored_stocks(list[tuple]); all user stocks listed as portfolio id, stock id, ticker, quantity
# OUTPUT:
#   -portfolio_assignments(dict[int, list[tuple]]); list of stock data keyed to specific portfolio id
# PRECONDITION:
#   -stored_stocks; see Database.pull_stocks() POSTCONDITION
# POSTCONDITION:
#   -portfolio_assignments; each portfolio id maps to its list of stock tuples
# RAISES: None
def assign_portfolio_allocations(stored_stocks : list[tuple]) -> dict[int, list[tuple]]:
    portfolio_assignments = defaultdict(list)
    for stock in stored_stocks:
        p_id = stock[0]
        portfolio_assignments[p_id].append(stock[1:])

    return portfolio_assignments

# INPUT:
#   -user_portfolios(dict[str,Portfolio]); user portfolios keyed by portfolio name
#   -stored_portfolios(list[tuple]); all user portfolios listed as portfolio id, name 
#   -stored_stocks(list[tuple]); all user stocks listed as portfolio id, stock id, ticker, quantity
# OUTPUT: None
# PRECONDITION:
#   -user_portfolios; is empty
#   -stored_portfolios; see Database.pull_portfolios() POSTCONDITION
#   -stored_stocks; see Database.pull_stocks() POSTCONDITION
# POSTCONDITION:
#   -user_portfolios; populated with all portfolios and their respective stocks
# RAISES: None
def hydrate_user_portfolios(user_portfolios : dict[str, Portfolio], stored_portfolios : list[tuple], stored_stocks : list[tuple]) -> None:
    stored_stocks = assign_portfolio_allocations(stored_stocks)

    for portfolio in stored_portfolios:

        p_id = portfolio[0]
        p_name = portfolio[1]

        user_portfolios[p_name] = Portfolio(id=p_id,name=p_name)

        hydrate_portfolio_stocks(user_portfolios[p_name].stocks, stored_stocks.get(p_id, []))


# INPUT:
#   -portfolio_stocks(dict[str,Stock]); a users portfolio stocks keyed by ticker 
#   -stored_portfolio_stocks(list[tuple]); specific portfolios stock list
# OUTPUT: None
# PRECONDITION:
#   -portfolio_stocks; is empty
#   -stored_portfolio_stocks; contains all stocks for given portfolio
# POSTCONDITION:
#   -portfolio_stocks; populated with all stocks for the given portfolio
# RAISES: None
def hydrate_portfolio_stocks(portfolio_stocks : dict[str, Stock], stored_portfolio_stocks : list[tuple]) -> None:

    for stock in stored_portfolio_stocks:

        s_id = stock[0]
        s_ticker = stock[1]
        s_quantity = stock[2]

        portfolio_stocks[s_ticker] = Stock(id=s_id, ticker=s_ticker, quantity=s_quantity)

    