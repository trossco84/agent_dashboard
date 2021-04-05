import pandas as pd 
import numpy as np 
import datetime


def process_new_week(weekdf,week_string):

    raw_data = pd.read_csv('/Users/trevorross/Desktop/My Projects/bettingatwork/raw_archives.csv')
    r2=raw_data.copy()

    nw2 = weekdf.copy()
    
    #processing
    nw2['Amts'] = np.where(nw2['Action']=='Pay',nw2['Amount']*-1,nw2['Amount'])
    nw3 = nw2.groupby('Agent').sum().reset_index().drop(['Amount'],axis=1)
    nw3['Expected Balance'] = nw3.Amts
    nw3.drop(['Amts'],axis=1,inplace=True)
    num_players = pd.DataFrame(nw2.Agent.value_counts())
    num_players['Number of Players'] = num_players.Agent
    num_players.drop(['Agent'],axis=1,inplace=True)
    nw3 = nw3.set_index('Agent').join(num_players).reset_index()
    nw3['Final Balance'] = sum(nw3['Expected Balance'])/4

    #adding the week
    ws2 = week_string.split("_")
    nw3['Week'] = datetime.date(year=int(ws2[2]),month=int(ws2[0]),day=int(ws2[1]))

    #updating raw archives
    r3 = r2.append(nw3,ignore_index=True)
    r3.to_csv('/Users/trevorross/Desktop/My Projects/bettingatwork/raw_archives.csv',index=False)
    create_totals(r3)

def create_totals(raw_data):
    rgroup = raw_data.groupby('Agent').sum()
    numweeks = len(raw_data.Week.unique())
    rgroup = rgroup.rename(columns={'Expected Balance':'Total Revenue'})
    tots = rgroup[['Total Revenue']]
    tots['Avg Players per Week'] = rgroup['Number of Players']/numweeks
    tots['Avg Revenue per Week'] = tots['Total Revenue']/numweeks
    tots.to_csv('/Users/trevorross/Desktop/My Projects/bettingatwork/agent_totals.csv')
