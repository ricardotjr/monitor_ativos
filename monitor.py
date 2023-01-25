import pandas_datareader as web
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print
from yahoo_fin.stock_info import get_dividends
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pyfiglet import figlet_format

print("=" * 80)
print(figlet_format(text="CARREGANDO", font="standard", justify="center"))
print("=" * 80)

while True:
    with open('ativos.txt', 'r') as f:
        tickers_plain = f.read()
    tickers = [value.replace('\n', '') + ".SA" for value in tickers_plain.split(",")]
    current_price = web.get_quote_yahoo(tickers)
    table_fii = Table(title="Ativos")
    table_fii.add_column(" ", justify="right", style="blue")
    for ticker in tickers:
        table_fii.add_column(ticker, justify="center", style="magenta")
    def current_price(tickers):
        current_price = web.get_quote_yahoo(tickers)["price"]
        return current_price
    def regular_market_change(tickers):
        market_change = web.get_quote_yahoo(tickers)["regularMarketChange"]
        return market_change
    def regular_market_high(tickers):
        market_high = web.get_quote_yahoo(tickers)["regularMarketDayHigh"]
        return market_high
    def regular_market_low(tickers):
        market_low = web.get_quote_yahoo(tickers)["regularMarketDayLow"]
        return market_low
    prices = current_price(tickers)
    mud_reg_merc = regular_market_change(tickers)
    high = regular_market_high(tickers)
    low = regular_market_low(tickers)
    table_fii.add_row("Preço Atual (R$)", *[str(prices[i]) for i in range(len(prices))])
    table_fii.add_row("Variação +-", *[str(round(mud_reg_merc[i], 2)) for i in range(len(mud_reg_merc))])
    table_fii.add_row("Maior Preço ⬆", *[str(high[i]) for i in range(len(high))])
    table_fii.add_row("Menor Preço ⬇", *[str(low[i]) for i in range(len(low))])
    table_div = Table(title="Dividendos")
    table_div.add_column(" ", justify="right", style="blue")
    [table_div.add_column(ticker, justify="center", style="magenta") for ticker in tickers]
    dividends = []
    reference_month = datetime.now() + relativedelta(day=1) + relativedelta(months=-1)
    date_string = reference_month.strftime('%Y/%m/%d')
    [dividends.append(get_dividends(ticker, date_string).values) for ticker in tickers]
    table_div.add_row("Último Div. (R$)", *[str(round(dividends[i][0][0], 2)) if len(dividends[i]) > 0 and len(dividends[i][0]) > 0 else str(round(0, 2)) for i in range(len(dividends))])
    console = Console()
    console.clear()
    console.print(table_fii)
    console.print(table_div)
    time.sleep(10)
