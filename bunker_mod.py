from bs4 import BeautifulSoup
import requests
# import pandas as pd
import math
# import json
# import plotly
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


# def many_pieplot(res,specs,subplot_titles,labels,total_class,total_present):
#     """
#         This function is to plot sub-pie-chart 
#     """

#     fig = make_subplots(rows=len(res), cols=1,specs=specs,subplot_titles=subplot_titles)

#     for i in range(len(res)):
#         # Define pie charts
#         fig.add_trace(go.Pie(labels=labels, values=[total_class[i],total_present[i]]
#                             ), row=i+1, col=1)



#     fig.update_layout(height=250*len(res))
#     fig.update_layout({
#         'plot_bgcolor':'rgba(0,0,0,0)',
#         'paper_bgcolor': 'rgba(0,0,0,0)'
#     },showlegend=True,
#     title="Class-Wise view")

    
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON


    

# def line_chart(courses,total_class,total_present,title):
#     """
#         This function is to plot line chart Present vs Total
#     """
#     fig = go.Figure(data=[
#                     go.Bar(name='Total Class', x=courses, y=total_class),
#                     go.Bar(name='Total Present', x=courses, y=total_present)
#         ])
#     # fig = px.bar(df, x='course_code', y='total_class', color='course_code', barmode='group')
#     fig.update_layout({
#         'plot_bgcolor':'rgba(0,0,0,0)',
#         'paper_bgcolor': 'rgba(0,0,0,0)'
#     },showlegend=True,
#     title=title)
    
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON 



# def pie_chart(label,value,title):
#     """
#         This function is to plot pie chart
#     """
#     fig = go.Figure(data=[go.Pie(labels=label, values=value, hole=.3)])
#     fig.update_layout({
#         'plot_bgcolor':'rgba(0,0,0,0)',
#         'paper_bgcolor': 'rgba(0,0,0,0)'
#     }
#     ,showlegend=True,
#     title=title)

#     graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON2




def data_json(data):
    """
        here we convert the data to json format calculate the amount days we have to take leave.
    """
    index_required = [0,1,2,4,7,8,9]
    response_data = []
    threshold = 0.75

    for item in range(1,len(data)):
        item = data[item]
        temp = {}

        temp['name'] = item[index_required[0]]

        
        j = 1
        temp['total_hours'] = int(item[index_required[j]]) #1
        j += 1
        temp['exception_hour'] = int(item[index_required[j]]) #2
        j += 1
        temp['total_present'] = int(item[index_required[j]]) #4
        temp['total_present'] += temp['exception_hour']
        j += 1
        temp['percentage_of_attendance'] = int(item[index_required[j]]) 

        if temp['percentage_of_attendance'] <= 75:
            temp['class_to_attend'] = math.ceil((threshold*temp['total_hours'] - temp['total_present'])/(1-threshold))
        
        else:
            temp['class_to_bunk'] = math.floor((temp['total_present']-(threshold*temp['total_hours']))/(threshold))


        j += 1
        temp['attendance_from'] = (item[index_required[j]])
        j += 1
        temp['attendance_to'] = (item[index_required[j]])
        
        response_data.append(temp)
    
    return response_data


def return_attendance(username,pwd):
    try:
        session = requests.Session()
        r = session.get('https://ecampus.psgtech.ac.in/studzone2/')
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
            'txtusercheck': username,
            'txtpwdcheck': pwd,
            'abcd3': 'Login',
        }
        
        response = session.post(url=r.url, data=item_request_body, headers={"Referer": r.url})
        val = response.url

        if response.status_code == 200:

            defaultpage = 'https://ecampus.psgtech.ac.in/studzone2/AttWfPercView.aspx'
        
            page = session.get(defaultpage)
            soup = BeautifulSoup(page.text,"html.parser")


        
            data = []
            column = []
            table = soup.find('table', attrs={'class':'cssbody'})

            if table == None:
                message = str(soup.find('span', attrs={'id':'Message'}))
                if "On Process" in message:
                    return "Table is being updated"
        
            try:
                rows = table.find_all('tr')
                for index,row in enumerate(rows):
                    
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele]) # Get rid of empty val
            
                # df = pd.DataFrame(data, columns=column)
                # res = df.to_json(orient="split")
                # return res
                return data,session
            except:
                return "Invalid password"
        else:
            return "Try again after some time"
    
    except:
        return "Try again after some time"


def return_timetable(session):
    defaultpage = 'https://ecampus.psgtech.ac.in/studzone2/AttWfStudTimtab.aspx'

    page = session.get(defaultpage)
    soup = BeautifulSoup(page.text,"html.parser")



    data = []
    table = soup.find('table', attrs={'id':'TbCourDesc'})

    if table == None:
        return {"error" : "no data"}

    try:
        rows = table.find_all('tr')
        for index,row in enumerate(rows):
            
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) 
        
        class_id = {}
        for i in range(1,len(data)):
            class_id[data[i][0]] = data[i][1]

    
        return class_id
    except:
        return {"error" : "no data"}

def gradeMap(grade):
    grade_score_map = {
        'O':10,
        'A+':9,
        'A':8,
        'B+':7,
        'B':6,
        'C+':5,
        'C':4,
        'W':0,
        'RA':0,
        'SA':0
    }
    
    if grade not in grade_score_map.keys():
        return 0

    return grade_score_map[grade]

def return_cgpa(session):
    resultspage = 'https://ecampus.psgtech.ac.in/studzone2/FrmEpsStudResult.aspx'
        
    page = session.get(resultspage)
    soup = BeautifulSoup(page.text,"html.parser")

    latest_sem_data = []
    table = soup.find('table', attrs={'id':"DgResult"})

    if table != None:
        try:
            rows = table.find_all('tr')
            for index,row in enumerate(rows):
                
                cols = row.find_all('td')
                cols = [ele.text for ele in cols]
                latest_sem_data.append([ele for ele in cols if ele])
        except:
            print("No results available !!")

    coursepage = 'https://ecampus.psgtech.ac.in/studzone2/AttWfStudCourseSelection.aspx'

    page = session.get(coursepage)
    soup = BeautifulSoup(page.text,"html.parser")

    data = []
    table = soup.find('table', attrs={'id':"PDGCourse"})

    if table != None:
        try:
            rows = table.find_all('tr')
            for index,row in enumerate(rows):
                
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
        except:
            print("No Course Info available !!")
    else:
        print("No Course Info available !!")

    global df
    global latest_sem_records
    
    # Preprocess latest sem results if available
    if len(latest_sem_data) != 0:
        latest_sem_data.pop(0)
        latest_sem_records = pd.DataFrame(latest_sem_data, columns=['COURSE SEM', 'COURSE CODE', 'COURSE TITLE', 'CREDITS', 'GRADE', 'RESULT'])
        latest_sem_records['GRADE'] = latest_sem_records['GRADE'].str.split().str[-1]
        latest_sem_records['COURSE SEM'] = latest_sem_records['COURSE SEM'].replace(r'^\s*$', np.nan, regex=True)
        latest_sem_records['COURSE SEM'].fillna(method='ffill', inplace=True)

    try:
        cols = data.pop(0)
        df = pd.DataFrame(data, columns=cols)

        # Add latest sem results if available
        if len(latest_sem_data) != 0:
            df = df.append(latest_sem_records, ignore_index=True)
            df.drop_duplicates(subset="COURSE CODE", keep="last", inplace=True)
    except:
        df = latest_sem_records.copy()

    # CPGA calculation
    latest_sem = df['COURSE SEM'].max()
    df['CREDITS']=df['CREDITS'].astype(int)
    df['GRADE'] = df['GRADE'].apply(gradeMap)
    df['COURSE SCORE'] = df['GRADE'] * df['CREDITS']
    latest_cgpa = df['COURSE SCORE'].sum() / df['CREDITS'].sum()

    res = {
        'lastest_sem' : latest_sem,
        'latest_sem_cgpa' : round(latest_cgpa, 3) 
    }

    return res

