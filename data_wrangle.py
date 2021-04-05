import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

master = pd.read_clipboard()
pyragt = pd.read_csv('/Users/trevorross/Desktop/My Projects/bettingatwork/players_and_agents.csv')

m2 = master[['Player','Name','Lifetime']]
m2.Player = m2.Player.apply(lambda x: x.lower())
m2.Lifetime = m2.Lifetime.str.replace(',', '').astype(float)


m2['Agent'] = [pyragt.set_index('Player').loc[x].Agent for x in m2.Player]
m2.groupby('Agent').Lifetime.max

m2.nlargest(5,'Lifetime')
m2.nsmallest(5,'Lifetime')

xls = pd.ExcelFile('/Users/trevorross/Desktop/My Projects/bettingatwork/Master Balances.xls')

previous_weeks = ['3.15.2021','3.8.2021','3.1.2021','2.22.2021','2152021','282021','212021','1252021','1182021','1112021','1042021','12282020','12212020','12142020','12072020','11302020','11232020','11162020','11092020','11022020','10262020','10192020','10122020','10052020','9282020','9212020','9142020','972020']

t1 = pd.DataFrame()
for week in previous_weeks[::-1]:
    next1 = pd.read_excel('/Users/trevorross/Desktop/My Projects/bettingatwork/Master Balances (2).xlsx',sheet_name=week,usecols='I:M',nrows=4,skiprows=44)
    next1['Week'] = week
    t1 = t1.append(next1)
t1.drop(['Unnamed: 12'],axis=1,inplace=True)
t2 = t1.reset_index().drop(['index'],axis=1).fillna(np.nan)
agent_list=[]
for x in t2.index:
    if type(t2.iloc[x].Agent) == type(np.nan):
        agent_list.append(t2.iloc[x]['Agent.1'])
    else:
        agent_list.append(t2.iloc[x].Agent)
t2['Agent'] = agent_list
t2.drop(['Agent.1'],axis=1,inplace=True)
t2['Number of Players'][0:4] = 5

t3 = t2[['Week','Agent','Number of Players','Expected Balance','Final Balance']]


t3.groupby('Week').sum()['Expected Balance']
t3.head(30)
last_week = pd.read_csv('/Users/trevorross/Desktop/My Projects/bettingatwork/weekly_outputs/3_22_2021')
last_week['Amts'] = [last_week.iloc[x].Amount if last_week.iloc[x].Action == 'Request' else (last_week.iloc[x].Amount) *(-1) for x in last_week.index]
last_week.head()
last_week.Agent.value_counts()
lw2 = last_week.groupby('Agent').sum()
lw2 = lw2.reset_index().drop(['Amount'],axis=1)
lw2['Expected Balance'] = lw2.Amts
lw2.drop(['Amts'],axis=1,inplace=True)
lw2['Week'] = '3.22.2021'
lw2['Number of Players'] = [2,5,9,4]
lw2['Final Balance'] = sum(lw2['Expected Balance'])/4

t4 = t3.append(lw2).reset_index().drop(['index'],axis=1)

tgroup = t4.groupby('Agent').sum()
numweeks = len(previous_weeks)+1
tgroup = tgroup.rename(columns={'Expected Balance':'Total Revenue'})
totals = tgroup[['Total Revenue']]
totals['Avg Players per Week'] = tgroup['Number of Players']/numweeks
totals['Avg Revenue per Week'] = totals['Total Revenue']/numweeks


import datetime
#fixing the date column
days = []
months = []
years = []
for wk in t4.Week[96:]:
    nwk = wk.split('.')
    months.append(nwk[0])
    days.append(nwk[1])
    years.append(nwk[2])
    
datelist = []
for x in range(0,len(days)):
    datelist.append(datetime.date(year=int(years[x]),month=int(months[x]),day=int(days[x])))

archives = t4.copy()
ar2 = archives.copy()
ar2['Week'] = datelist
ar2.groupby('Week').sum()

ar2.to_csv('/Users/trevorross/Desktop/My Projects/bettingatwork/raw_archives.csv',index=False)
pd.read_csv('/Users/trevorross/Desktop/My Projects/bettingatwork/raw_archives.csv').head()

sns.barplot(x=totals.index,y=totals['Avg Players per Week'],palette='Pastel1')
plt.title('Average Players per Week')

sns.barplot(x=totals.index,y=totals['Total Revenue'],palette='Pastel1')
plt.title('Total Revenue by Agent')

sns.barplot(x=totals.index,y=totals['Avg Revenue per Week'],palette='Pastel1')
plt.title('Average Revenue per Week')
totals
import matplotlib.pyplot as plt


trevs_clients = pd.read_csv('/Users/trevorross/Desktop/My Projects/bettingatwork/raw_archives.csv')
trevs_clients=trevs_clients[trevs_clients.Agent=='Trev'].reset_index()
tc2 = trevs_clients.copy()
tc2['Week2'] = [datetime.date(int(x[0:4]),int(x[5:7]),int(x[8:])) for x in tc2.Week]
tc3 = tc2[25:]
tc3.head()

march = pd.read_clipboard()
march['Player'] = [x.lower() for x in march.Player]
pa = pd.read_csv('/Users/trevorross/Desktop/My Projects/bettingatwork/players_and_agents.csv')
pa.head()

ng = march.set_index('Player').join(pa.set_index('Player'),how='inner')
ng2 = ng[['Name','Agent','Graded Bets Amount','Net']]
ng2.rename(columns={'Graded Bets Amount':'TotalGambled'},inplace=True)
ng2.drop(['pyr101'],inplace=True)
ng2 = ng2[ng2.Agent != "None"]
ng2.Net = ng2.Net.str.replace(',','').astype(float)
ng2.Net = [-x for x in ng2.Net]
month_agents = ng2.groupby('Agent').sum()
ma2 = month_agents.copy()
ma2.reset_index(inplace=True)

t = ng2[ng2.Agent == 'Gabe']
t2 = t.copy()
t.Net = [-x for x in t.Net]
t.Name.pyr124 = 'luc'
t.Name.pyr117 = 'peyton'
t.Name.pyr129 = 'wagner'
t.Name.pyr105 = 'maxwell'
t.Name.pyr103 = 'jalen'
t.Name.pyr125 = 'casey'
keep = ['ben','peyton','maxwell','jalen','casey']
t3 = t[t.Name.isin(keep)].reset_index()

t.head()

sns.barplot(x=t.Name,y=t.TotalGambled,palette='seismic')
plt.title('Total Amount Gambled by Player in March')
plt.ylabel('Total Gambled')
plt.xlabel('')
plt.xticks(rotation=90)

sns.barplot(x=t.Name,y=t.Net,palette='seismic')
plt.title('Player Profit in March')
plt.ylabel('Net Amount')
plt.xlabel('')
plt.xticks(rotation=90)


sns.barplot(x=ma2.Agent,y=ma2.Net,palette='seismic')
plt.title('Mach Revenue by Agent')

sns.barplot(x=ma2.Agent,y=ma2.TotalGambled,palette='seismic')
plt.title('Total Amount Gambled in March by Agent')
plt.ylabel('Total Amount Gambled')

ng[ng.Agent=='Dro']

ng.head(30)