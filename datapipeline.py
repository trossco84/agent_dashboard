###INSTRUCTIONS####

# Pregame
#1. Login to Red.ag and go to Figures -> Weekly Balance -> Specified Week
#2. highlight the table from the first P of player to the last number in the table
    # don't include the totals row
#3. copy with whatever method you like (ctrl/cmd + c)

# Pressing Play
#4a. RUNS SELECTION IN JUPYTER NOTEBOOK: Highlight all of this test and press play or shift + enter 
#4b. RUNS SELECTION IN TERMINAL: 
#      i) navigate to this folder (cd folder path)
#      ii) run the app (python3 datapipeline.py)

# Postgame
#5 Screenshot important areas and send to intended parties
    #old mac: command + shift + 4
    #new mac: command + ctrl + shift + 4
    #windows: windows button + shift + s
    #the goal is for this to eventually become an automated email

import numpy as np
import pandas as pd
import warnings
import datetime
import master_analysis
warnings.filterwarnings("ignore", category=FutureWarning)
pd.options.mode.chained_assignment = None
this_week = pd.read_clipboard()
pyragt = pd.read_csv('/Users/trevorross/Desktop/My Projects/bettingatwork/players_and_agents.csv')

#kevin's balance
with open("/Users/trevorross/Desktop/My Projects/bettingatwork/kevin.txt") as f:
    kbal = f.readlines()
kbal = kbal[0]
kbal = float(kbal)

def update_pyragt(w3, pyragt):
    nones = w3[w3.Agent == "None"]
    
    #update pyragt dataframe and csv
    for ind in range(0,len(nones)):
        pyr = nones.iloc[ind].Player
        newplayer = input(f'what is the name for player {pyr}')
        newagent = input('and who is the agent?')
        pyragt.loc[pyr].Name = newplayer
        pyragt.loc[pyr].Agent = newagent
    
    pyragt.reset_index(inplace=True)
    pyragt.to_csv('/Users/trevorross/Desktop/My Projects/bettingatwork/players_and_agents.csv',index=False)
    pyragt.set_index('Player',inplace=True)

    #update weekly df
    w3['Agent'] = [pyragt.loc[x].Agent for x in w3.Player]
    
    return w3, pyragt

def update_master(weekly_records,lm):
    # wr1 = weekly_records.copy()
    # ls1 = lm
    # wr1['Amt'] = [wr1.loc[x].Amount if wr1.loc[x].Action == "Request" else (wr1.loc[x].Amount*(-1)) for x in wr1.index]
    # raw9 = pd.read_csv('/Users/trevorross/Desktop/My Projects/TrevorRoss/Sports Science/betatwork/raw_archives.csv')
    # wr1 = wr1.groupby('Agent').sum().drop(['Amount'],axis=1).rename(columns={'Amt':'Expected Balance'})
    # wr1['Final Balance'] = wr1['Expected Balance'].sum()/4
    # wr2 = pd.DataFrame(wr1.Agent.value_counts()).rename(columns={'Agent':'Number of Players'})
    # wr3 = wr2.join(wr1).reset_index().rename(columns={'index':'Agent'})
    # wr3['Week'] = ls1.date()
    # raw10 = raw9.append(wr3,ignore_index=True)
    # raw10.to_csv()
    master_analysis.process_new_week(weekly_records,lm)
    rd = pd.read_csv('/Users/trevorross/Desktop/My Projects/TrevorRoss/Sports Science/betatwork/raw_archives.csv')
    master_analysis.create_totals(rd)





def any_slips(w2):
    any_more='y'
    while any_more not in ['no',"No","NO","N","n"]:
        slippyr = input("slip player id?")
        amt = int(input("amount to add?"))
        current = w2.loc[slippyr].Weekly
        adjust = current + amt
        w2.Weekly.loc[slippyr] = adjust
        any_more = input('any more slips?')
    return w2

def adjust_amounts(w2):
    w2.set_index('Player',inplace=True)

    #slips
    slipcheck = input('any slips?')
    yes = ['Yes','yes','Y','y',"YES"]
    if slipcheck in yes:
        w2 = any_slips(w2)

    kb2 = kbal
    #kevin specific
    if 'pyr109' in list(w2.index):
        kcur = w2.loc['pyr109'].Weekly
        #bubble of 100
        if abs(kcur)<100:
            kb2 = kb2 + kcur
            with open("/Users/trevorross/Desktop/My Projects/bettingatwork/kevin.txt",'w') as f:
                f.write(f'{kb2}')
            w2.Weekly.pyr109 = 0
        #5% kickbacks
        elif kcur < -100:
            k5back = int(kcur * 0.95)
            w2.Weekly.pyr109 = k5back
            with open("/Users/trevorross/Desktop/My Projects/bettingatwork/kevin.txt",'w') as f:
                f.write('0')
        else:    
            with open("/Users/trevorross/Desktop/My Projects/bettingatwork/kevin.txt",'w') as f:
                f.write('0')

    #10% kickback for those greater than 1000
    w2.Weekly = w2.Weekly.apply(lambda x: x*0.9 if x < -1000 else x)

    w2.reset_index(inplace=True)
    return w2

def agent_updates(w3,agents):
    no = ['no',"No","NO","N","n"]
    yes = ['Yes','yes','Y','y',"YES"]
    any_more='y'
    while any_more not in no:
        #player id must be full, example: pyr132
        namecheck = 'n'
        while namecheck in no: 
            pyrid = input("player id?")
            pname = pyragt.loc[pyrid].Name
            print(pname)
            namecheck = input(f'is this the player you wanted to change? ({pname})')
            
        newname = input("who's the new guy? \n (this input must match name in Management)")
        newagt = input(f'new agent? \n current values are: {agents}')
        if newagt not in agents:
            agents.append(newagt)
        
        pyr2 = pyragt.copy()
        pyr2.loc[pyrid].Name = newname
        pyr2.loc[pyrid].Agent = newagt

        any_more = input('any more updates?')

    return pyr2,agents

def process_agents(w2,pyragt):
    w3 = w2.copy()
    pyragt.set_index('Player',inplace=True)

    #matching agents to their players
    w3['Agent'] = [pyragt.loc[x].Agent for x in w3.Player]
    agents = w3.Agent.unique()
    w3.fillna("None",inplace=True)   

    #agent updates
    acheck = input('any agent updates?')
    yes = ['Yes','yes','Y','y',"YES"]
    if acheck in yes:
        pyragt,agents = agent_updates(w3,agents)
    
    #updating player agent list if there is a new account
    if "None" in agents:
        w3, pyragt = update_pyragt(w3, pyragt)

    #christian logic
    c_accts = ['pyr118','pyr123']
    c_bal = 0
    if set(list(w3.Player)).isdisjoint(set(c_accts)) == False:
        for acct in c_accts:
            if acct in list(w3.Player):
                weekly = w3.set_index('Player').loc[acct].Weekly
                if weekly < 0:
                    add = weekly * 0.1
                    c_bal = c_bal+add

    c_bal = int(abs(c_bal))
    if c_bal%4 >1:
        c_bal = c_bal + 1
    c_logic = f'we each pay christian {int(c_bal/4)}'

    #adding an action column
    w3['Action'] = ['Request' if x < 0 else 'Pay' for x in w3.Weekly]
    w3['Amount'] = [abs(x) for x in w3.Weekly]
    w4 = w3[['Agent','Player','Name','Action','Amount']]
    w5 = w4.groupby(['Agent','Action','Player','Name','Amount']).sum()
    w5.to_clipboard()

    #agent specific views
    weekly_records_df = pd.DataFrame()
    print('AGENTS:')
    for agnt in agents:
        agent_view = w4[w4.Agent == agnt]
        agent_view.set_index('Agent',inplace=True)
        weekly_records_df = weekly_records_df.append(agent_view)
        print(agent_view)
        print()

    #recording the weekly output
    today = datetime.datetime.today() 
    last_monday = today - datetime.timedelta(days=today.weekday(),weeks=1)
    lm1 = datetime.date(last_monday.year,last_monday.month,last_monday.day)
    lm_string = str(lm1)
    weekly_records_df.to_csv(f'/Users/trevorross/Desktop/My Projects/bettingatwork/weekly_outputs/{lm_string}.csv')

    update_master(weekly_records_df,last_monday)

    print()
    print('Christian:')
    print(c_logic)
    print()

    return w4,pyragt
        
def process_totals(w4):
    w5 = w4.copy()
    w5['Amount'] = np.where(w5['Action']=='Pay',w5['Amount']*-1,w5['Amount'])
    totals_df = w5.groupby('Agent').sum()
    pyr_counts = pd.DataFrame(w5.Agent.value_counts())
    pyr_counts.rename(columns={'Agent':"Num. Players"},inplace=True)
    tdf = pyr_counts.join(totals_df)
    tdf['Final Balance'] = tdf.Amount.sum()/4
    print("TOTALS:")
    print(tdf)
    return tdf


def inter_bookie(tdf):
    tdf['Demand'] = [tdf.iloc[x]['Final Balance']-tdf.iloc[x].Amount for x in tdf.reset_index().index]
    td2 = tdf.sort_values('Demand')
    while td2.Demand.any() != 0.0:
        if abs(td2.iloc[0,3]) > abs(td2.iloc[3,3]):
            amt = abs(td2.iloc[3,3])
            print(f'{td2.index[0]} pays {td2.index[3]} {amt}')
            td2.iloc[0,3] = td2.iloc[0,3] + amt
            td2.iloc[3,3] = td2.iloc[3,3] - amt
            td2 = td2.sort_values('Demand')
        else:
            amt = abs(td2.iloc[0,3])
            print(f'{td2.index[0]} pays {td2.index[3]} {amt}')
            td2.iloc[0,3] = td2.iloc[0,3] + amt
            td2.iloc[3,3] = td2.iloc[3,3] - amt
            td2 = td2.sort_values('Demand')


def weekly_processing(weekly_data,pyragt):
    w2 = weekly_data[['Player','Name','Weekly']]
    if type(w2.Weekly[0]) == type('yo!'):
        w2.Weekly = w2.Weekly.str.replace(',', '').astype(float)
    w2.Player = w2.Player.apply(lambda x: x.lower())
    pyragt.Player = pyragt.Player.apply(lambda x: x.lower())
    w2 = adjust_amounts(w2)
    w4, pyragt = process_agents(w2,pyragt)
    print()
    totalsdf = process_totals(w4)
    print()
    inter_bookie(totalsdf)


if __name__ == "__main__":
    weekly_processing(this_week,pyragt)

#walk thru's
# weekly_data = this_week
# this_week.head()
# pyragt.head()