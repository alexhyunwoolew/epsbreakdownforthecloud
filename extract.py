# Importing required packages
import os
import requests
import pandas as pd

# Setting up dictionary of desired companies' stock ticker and name
companies = {
    'AMZN': 'Amazon'
    , 'GOOG': 'Alphabet'
    , 'MSFT': 'Microsoft'
}

# Setting up "apikey" string variable
project_dir = os.path.dirname(__file__)
apikey_rel_path = 'myapikey.txt'
apikey_abs_path = os.path.join(project_dir, apikey_rel_path)

with open(apikey_abs_path) as txt:
    apikey = txt.read()

# Setting up "data" list variable
data = []

# Extracting raw data for each company from Financial Modeling Prep API and appending to "data" list
for ticker in list(companies.keys()):
    url = 'https://financialmodelingprep.com/api/v3/income-statement/' + ticker + '?apikey=' + apikey
    request = requests.get(url)
    request_json = request.json()

    for i in request_json:
        data.append([
            companies[i['symbol']]
            , i['date']
            , i['operatingIncome']
            , i['totalOtherIncomeExpensesNet']
            , i['netIncome']
            , i['epsdiluted']
        ])

# Transforming "data" list of lists to pandas DataFrame
df = pd.DataFrame(
    data
    , columns = [
        'Company'
        , 'Date'
        , 'Operating Income'
        , 'Non-Operating Income'
        , 'Net Income'
        , 'EPS'
    ]
)

# Creating calculated columns for DataFrame
df['Pre-Tax Income'] = df['Operating Income'] + df['Non-Operating Income']
df['Tax'] = df['Net Income'] - df['Pre-Tax Income']
df['Tax Rate'] = abs(df['Tax']) / df['Pre-Tax Income']
df['Shares'] = df['Net Income'] / df['EPS']

# Re-arranging order of columns in DataFrame
df = df[[
    'Company'
    , 'Date'
    , 'Operating Income'
    , 'Non-Operating Income'
    , 'Pre-Tax Income'
    , 'Tax Rate'
    , 'Tax'
    , 'Net Income'
    , 'Shares'
    , 'EPS'
]]

# Exporting DataFrame to CSV file for Tableau
df.to_csv(
    'extract.csv'
    , index=False
)
