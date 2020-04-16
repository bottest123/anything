from nsepy import get_history
import numpy as np
import pandas as pd
from datetime import date, timedelta
import os
import csv


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# retrieves the names of stock
companies_file = (open('stocklist.csv'))
companies_list = csv.reader(companies_file)

# creates new data frame
final = pd.DataFrame()
counter = 0

# dates configuration

end_day = date.today()
start_day = end_day - timedelta(365)

for company in companies_list:
    try:

        symbol, name = company
        # iterates through stock lists and retrieves by date conditions
        df = get_history(symbol=symbol.format(symbol), start=start_day, end=end_day)

        # adds three columns for statistical purposes
        change = np.log(df['Close'] / df['Close'].shift())
        stdev = np.std(change)
        avg = np.mean(change)
        df['Upside'] = round(((avg + stdev) * 100), 2)
        df['Downside'] = round(((avg - stdev) * 100), 2)
        df['Stock Name'] = symbol

        df['PP'] = round(((df['High'] + df['Low'] + df['Close']) / 3), 2)
        df['R1'] = (2 * df['PP'] - df['Low'])
        df['S1'] = (2 * df['PP'] - df['High'])
        df['R2'] = (df['PP'] + df['High'] - df['Low'])
        df['S2'] = (df['PP'] - df['High'] + df['Low'])
        df['R3'] = (df['High'] + 2 * (df['PP'] - df['Low']))
        df['S3'] = (df['Low'] - 2 * (df['High'] - df['PP']))

        # select new columns / first row
        selected = df.iloc[-1:, [16, 6, 9,14,15,23,21,19,17,18,20,22]]

        # appends datasets to final dataframe
        final = pd.concat([final, selected])
    except:
        continue

    # counts the iteration
    counter += 1

    # show progress
    print("Writing " + str(counter) + " of " + str(companies_list) + "!")

    # clears console

    # exports csv file
    final.to_csv("historicalSD1.csv", index=None, header=True)