from bs4 import BeautifulSoup
import requests


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

# print(data)
# TableIt.print(data, useFieldNames=True)

# ['COURSE CODE', 'TOTAL HOURS', 'EXEMPTION HOURS', 'TOTAL ABSENT', 'TOTAL PRESENT', 'PERCENTAGE OF ATTENDANCE', 'PERCENTAGE WITH EXEMP', 'PERCENTAGE WITH EXEMP MED', 'ATTENDANCE PERCENTAGE FROM', 'ATTENDANCE PERCENTAGE TO']
# ['18XD61', '21', '0', '7', '14', '67', '67', '67', '21-02-2022', '02-04-2022']
# ['18XD62', '21', '0', '5', '16', '77', '77', '77', '21-02-2022', '02-04-2022']
# ['18XD63', '20', '0', '5', '15', '75', '75', '75', '21-02-2022', '02-04-2022']
# ['18XD64', '35', '0', '3', '32', '92', '92', '92', '21-02-2022', '02-04-2022']
# ['18XD66', '28', '0', '4', '24', '86', '86', '86', '21-02-2022', '02-04-2022']
# ['18XD67', '28', '0', '4', '24', '86', '86', '86', '21-02-2022', '02-04-2022']
# ['18XD68', '28', '0', '8', '20', '72', '72', '72', '21-02-2022', '02-04-2022']
# ['18XDA8', '35', '0', '3', '32', '92', '92', '92', '21-02-2022', '02-04-2022']
print(int(85)/100)
print(round(0.5714285714285714,2))