from dash import html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
from src.services.dash import Dash


# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("assets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

options = [{'label': 'All Sites', 'value': 'ALL'}]
for item in spacex_df['Launch Site'].unique():
    options.append({'label': item.upper(), 'value': item})

app_layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={
                'textAlign': 'center',
                'color': '#503D36',
                'font-size': 40}),
        dcc.Dropdown(
            id='site-dropdown',
            options=options,
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True),
        html.Br(),
        html.Div(
            dcc.Graph(
                id='success-pie-chart')),
        html.Br(),
        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            marks={
                0: '0',
                100: '100'},
            value=[
                min_payload,
                max_payload]),
        html.Div(
            dcc.Graph(
                id='success-payload-scatter-chart')),
    ])


def init(server):
    # Initialize the Dash app
    app = Dash(
        server=server,
        routes_pathname_prefix="/spacex/",
    )
    app.layout = app_layout

    @app.callback(
        Output(component_id='success-pie-chart', component_property='figure'),
        Input(component_id='site-dropdown', component_property='value')
    )
    def get_pie_chart(entered_site):
        filtered_df = spacex_df[spacex_df['class'] > 0]
        if entered_site == 'ALL':
            fig = px.pie(
                filtered_df.groupby('Launch Site')['class'].sum().reset_index(),
                values='class',
                names='Launch Site',
                title='Total success launches by site')
            return fig
        else:
            filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
            df_r = filtered_df.value_counts('class')
            df_grouped = pd.DataFrame(
                {'class': [df_r.loc[0], df_r.loc[1]], 'name': [0, 1]})
            fig = px.pie(
                df_grouped,
                values='class',
                names='name',
                title=f'Total success launches for site {entered_site.upper()}')
            return fig

    @app.callback(Output(component_id='success-payload-scatter-chart',
                         component_property='figure'),
                  [Input(component_id='site-dropdown',
                         component_property='value'),
                   Input(component_id="payload-slider",
                         component_property="value")])
    def slide(entered_site, slide_values):
        slide_min = int(slide_values[0])
        slide_max = int(slide_values[1])
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= slide_min) & (
            spacex_df['Payload Mass (kg)'] <= slide_max)]
        if entered_site == 'ALL':
            fig = px.scatter(
                filtered_df,
                x="Payload Mass (kg)",
                y="class",
                color="Booster Version Category",
                title="Correlation between Payload and Success for all sites")
            return fig
        else:
            df = filtered_df[filtered_df['Launch Site'] == entered_site]
            fig = px.scatter(
                df,
                x="Payload Mass (kg)",
                y="class",
                color="Booster Version Category",
                title=f"Correlation between Payload and Success for {entered_site}")
            return fig
    return app.server


if __name__ == "__main__":
    app = Dash(__name__)
    app.run_server(debug=True)
