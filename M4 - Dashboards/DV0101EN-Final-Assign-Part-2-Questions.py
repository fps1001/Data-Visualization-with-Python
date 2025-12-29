#!/usr/bin/env python
# coding: utf-8

# Import required libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv'
)

# Initialize the Dash app
app = dash.Dash(__name__)

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years 
year_list = [i for i in range(1980, 2024)]
#---------------------------------------------------------------------------------------

# Create the layout of the app
app.layout = html.Div([

    # TASK 2.1: Add title to the dashboard
    html.H1(
        "Automobile Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'font-size':24}
    ),

    # TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='select-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select Statistics'
        )
    ]),

    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=1980
        )
    ]),

    # TASK 2.3: Add a division for output display
    html.Div(
        id='output-container',
        className='output-container',
        style={'marginTop': '20px'}
    )
])

# TASK 2.4: Creating Callbacks
# Define the callback function to enable/disable year dropdown
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='select-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False  # Enable year dropdown
    else:
        return True   # Disable year dropdown


# Callback for plotting
# Define the callback function to update the output container
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [
        Input(component_id='select-statistics', component_property='value'),
        Input(component_id='select-year', component_property='value')
    ]
)
def update_output_container(selected_statistics, input_year):

    # -----------------------------
    # TASK 2.5: Recession Statistics
    # -----------------------------
    if selected_statistics == 'Recession Period Statistics':

        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales over recession years
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"
            )
        )

        # Plot 2: Average vehicles sold by vehicle type
        average_sales = recession_data.groupby(
            'Vehicle_Type'
        )['Automobile_Sales'].mean().reset_index()

        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Vehicles Sold by Vehicle Type during Recession"
            )
        )

        # Plot 3: Advertisement expenditure share by vehicle type
        exp_rec = recession_data.groupby(
            'Vehicle_Type'
        )['Advertising_Expenditure'].sum().reset_index()

        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure Share by Vehicle Type'
            )
        )

        # Plot 4: Effect of unemployment rate on sales
        unemp_data = recession_data.groupby(
            ['unemployment_rate', 'Vehicle_Type']
        )['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'
                },
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[R_chart1, R_chart2],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[R_chart3, R_chart4],
                style={'display': 'flex'}
            )
        ]

    # -----------------------------
    # TASK 2.6: Yearly Statistics
    # -----------------------------
    elif input_year and selected_statistics == 'Yearly Statistics':

        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Average automobile sales by year
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales by Year'
            )
        )

        # Plot 2: Total monthly automobile sales
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )

        # Plot 3: Average vehicles sold by vehicle type for selected year
        avr_vdata = yearly_data.groupby(
            'Vehicle_Type'
        )['Automobile_Sales'].mean().reset_index()

        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
            )
        )

        # Plot 4: Advertisement expenditure by vehicle type
        exp_data = yearly_data.groupby(
            'Vehicle_Type'
        )['Advertising_Expenditure'].sum().reset_index()

        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure by Vehicle Type'
            )
        )

        return [
            html.Div(
                className='chart-item',
                children=[Y_chart1, Y_chart2],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[Y_chart3, Y_chart4],
                style={'display': 'flex'}
            )
        ]

    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
