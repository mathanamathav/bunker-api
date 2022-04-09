from bs4 import BeautifulSoup
import requests
from tabulate import tabulate


session = requests.Session()
r = session.get('https://ecampus.psgtech.ac.in/studzone2/')

# print ("STATUS 1:",r.status_code)
# print (r.history)
# print ("REDIRECT 1: ",r.url)

loginpage = session.get(r.url)

soup = BeautifulSoup(loginpage.text,"html.parser")

viewstate = soup.select("#__VIEWSTATE")[0]['value']
eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
viewstategen = soup.select("#__VIEWSTATEGENERATOR")[0]['value']


item_request_body  = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR': viewstategen,
    '__EVENTVALIDATION': eventvalidation,
    'rdolst': 'S',
    'txtusercheck': '19PD01',
    'txtpwdcheck': '27feb02',
    'abcd3': 'Login',
}


response = session.post(url=r.url, data=item_request_body, headers={"Referer": r.url})
print ("STATUS 2:",response.status_code)

defaultpage = 'https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx'

page = session.get(defaultpage)
soup = BeautifulSoup(page.text,"html.parser")

data = []
table = soup.find('table', attrs={'class':'cssbody'})


rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty val

print(tabulate(data,tablefmt="plain"))
# TableIt.print(data, useFieldNames=True)