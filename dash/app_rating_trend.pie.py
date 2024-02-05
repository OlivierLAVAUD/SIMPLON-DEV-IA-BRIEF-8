import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client['biblio']

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[])

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
    html.Div(className="plot", children=[
        dcc.Graph(id='rating-pie-chart')
    ]),
])

@app.callback(
    Output('rating-pie-chart', 'figure'),
    Input('search-button', 'n_clicks')
)
def update_rating_pie_chart(n_clicks):
    data = list(db.books.find({}, {"_id": 0, "rating": 1}))
    df = pd.DataFrame(data)

    fig = px.pie(df, names='rating', title='Rating Distribution of Books')
 #   fig.update_xaxes(categoryorder="1","2","3","4","5")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color='white',
        font_color='white',
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
