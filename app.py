# Classic libraries
import os
import numpy as np
import pandas as pd
import flask
import io
import base64

# Logging information
import logging
import logzero
from logzero import logger

# Dash imports
import dash
import dash_core_components as dcc
import dash_html_components as html


# Custom function
import scripts.utils_covid as f

# Load pre computed data
world = f.load_pickle('world_info.p')

# Deployment inforamtion
PORT = 8050


############################################################################################
########################################## APP #############################################
############################################################################################

# Creating app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

# Associating server
server = app.server
app.title = 'COVID 19 - World cases'
app.config.suppress_callback_exceptions = True

css_directory = os.getcwd()
stylesheets = ['styles.css']
static_css_route = '/static/'


@app.server.route('{}<styles>'.format(static_css_route))
def serve_stylesheet(styles):
    if styles not in stylesheets:
        raise Exception(
            '"{}" is excluded from the allowed static files'.format(
                styles
            )
        )
    return flask.send_from_directory(css_directory, styles)

for styles in stylesheets:
    app.css.append_css({"external_url": "/static/{}".format(styles)})


def b64_image(image_filename): 
    with open(image_filename, 'rb') as f: image = f.read() 
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')
############################################################################################
######################################### LAYOUT ###########################################
############################################################################################


links = html.Div(
    id='platforms_links',
    children=[                   
        html.A(
            href='https://www.linkedin.com/in/anurag-sharma-0308/',
            children=[
                html.Img(src=b64_image('linkedin.png'), width=20, height=20),
                html.Span("Connect")
            ]
        ),
        html.A(
            href='https://github.com/anurag0308',
            children=[
                html.Img(src=b64_image('github.png'),width=20, height=20),
                # "Application code"
                html.Span("Code")
            ]
        ),
        html.A(
            href='https://public.opendatasoft.com/explore/dataset/covid-19-pandemic-worldwide-data/information/?disjunctive.zone&disjunctive.category&sort=date',
            children=[
                html.Img(src=b64_image('database.png'),width=20, height=20),
                # "Original COVID dataset"
                html.Span("Data")
            ],
        ),
    ],
)

app.layout = html.Div(
    children=[

        # HEADER
        html.Div(
            className="header",
            children=[
                html.H1("COVID 19 🦠 - Day to day evolution all over the world", className="header__text"),
                html.Span('(Last update: {})'.format(world['last_date'])),
                # html.Hr(),
            ],
        ),

        # CONTENT
        html.Section([
            
            # Line 1 : KPIS - World
            html.Div(
                id='world_line_1',
                children = [ 
                    html.Div(children = ['🚨 Confirmed', html.Br(), world['total_confirmed']], id='confirmed_world_total', className='mini_container'),
                    html.Div(children = ['🏡 Recovered', html.Br(), world['total_recovered']], id='recovered_world_total', className='mini_container'),
                    html.Div(children = [' ⚰️ Victims',   html.Br(), world['total_deaths']],    id='deaths_world_total',    className='mini_container'),            
                ],
            ),
            # html.Br(),
            links,

            # Line 2 : MAP - WORLD
            html.Div(
                id='world_line_2',
                children = [
                    dcc.Graph(id='world_map', figure=world['figure'], config={'scrollZoom': False}),         
                ],
            ),
            # html.Br(),
        ]),
    ],
)

############################################################################################
######################################### RUNNING ##########################################
############################################################################################

if __name__ == "__main__":
    
    # Display app start
    logger.error('*' * 80)
    logger.error('App initialisation')
    logger.error('*' * 80)

    # Starting flask server
    app.run_server(debug=True, port=PORT)