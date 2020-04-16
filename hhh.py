from __future__ import print_function
from nsetools import Nse
import csv
import pandas as pd
import pandas.io.json as pd_json
from datetime import date, timedelta
from gspread_pandas import Spread, Client

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def dayopen():
    nse = Nse()
    print(nse)

    companies_list = nse.get_stock_codes(cached=False)
    my_dict = companies_list
    w = csv.writer(open("stocklist.csv", "w",newline=''))
    for key, val in my_dict.items():
        w.writerow([key, val])

    stock_list = csv.reader(open('stocklist.csv'))

    next(stock_list)

    #creates new data frame
    final = pd.DataFrame()

    # dates configuration
    end_day = date.today()
    start_day = end_day - timedelta(365)

    for company in stock_list:
        try:

            symbol, name = company



            df1 = nse.get_quote(symbol.format(symbol), as_json=True)
            # df10 = nse.get_history(symbol.format(symbol), start=start_day, end=end_day,as_json=True)
            # datax = pd_json.loads(df10)
            # df11 = pd.json_normalize(datax)
            # df12 = pd.DataFrame(df11)
            data = pd_json.loads(df1)  # load
            df = pd.json_normalize(data)  # normalise
            df2 = pd.DataFrame(df)
        except:
            continue
        selected = df2.iloc[0:, [1, 6, 65, 11, 20, 67]]
        final = pd.concat([final, selected])
        final = final.reset_index(drop=True)
        print(final)
        final.to_csv('dayopendata.csv', index=None, header=True)
dayopen()

def combine():
    xxx = pd.read_csv('historicalSD1.csv')
    yyy = pd.read_csv('dayopendata.csv')

    # merge multiple dataframes for legibility and add new columns
    xyz = xxx.merge(yyy, left_on='Stock Name', right_on='symbol')

    xyz['Sell T4'] = round(((xyz['Downside'] * xyz['open']) / 100 * 1.618) + xyz['open'], 2)
    xyz['-1.236'] = round(((xyz['Downside'] * xyz['open']) / 100 * 1.236) + xyz['open'], 2)
    xyz['Sell T3'] = round(((xyz['Downside'] * xyz['open']) / 100) + xyz['open'], 2)
    xyz['-0.888'] = round(((xyz['Downside'] * xyz['open']) / 100 * 0.888) + xyz['open'], 2)
    xyz['-0.786'] = round(((xyz['Downside'] * xyz['open']) / 100 * 786) + xyz['open'], 2)
    xyz['Sell T2'] = round(((xyz['Downside'] * xyz['open']) / 100 * 0.618) + xyz['open'], 2)
    xyz['-0.5'] = round(((xyz['Downside'] * xyz['open']) / 100 * 0.5) + xyz['open'], 2)
    xyz['Sell T1'] = round(((xyz['Downside'] * xyz['open']) / 100 * 0.382) + xyz['open'], 2)
    xyz['INITIATE Sell'] = round(((xyz['Downside'] * xyz['open']) / 100 * 0.236) + xyz['open'], 2)

    xyz['INITIATE Buy'] = round(((xyz['Upside'] * xyz['open']) / 100 * 0.236) + xyz['open'], 2)
    xyz['Buy T1'] = round(((xyz['Upside'] * xyz['open']) / 100 * 0.382) + xyz['open'], 2)
    xyz['0.5'] = round(((xyz['Upside'] * xyz['open']) / 100 * 0.5) + xyz['open'], 2)
    xyz['Buy T2'] = round(((xyz['Upside'] * xyz['open']) / 100 * 0.618) + xyz['open'], 2)
    xyz['0.786'] = round(((xyz['Upside'] * xyz['open']) / 100 * 0.786) + xyz['open'], 2)
    xyz['0.888'] = round(((xyz['Upside'] * xyz['open']) / 100 * 0.888) + xyz['open'], 2)
    xyz['Buy T3'] = round(((xyz['Upside'] * xyz['open']) / 100) + xyz['open'], 2)
    xyz['1.236'] = round(((xyz['Upside'] * xyz['open']) / 100 * 1.236) + xyz['open'], 2)
    xyz['Buy T4'] = round(((xyz['Upside'] * xyz['open']) / 100 * 1.618) + xyz['open'], 2)

    # selected few columns required for storage or display

    xyz = xyz.iloc[:, [0,15,16,17,12,5,6,7,8,9,10,11,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]]

    print(xyz)
    xyz.to_csv('xyz.csv', index=None, header=True)
combine()

def uploadtosheet():
    file_name = "xyz.csv"
    df = pd.read_csv(file_name)

    # 'Example Spreadsheet' needs to already exist and your user must have access to it
    spread = Spread('Example Spreadsheet')
    # This will ask to authenticate if you haven't done so before

    # Display available worksheets
    spread.sheets

    # Save DataFrame to worksheet 'New Test Sheet', create it first if it doesn't exist
    spread.df_to_sheet(df, index=False, sheet='SDSheet', start='A2', replace=True)
    print(spread)
    # <gspread_pandas.client.Spread - User: '<example_user>@gmail.com', Spread: 'Example Spreadsheet', Sheet: 'New Test Sheet'>

    # You can now first instanciate a Client separately and query folders and
    # instanciate other Spread objects by passing in the Client
    client = Client()
    # Assumming you have a dir called 'example dir' with sheets in it
    available_sheets = client.find_spreadsheet_files_in_folders('example dir')
    spreads = []
    for sheet in available_sheets.get('example dir', []):
        spreads.append(Spread(sheet['id'], client=client))
uploadtosheet()
