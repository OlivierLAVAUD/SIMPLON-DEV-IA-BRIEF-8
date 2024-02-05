import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import pymongo
from app_category_trend_hist import app as category_app
# from app_price_trend_hist_perc import app price_trend_hist_perc as price_trend_hist_perc
from app_price_trend import app as price_app


from app_rating_trend_hist import app as rating_app

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client['biblio']

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=['assets/style.css'], suppress_callback_exceptions=True)

app.layout = html.Div(className="container", children=[
    html.Div(className="navbar", children=[
        html.Div(id='logo', className='logo', children=[
            html.Img(src='assets/icons/logo.svg', alt=''),
            html.H1("Bookle"),
        ]),
        html.Div(className='searchbarContainer', children=[
            dcc.Input(id='search-input', type='text', placeholder='Enter book title'),
            html.Button(id='search-button', className="search-button", children=[
                html.Img(src="assets/icons/search_icon.svg", className="button-image")
            ]),
        ]),
    ]),
    
    html.Div(className='resultsContainer', children=[
        html.Div(className='search-results', children=[
            html.Div(id='search-output'),
        ]),
        html.Div(id='book-details', className='book-details')
    ]),
    
    html.Div(className="trends-container", children=[
        html.Div(className="trend-item", children=[
            dcc.Graph(id='category-plot')
        ]),
        html.Div(className="trend-item", children=[
            dcc.Graph(id='price-trend-plot')
        ]),
        html.Div(className="trend-item", children=[
            dcc.Graph(id='rating-trend-plot')
        ]),
    ]),
])

# Callbacks
@app.callback(
    Output('category-plot', 'figure'),
    Input('search-button', 'n_clicks')
)
def update_category_plot(n_clicks):
    return category_app.callback_map['update_category_plot']('clicks')(n_clicks)

@app.callback(
    Output('price-trend-plot', 'figure'),
    Input('search-button', 'n_clicks')
)
def update_price_trend_plot(n_clicks):
    return price_app.callback_map['update_price_trend_plot']('clicks')(n_clicks)

@app.callback(
    Output('rating-trend-plot', 'figure'),
    Input('search-button', 'n_clicks')
)
def update_rating_trend_plot(n_clicks):
    return rating_app.callback_map['update_rating_trend_plot']('clicks')(n_clicks)

if __name__ == '__main__':
    app.run_server(debug=True)
