# -*- coding: utf-8 -*-
"""
Created on Sat May  4 12:46:17 2024

@author: lovro
v0.1
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter

URL = "https://paka3.mss.edus.si/registriweb/Seznam1.aspx?Seznam=2010"

response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
form = soup.select_one('#form1')
div = form.find_all('div')[1]
t1 = div.find_all('tr')[1]
table = t1.find_all('table')[0]
rows = table.find_all('tr')
data = []

for row in rows:
    cols = row.find_all('td')
    row_data = []
    for index, col in enumerate(cols):
        link = col.find('a')
        if link:
            if index == 2:
                row_data.append(col.text.strip())
            elif index == 8:
                email = link['href'].split(':')[1]
                row_data.append(email)
            elif index == 9:
                row_data.append((link['href']))
            else:
                row_data.append((link.text.strip(), link['href']))
        else:
            row_data.append(col.text.strip())
    data.append(row_data)


headers = data[0]
data_rows = data[1:]
DATA = pd.DataFrame(data_rows, columns=headers)
DATA.sort_values(by='STATISTIČNA REGIJA', inplace=True)

# =============================================================================
# # To excel
# =============================================================================

excel = ExcelWriter("Slovenske sole.xlsx", engine='xlsxwriter')
DATA.to_excel(excel, 'Seznam sol')
excel.close()
