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
        dcc.Graph(id='category-histogram')
    ]),
])

@app.callback(
    Output('category-histogram', 'figure'),
    Input('search-button', 'n_clicks')
)
def update_category_histogram(n_clicks):
    data = list(db.books.find({}, {"_id": 0, "category": 1}))
    df = pd.DataFrame(data)
    
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['category', 'count']

    fig = px.bar(category_counts, x='count', y='category', orientation='h', title='Number of Books per Category')
#    fig = px.bar(category_counts, x='category', y='count', orientation='h', title='Number of Books per Category')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color='white',
        font_color='white',
        xaxis=dict(color='white'),
        yaxis=dict(color='white'),
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
