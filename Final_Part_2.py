#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

# Dropdown options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# Year list
year_list = [i for i in range(1980, 2024)]

# Layout
app.layout = html.Div([

    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}
    ),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type',
            style={'width': '80%', 'fontSize': 20}
        )
    ]),

    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select Year',
            style={'width': '80%', 'fontSize': 20}
        )
    ]),

    html.Div(
        id='output-container',
        className='chart-grid',
        style={'display': 'flex', 'flexDirection': 'column'}
    )
])

# Enable / disable year dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'


# Update charts
@app.callback(
    Output('output-container', 'children'),
    [
        Input('dropdown-statistics', 'value'),
        Input('select-year', 'value')
    ]
)
def update_output_container(selected_statistics, input_year):

    # ------------------ RECESSION STATISTICS ------------------
    if selected_statistics == 'Recession Period Statistics':

        recession_data = data[data['Recession'] == 1]

        # Plot 1: Average automobile sales over recession years
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales During Recession Period"
            )
        )

        # Plot 2: Average sales by vehicle type during recession
        avg_sales = recession_data.groupby(
            ['Year', 'Vehicle_Type']
        )['Automobile_Sales'].mean().reset_index()

        R_chart2 = dcc.Graph(
            figure=px.bar(
                avg_sales,
                x='Year',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title='Average Automobile Sales by Vehicle Type During Recession'
            )
        )

        # Plot 3: Advertising expenditure share during recession
        exp_rec = recession_data.groupby(
            'Vehicle_Type'
        )['Advertising_Expenditure'].sum().reset_index()

        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Advertising Expenditure Share by Vehicle Type During Recession'
            )
        )

        # Plot 4: Effect of unemployment rate on sales
        unemp_rate = recession_data.groupby(
            ['unemployment_rate', 'Vehicle_Type']
        )['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_rate,
                x='Vehicle_Type',
                y='Automobile_Sales',
                color='unemployment_rate',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'
                },
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div([R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div([R_chart3, R_chart4], style={'display': 'flex'})
        ]

    # ------------------ YEARLY STATISTICS ------------------
    elif selected_statistics == 'Yearly Statistics' and input_year:

        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly automobile sales
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Automobile Sales'
            )
        )

        # Plot 2: Monthly automobile sales
        mon_sales = data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mon_sales,
                x='Month',
                y='Automobile_Sales',
                title='Average Monthly Automobile Sales'
            )
        )

        # Plot 3: Vehicle type sales in selected year
        avr_vdata = yearly_data.groupby(
            ['Month', 'Vehicle_Type']
        )['Automobile_Sales'].mean().reset_index()

        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Month',
                y='Automobile_Sales',
                color='Vehicle_Type',
                title=f'Average Vehicles Sold by Vehicle Type in {input_year}'
            )
        )

        # Plot 4: Advertising expenditure in selected year
        exp_data = yearly_data.groupby(
            'Vehicle_Type'
        )['Advertising_Expenditure'].sum().reset_index()

        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title=f'Advertising Expenditure by Vehicle Type in {input_year}'
            )
        )

        return [
            html.Div([Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div([Y_chart3, Y_chart4], style={'display': 'flex'})
        ]

    return None


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
