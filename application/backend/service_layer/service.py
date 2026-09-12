import sys

from .hydrator import hydrate_account
from common.security import secure_creds
from common.errors import DatabaseError, LiveCacheError, ServiceError
from domain_models import User, Portfolio
from integration_layer import LiveCache as lcac
from persistence_layer import StoredUser, StoredPortfolio, StoredStock

# PURPOSE:
#   -Service provides a routing/serving, and memory populator abstraction
#   -Decouples business logic from the database and interface layers
class Service:
    def __init__(self, database):
        self.db = database

    
    # INPUT:
    #   -username(str); user username
    # OUTPUT:
    #   -user_dat(StoredUser); user id, username, password, balance
    # PRECONDITION: None
    # POSTCONDITION:
    #   -user_dat; user information provided if username exists in database, None otherwise
    # RAISES:
    #   -ServiceError; database call fails
    def identify_user(self, username : str) -> StoredUser:
        try:

            user_dat = self.db.pull_user(username)

        except DatabaseError as e:
            raise ServiceError("Failed to match credentials") from e

        return user_dat


    # INPUT:
    #   -username(str); user username
    # OUTPUT:
    #   -user(User); populated account for the given username
    # PRECONDITION:
    #   -username; a user with this username exists in the database
    # POSTCONDITION: 
    #   -user; populated with id, username, balance and all portfolios and respective stocks
    # RAISES:
    #   -ServiceError; database call fails
    def find_account(self, username : str) -> User:
        try:

            user = hydrate_account(self.db.pull_account(username))

        except DatabaseError as e:
            raise ServiceError("Failed to find account") from e

        return user


    # INPUT: 
    #   -credentials(tuple[str,str]); user username and password
    # OUTPUT: None
    # PRECONDITION:
    #   -credentials; username and password are non-empty strings, see Validator.account_validator() POSTCONDITION
    # POSTCONDITION: 
    #   -database; see Database.insert_user() POSTCONDITION
    # RAISES: 
    #   -ServiceError; database call fails
    def create_account(self, credentials : tuple[str, str]) -> None:
        credentials = secure_creds(credentials)

        try:
            with self.db.transaction():
                self.db.insert_user(credentials)

        except DatabaseError as e:
            raise ServiceError("Failed to create account") from e
    
    
    # INPUT:
    #   -user_account(User); current user account
    #   -funds_request(float); amount of money to add to balance 
    # OUTPUT: None
    # PRECONDITION:
    #   -user_account; account info is up to date
    #   -funds_request; > 0
    # POSTCONDITION: 
    #   -database; see Database.update_funds() POSTCONDITION
    #   -user_account; funds are added to account
    # RAISES:
    #   -ServiceError; database call fails
    def fund_account(self, user_account : User, funds_request : float) -> None:
        try:

            with self.db.transaction():
                self.db.update_funds(user_account.id, funds_request)

        except DatabaseError as e:
            raise ServiceError("Failed to update funds") from e

        user_account.add_funds(funds_request)
        

    # INPUT:
    #   -user_account(User); current user account
    #   -portfolio_name(str); name of portfolio to create
    # OUTPUT: None
    # PRECONDITION:
    #   -user_account; account info is up to date
    #   -portfolio_name; see Validator.portfolio_validator() POSTCONDITION
    # POSTCONDITION: 
    #   -database; see Database.insert_portfolio() POSTCONDITION
    #   -user_account; empty portfolio with portfolio_name is added to account
    # RAISES:
    #   -ServiceError; database call fails
    def create_portfolio(self, user_account : User, portfolio_name : str) -> None:
        try:

            with self.db.transaction():
                p_id = self.db.insert_portfolio(user_account.id, portfolio_name)

        except DatabaseError as e:
            raise ServiceError("Failed to create portfolio") from e

        user_account.add_portfolio(portfolio_name, p_id)


    # INPUT:
    #   -user_account(User); current user account
    #   -portfolio_name(str); name of portfolio to remove
    # OUTPUT: None
    # PRECONDITION:
    #   -user_account; account info is up to date
    #   -portfolio_name; see Validator.portfolio_validator() POSTCONDITION
    # POSTCONDITION:
    #   -database; see Database.delete_portfolio() POSTCONDITION
    #   -user_account; portfolio is removed from in memory account
    # RAISES:
    #   -ServiceError; database call fails
    def remove_portfolio(self, user_account : User, portfolio_name : str) -> None:
        try:

            portfolio = user_account.portfolios[portfolio_name]
            with self.db.transaction():
                self.db.delete_portfolio(portfolio.id)

        except DatabaseError as e:
            raise ServiceError("Failed to remove portfolio") from e

        user_account.remove_portfolio(portfolio_name)


    # INPUT: 
    #   -user_account(User); current user account
    #   -portfolio(Portfolio); some portfolio belonging to current user
    #   -shares_request(tuple[str,int]); requested stock ticker and quantity
    # OUTPUT: None
    # PRECONDITION:
    #   -user_account; account info is up to date
    #   -portfolio; portfolio is up to date
    #   -shares_request; see Validator.shares_request_validator() POSTCONDITION
    # POSTCONDITION:
    #   -database; if ticker exists in portfolio see Database.update_stock(), else see Database.insert_stock() POSTCONDITION
    #   -user_account; balance is decremented based on purchase cost
    #   -portfolio; stock with matching ticker is added with quantity or updated
    # RAISES:
    #   -ServiceError; database call fails or LiveCache call fails
    def execute_buy(self, user_account : User, portfolio : Portfolio, shares_request : tuple[str, int]) -> None:
        
        try:

            ticker, quantity = shares_request

            price = lcac.get_stock_price(ticker)
            total_cost = price * quantity

            s_id = None


            with self.db.transaction():
                self.db.update_funds(user_account.id, -total_cost)
            
                if portfolio.has_stock(ticker):
                    stock = portfolio.stocks[ticker]
                    self.db.update_stock(stock.id, quantity)
                else:
                    s_id = self.db.insert_stock(portfolio.id, shares_request)

        except (DatabaseError, LiveCacheError) as e:
            raise ServiceError("Failed to execute buy") from e

        user_account.sub_funds(total_cost)
        portfolio.buy_shares(shares_request, s_id)
        

    # INPUT: 
    #   -user_account(User); current user account
    #   -portfolio(Portfolio); some portfolio belonging to current user
    #   -shares_request(tuple[str,int]); requested stock ticker and quantity
    # OUTPUT: None
    # PRECONDITION:
    #   -user_account; account info is up to date
    #   -portfolio; portfolio is up to date
    #   -shares_request; see Validator.shares_request_validator() POSTCONDITION
    # POSTCONDITION:
    #   -database; if quantity equals current holdings see Database.delete_stock(), else see Database.update_stock() POSTCONDITION
    #   -user_account; balance is incremented by sale value
    #   -portfolio; stock with matching ticker is updated or removed
    # RAISES:
    #   -ServiceError; database call fails or LiveCache call fails
    def execute_sell(self, user_account : User, portfolio : Portfolio, shares_request : tuple[str, int]) -> None:
        
        try:

            ticker, quantity = shares_request

            price = lcac.get_stock_price(ticker)
            total_value = price * quantity


            with self.db.transaction():
                self.db.update_funds(user_account.id, total_value)

                stock = portfolio.stocks[ticker]

                if quantity == stock.quantity:
                    self.db.delete_stock(stock.id)
                else:
                    self.db.update_stock(stock.id, -quantity)

        except (DatabaseError, LiveCacheError) as e:
            raise ServiceError("Failed to execute sell") from e

        user_account.add_funds(total_value)
        portfolio.sell_shares(shares_request)


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective fields in LiveCache.get_stock_quote()
    # RAISES: 
    #   -ServiceError; propagated from LiveCache.get_stock_quote()
    def quote_stock(self, ticker : str):
        try:

            quote = lcac.get_stock_quote(ticker)

        except LiveCacheError as e:
            raise ServiceError("Failed to get stock info") from e

        return quote 


    # INPUT:
    #   -portfolios(list[Portfolio]); users portfolios
    # OUTPUT:
    #   -packaged_data(dict[str, list[dict]]); all portfolios holdings and total value at the moment or empty dict if the call fails
    # PRECONDITION: None
    # POSTCONDITION:
    #   -packaged_data; "total" contains portfolio current value and "holdings" contains all stock holdings
    # RAISES: None
    def package_portfolio_data(self, portfolios: list[Portfolio]) -> dict[str, list[dict]]:

        packaged_data = {}
        holdings = []

        try:
            
            for portfolio in portfolios: holdings.extend(list(portfolio.stocks.keys()))

            prices = lcac.get_stock_prices(holdings)

            packaged_data["portfolios"] = []
            for portfolio in portfolios:
                total = 0
                entry = {"portfolio": portfolio.name, "total": "$0.00", "holdings": []}

                for ticker, stock in portfolio.stocks.items():
                    price = prices[ticker]
                    value = stock.quantity * price
                    total += value

                    entry["holdings"].append({
                        "ticker": ticker,
                        "price": price,
                        "quantity": stock.quantity,
                        "value": value,
                        "sector": lcac.get_sector(ticker),
                        "label": f"{ticker} (${value:,.2f})"
                    })

                entry["total"] = f"${total:,.2f}"
                packaged_data["portfolios"].append(entry)

        except LiveCacheError as e:
            pass

        return packaged_data

    
    # INPUT: None
    # OUTPUT: None
    # PRECONDITION: None
    # POSTCONDITION: None
    #   -execution; program execution is terminated
    # RAISES:   
    #   -SystemExit; always raised on call
    @staticmethod
    def exit_app() -> None:
        sys.exit(0)




    