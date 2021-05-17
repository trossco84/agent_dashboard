import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input,Output
import plotly.express as px
import dash_table as dtable
# import dash_auth

#authorization

#create data
week_totals = pd.read_csv('https://raw.githubusercontent.com/trossco84/bettingatwork/main/raw_archives.csv')
a_weeks = list(week_totals.Week.unique())[::-1]
totals_columns=[{"name": i, "id": i} for i in week_totals.columns[1:]]
last_week = a_weeks[0]


possible_agents = list(week_totals.Agent.unique())
possible_agents.append('All')
a_cols=['Agent','Player','Name','Action','Amount']
agent_columns = [{"name":i,"id":i} for i in a_cols]
agent_columns.pop(1)

available_weeks = [{"label":x,"value":x} for x in a_weeks]

#interbookie rapid optimization
def process_interbookie(ww2):
    #creates data frame for optimization
    w2p = pd.read_csv(f'https://raw.githubusercontent.com/trossco84/bettingatwork/main/weekly_outputs/{ww2}.csv')
    w2p['Amount'] = np.where(w2p['Action']=='Pay',w2p['Amount']*-1,w2p['Amount'])
    tdf = w2p.groupby('Agent').sum()
    tdf['Final Balance'] = tdf.Amount.sum()/4
    weekly_balance = tdf['Final Balance'].sum()

    #optimization
    tdf['Demand'] = [tdf.iloc[x]['Final Balance']-tdf.iloc[x].Amount for x in tdf.reset_index().index]
    tdf.Demand = tdf.Demand.round(decimals=2)
    td2 = tdf.sort_values('Demand')
    output_list = []
    while td2.Demand.any() != 0.0:
        if abs(td2.iloc[0,2]) > abs(td2.iloc[3,2]):
            amt = abs(td2.iloc[3,2])
            output_list.append(f'{td2.index[0]} pays {td2.index[3]} {amt}')
            td2.iloc[0,2] = td2.iloc[0,2] + amt
            td2.iloc[3,2] = td2.iloc[3,2] - amt
            td2 = td2.sort_values('Demand')
        else:
            amt = abs(td2.iloc[0,2])
            output_list.append(f'{td2.index[0]} pays {td2.index[3]} {amt}')
            td2.iloc[0,2] = td2.iloc[0,2] + amt
            td2.iloc[3,2] = td2.iloc[3,2] - amt
            td2 = td2.sort_values('Demand')
        
        if ((td2.Demand < 1).all()):
            break
   
#christian logic
    w3 = w2p
    c_accts = ['pyr118','pyr123']
    c_bal = 0
    if set(list(w3.Player)).isdisjoint(set(c_accts)) == False:
        for acct in c_accts:
            if acct in list(w3.Player):
                weekly = w3.set_index('Player').loc[acct].Amount
                if weekly > 0:
                    add = weekly * 0.1
                    c_bal = c_bal+add

    c_bal = int(abs(c_bal))
    if c_bal%4 >1:
        c_bal = c_bal + 1
    c_logic = f'we each pay christian {int(c_bal/4)}'
    output_list.append(c_logic)
    return output_list,weekly_balance

last_payments,idc = process_interbookie(last_week)
output_list = last_payments

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash( __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server

app.title= 'Agent Dashboard'
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Img(className="logo", src="https://raw.githubusercontent.com/trossco84/bettingatwork/main/assets/logo2.jpg"),
                        html.H2("Agent Dashboard for Betting at Work"),
                        html.P("Weeks:"),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id='WeekFilter',
                                    options=available_weeks,
                                    value=last_week,
                                    clearable=False,
                                    className='div-for-dropdown'
                                    )
                                    ],
                        ),
                        html.P("Agents:"),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id='AgentFilter',
                                    options=[
                                        {"label":j,"value":j}
                                        for j in possible_agents
                                        ],
                                        value='All',
                                        clearable=False
                                        )
                                        ],
                        ),
                        html.Div(
                            children=[
                            html.H5(
                                id="Net",
                            ),
                            ]
                        ),
                        html.Div(
                            id="interbookie",
                        )
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        html.H2("Weekly Totals"),
                        dtable.DataTable(
                            id='TotalsTable',
                            columns=totals_columns,
                            style_header={'backgroundColor': '#1E1E1E'},
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white'
                            },
                            style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{Agent} ="Trev"',
                                    },
                                    'backgroundColor': '#08a9d19c',
                                    'color': 'white'
                                },
                                {
                                    'if': {
                                        'filter_query': '{Agent} ="Gabe"',
                                    },
                                    'backgroundColor': '#e066e08f',
                                    'color': 'white'
                                },
                                {
                                    'if': {
                                        'filter_query': '{Agent} ="Orso"',
                                    },
                                    'backgroundColor': '#58d18788',
                                    'color': 'white'
                                },
                                {
                                    'if': {
                                        'filter_query': '{Agent} ="Dro"',
                                    },
                                    'backgroundColor': '#94723fd8',
                                    'color': 'white'
                                },
                                ]                                        
                            ),
                        html.H2('Weekly Payments'),
                        dtable.DataTable(
                            id='AgentTable',
                            columns=agent_columns,
                            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                            style_as_list_view=True,
                            style_cell={
                                'backgroundColor': '#1E1E1E',
                                'color': 'white',
                                'text-align':'center'
                            },
                            style_data_conditional=[
                                {
                                    'if': {
                                        'filter_query': '{Agent} ="Trev"',
                                    },
                                    'backgroundColor': '#08a9d19c',
                                    'color': 'white'
                                },
                                {
                                    'if': {
                                        'filter_query': '{Agent} ="Gabe"',
                                    },
                                    'backgroundColor': '#e066e08f',
                                    'color': 'white'
                                },
                                {
                                    'if': {
                                        'filter_query': '{Agent} ="Orso"',
                                    },
                                    'backgroundColor': '#58d18788',
                                    'color': 'white'
                                },
                                {
                                    'if': {
                                        'filter_query': '{Agent} ="Dro"',
                                    },
                                    'backgroundColor': '#94723fd8',
                                    'color': 'white'
                                },                                                                                                
                                ]
                            )
                            ]
                )
            ]
        )
    ]    
)



@app.callback(
    [Output("Net","children"),Output("interbookie","children"),Output("TotalsTable","data"),Output("AgentTable","data")],
    [
        Input("WeekFilter","value"),
        Input("WeekFilter","value"),
        Input("AgentFilter","value")
    ],
)


def update_tables(wf1,weekfilter,agentfilter):
    try:
        output_list,weekly_balance = process_interbookie(weekfilter)
        Net_value=f'Net: ${weekly_balance}'
        o_list=[html.H5(x) for x in output_list]
        interbookie_children=o_list
    except:
        Net_value='Week Payments Data not Currently Availalbe'
        test_list=['Orso pays Trev 69', 'Dro pays Trev 69', 'Dro pays Gabe 69']
        t_list = [html.H5(x) for x in test_list]
        interbookie_children=t_list
    
    wtdata = week_totals[week_totals.Week == weekfilter].groupby('Agent').sum().reset_index()
    TotalsTable_data = wtdata.to_dict('records')
    try:
        agent_data = pd.read_csv(f'https://raw.githubusercontent.com/trossco84/bettingatwork/main/weekly_outputs/{weekfilter}.csv')
        agent_data = agent_data.sort_values(by='Agent')
        agent_data = agent_data[['Agent','Action','Name','Amount']]
        if agentfilter=="All":
            AgentTable_data = agent_data.to_dict('records')
        else:
            ad2 = agent_data[agent_data.Agent == agentfilter]
            AgentTable_data = ad2.to_dict('records')
    except:
        ad_empty = pd.DataFrame()
        ad_empty['Agent'] = possible_agents[:len(possible_agents)]
        ad_empty[['Name','Action','Amount']]=['week unavailable',np.nan,np.nan]
        AgentTable_data = ad_empty.to_dict('records')

    return Net_value,interbookie_children,TotalsTable_data,AgentTable_data



if __name__ == '__main__':
    app.run_server(debug=True)