import pickle
import time
import dash
from dash import html
from dash import dcc
import psutil
import pandas as pd
from dash import dash_table

# Create a dash app
app = dash.Dash(__name__)

# Create a figure with an empty trace
figure = dict(
    data=[{'x': [
        i for i in range(psutil.cpu_count())
    ], 'y': [], 'type': 'bar', 'name': 'CPU Usage (%)'}],
    layout=dict(
        title='Real Time CPU Usage',
        xaxis=dict(title='CPU', range=[0, psutil.cpu_count()], autorange=False, showgrid=False, zeroline=False, showline=False, ticks='', showticklabels=False, fixedrange=True),
        yaxis=dict(title='Usage (%)', range=[0, 100]),
    )
)

figure2 = dict(
    data=[{'x': [
        i for i in range(psutil.cpu_count())
    ], 'y': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 'type': 'line', 'name': 'CPU Usage (%)'}],
    layout=dict(
        title='Static CPU Usage',

        xaxis=dict(title='CPU', range=[0, psutil.cpu_count()], autorange=False, showgrid=False, zeroline=False, showline=False, ticks='', showticklabels=False, fixedrange=True),
        yaxis=dict(title='Usage (%)', range=[0, 100]),
    )

    
)

# Create a Graph component with the figure and a callback interval
app.layout = html.Div([  
    html.Link(rel='stylesheet', href='https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'),
    dcc.Graph(id='cpu-graph', figure=figure, 
              style={
                  'width': '100%',
                  'height': '50vh',
                  'display': 'none',
                  'padding': '0.5rem'
                  }
                  ),
    # another graph
    dcc.Graph(id='cpu-graph2', figure=figure2),

                #   add spacer
    
    # add button to donwload csv
    
    # add horizontal spacer

                  dcc.Slider(
        id='interval-component-slider',
        min=0,
        max=1000,
        step=1,
        value=100,
        marks={
            0: {'label': '0 ms', 'style': {'color': '#77b0b1'}},
            100: {'label': '100 ms'},
            200: {'label': '200 ms'},
            300: {'label': '300 ms'},
            400: {'label': '400 ms'},
            500: {'label': '500 ms'},
            600: {'label': '600 ms'},
            700: {'label': '700 ms'},
            800: {'label': '800 ms'},
            900: {'label': '900 ms'},
            1000: {'label': '1000 ms', 'style': {'color': '#f50'}}
        }
    ),
    # add horizontal spacer
    html.Div(style={'padding': '0.5rem'}),

   dash_table.DataTable(
    id='cpu-table',
    columns=[{'name': i, 'id': i} for i in ['CPU', 'Usage (%)']],
    style_cell={
        'textAlign': 'center',
        'font-family': 'Open Sans',
        'padding': '0.5rem'
    },
    style_header={
        'color': 'white',
        'backgroundColor': '#007bff',
        'fontWeight': 'bold',
        'font-family': 'Open Sans',
        'padding': '0.5rem'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ]
    # margin bottom
    , style_table={'marginBottom': '10rem'}
)
    ,
    # sldier for interval
    
    # interval component
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),

    html.Div(id='output'),
    # add a footer
    html.Footer('Andrés Aldaz - 2023  @daibeal'
                # add link
                
                , 
                style={
        'color': 'darkblue',
          'fontSize': 18,
            'textAlign': 'center',
            'font-family': 'Open Sans',
            'padding': '1rem',
            'background': 'lightgrey',
            'position': 'fixed',
            'bottom': '0',
            'width': '100%',
            # margin top
            'marginTop': '3rem'




        }
        )

])

# Define a callback function to update the figure and table with new data
@app.callback(
    [dash.dependencies.Output('cpu-graph', 'extendData'), dash.dependencies.Output('cpu-table', 'data')],
    [dash.dependencies.Input('interval-component', 'n_intervals')]
    
)
def update_graph(n):
    

    # Get CPU information
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(percpu=True)

    # Create a data frame with headers and data
    headers = ["CPU", "Usage (%)"]
    data = [[i, percent] for i, percent in enumerate(cpu_percent)]
    df = pd.DataFrame(data, columns=headers)

    # Append the new data to the existing trace
    graph_data = dict(x=[df['CPU']], y=[df['Usage (%)']]), [0] * cpu_count

    # Return the new data for the table
    table_data = df.to_dict('records')
    # create a database and fill it with the data
    # save to csv every 10 seconds
    #  set time with time lirbary
    
    df.to_pickle('cpu.pkl')
    # save to cavs but do not include the index and do not overwrite keep all data add columns for timestamp
    df['timestamp'] = pd.Timestamp.now()        
    # do not use print use logger
    import logging
    logging.basicConfig(filename='cpu.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    logging.info('CPU usage: %s', df.to_string())
    # save pandas as object for later use
    
    
        
        

    


    # fill figure with the data



    return graph_data, table_data

# define callback for slider
@app.callback(
    dash.dependencies.Output('interval-component', 'interval'),
    [dash.dependencies.Input('interval-component-slider', 'value')])
def update_interval(value):


    return value

# callback for cpu-graph2 insert static data
@app.callback(
    dash.dependencies.Output('cpu-graph2', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_graph2(n):
    # creat ploly lint chart with static data
    # fill with data from the table
    # get data from table
    # get data from table
    # data = get pandas from pickle
    data = pd.read_pickle('cpu.pkl')

    print(data)
    # create the plot and fill it with the data
    figure2 = dict(
    data=[{'x': [
        i for i in range(psutil.cpu_count())
    ], 'y': data['Usage (%)'], 'type': 'bar', 'name': 'CPU Usage (%)'}],
    layout=dict(
        title='CPU Usage (per core)',

        xaxis=dict(title='CPU', range=[0, psutil.cpu_count()], 
                   autorange=True, showgrid=True, zeroline=True, showline=True, showticklabels=True, fixedrange=True, 
                #    show all ticks
               tickmode='linear', tick0=0, dtick=1),
        yaxis=dict(title='Usage (%)', range=[0, 100]),
    )

    # change the color of each bar to red if it is above 80% usage
    # change the color of each bar to green if it is below 80% usage
    # change the color of each bar to yellow if it is above 50% usage

   



    

    )
    

    # update the color of the bars
    return figure2




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
