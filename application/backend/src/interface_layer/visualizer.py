import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.backend_bases import CloseEvent
import pandas as pd
from tabulate import tabulate

# PURPOSE:
#   -Visualizer provides a data visualization abstraction
#   -provides an isolated layer that allows for construction of data charts
class Visualizer:
    def __init__(self):
        self.fig = None
        self.ax = None
        self.ani = None

        
    # INPUT:
    #   -serialize(callable); returns serialized portfolios in a dict representing json format
    # OUTPUT: None
    # PRECONDITION:
    #   -serialize; returns a fully serialized dict representing all portfolios user has
    # POSTCONDITION:
    #   -self.fig, self.ax, self.ani; constructed and active if no chart exists and data is non-empty, otherwise unchanged
    #   -execution; chart display does not block program
    # RAISES: None
    def display_pie_chart(self, serialize : callable) -> None:
        PRICE_REFRESH_INTERVAL = 4000

        if self.fig is None and serialize()["portfolios"][0]["stocks"]:
            self.fig, self.ax = plt.subplots()
            self.fig.canvas.mpl_connect('close_event', self.clean_up)

            def update():
                portfolio_data = serialize()
                portfolio = portfolio_data["portfolios"][0]

                self.ax.clear()

                if not portfolio["stocks"]:
                    return

                df = pd.DataFrame(portfolio["stocks"])

                labels = df['ticker'] + ' (' + df['value'].map('${:,.2f}'.format) + ')'

                self.ax.pie(df['value'], labels=labels, autopct='%1.0f%%')
                self.ax.set_title(f"Portfolio Distribution")
                self.ax.set_xlabel(f"Total portfolio value: ${portfolio["total"]:,.2f}")

            self.ani = animation.FuncAnimation(self.fig, update, interval= PRICE_REFRESH_INTERVAL, cache_frame_data=False)
            plt.show(block=False)    


    # INPUT: 
    #   -portfolio(Portfolio); a user portfolio
    #   -head_length(int); length of the string(head) we are centering under
    # OUTPUT:
    #   -centered_table(str); an adjusted table generated from tabulate
    # PRECONDITION:
    #   -portfolio; fully populated and up to date
    # POSTCONDITION:
    #   -centered_table; a tabulate table is produced with padding to center it under some head
    # RAISES: None
    def construct_stock_table(self, portfolio, head_length : int) -> str:
        stock_list = list(portfolio.stocks.values())

        data = [[stock.ticker, stock.quantity] for stock in stock_list]
        headers = ["Stock", "Quantity"]

        table = tabulate(data, headers = headers, tablefmt="pretty")

        centered_table = "\n".join(line.center(head_length) for line in table.splitlines())

        return centered_table


    # INPUT: None
    # OUTPUT: None
    # PRECONDITION:
    #   -self.fig; an active chart exists
    # POSTCONDITION:
    #   -self.fig; chart is closed and removed from display
    # RAISES: None
    def close_chart(self) -> None:
        if self.ani is not None:
            self.ani.event_source.stop()
        plt.close(self.fig)
        self.clean_up()
    
    # INPUT:
    #    -event(CloseEvent); matplotlib state in event of manual user closure
    # OUTPUT: None
    # PRECONDITION: None
    # POSTCONDITION:
    #    -self.fig, self.ax, self.ani; all set to None
    # RAISES: None
    def clean_up(self, event : CloseEvent = None) -> None:
        if self.ani is not None:
            self.ani.event_source.stop()
        self.ani = None
        self.fig = None
        self.ax = None
