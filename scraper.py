import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd


#period = '2018'
url = 'https://www.numbeo.com/quality-of-life/rankings_by_country.jsp'
r = requests.get(url)
soup = BeautifulSoup(r.content,'html.parser')
form = soup.find('form',{'class':'changePageForm'})
periods = [f['value'] for f in form.findChildren() if f.name == 'option']
print(periods)
j = 0
df = pd.DataFrame(columns=['Rank',
                           'Country',
                           'Quality of Life Index',
                           'Purchasing Power Index',
                           'Safety Index',
                           'Health Care Index',
                           'Cost of Living Index',
                           'Property Price to Income Ratio',
                           'Traffic Commute Time Index',
                           'Pollution Index',
                           'Climate Index', 'Period'])

for period in periods:
    url = 'https://www.numbeo.com/quality-of-life/rankings_by_country.jsp?title={}'.format(period)

    r = requests.get(url)

    soup = BeautifulSoup(r.content,'html.parser')
    tbody = soup.find('tbody')

    i=1
    for row in tbody.children:
        if row.name != 'tr':
            continue
        #print(row)
        row_data = [e.text for e in row.contents if e.name == 'td']
        row_data[0] = i
        row_data.append(period)
        #print(row_data)
        df.loc[j] = row_data
        i += 1
        j += 1
    df.to_csv('numbeo.csv')
