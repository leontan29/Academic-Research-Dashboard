from dash import Dash, html, dcc, State, Input, Output, callback, dash_table, ctx
import pandas as pd
import plotly.express as px
import mysql_util
import mongo_util
import neo4j_util
import chatgpt_util
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate



# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = Dash(__name__, external_stylesheets=external_stylesheets)

app = Dash(__name__, suppress_callback_exceptions=True)


colorscheme=px.colors.sequential.Oryel

def graph_top5kw():
    data = mysql_util.top5kw_per_year()
    data = [{'year': x[0], '#pub': x[2], 'keyword': x[1]} for x in data]
    fig = px.scatter(data, x='year', y='#pub', log_y=True, hover_name='keyword', color='#pub')
    return fig


def top_count_html(cnt, unit):
    text = [html.Strong(f'{cnt:,}'), html.Br(), unit]
    return text

app.layout = html.Div(
    className='container',
    children=[
        html.Div(className='title', children=[html.H1("Academic World")]),
        
        ###################
        # Top Count
        ###################
        html.Div(
            className='top_count_container',
            children=[
                widget_count_faculties := html.Div(
                    className='item',
                    children=top_count_html(mysql_util.count_faculties(), 'faculties')),
                widget_count_university := html.Div(
                    className='item',
                    children=top_count_html(mysql_util.count_universities(), 'universities')),
                widget_count_keywords := html.Div(
                    className='item',
                    children=top_count_html(mysql_util.count_keywords(), 'keywords')),
                widget_count_publications := html.Div(
                    className='item',
                    children=top_count_html(mysql_util.count_publications(), 'publications')),
            ]),
        
        ###################
        # Part 1
        ###################
        html.Div(
            className='part1',
            children=[
                ###################
                # Keyword Explorer
                ###################
                html.Div([
                    html.H2("Keyword Explorer"),
                    html.Div([
                        widget_kwexplorer__input := dcc.Input(type='text', value='data mining'),
                        widget_kwexplorer__button := html.Button(children="submit", n_clicks=0)]),
                    
                    # keyword trend in publications
                    html.Div([
                        widget_kwtrend__title := html.H3(),
                        widget_kwtrend__graph := dcc.Graph()],
                             className='item'),
                    
                    # top-10 prof by keyword
                    html.Div([
                        widget_top10_prof_krc__title := html.H3(),
                        widget_top10_prof_krc__graph := dcc.Graph()],
                             className='item'),
                    
                    # top-10 university by kyc
                    html.Div([
                        widget_top10_uni_krc__title := html.H3(),
                        widget_top10_uni_krc__graph := dcc.Graph()],
                             className='item'),
                    
                    # top-10 papers by kyc
                    html.Div([
                        widget_top10_paper_krc__title := html.H3(),
                        widget_top10_paper_krc__table := dash_table.DataTable(
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'maxWidth': '50em', 'whiteSpace': 'normal'})],
                             className='item'),
                    
                ], className='kwexplorer_container'),
                
                ###################
                # Contact List
                ###################
                
                html.Div([
                    html.H2("Faculty Contact Method"),
                    html.Div([
                        html.H3("Select a Keyword"),
                        dcc.Dropdown(
                            id='keyword-dropdown',
                            options=[],  # Options will be populated by the callback
                            value=None,
                            placeholder='Select a keyword'
                        )
                    ], className='item'),
                    
                    html.Div([
                        html.H3("Select a Faculty"),
                        dcc.Dropdown(
                            id='faculty-dropdown',
                            options=[],  # Options will be populated by the callback
                            value=None,
                            placeholder='Select a professor'
                        )
                    ], className='item'),
                    
                    # Container for faculty picture and contact information
                    html.Div([
                        html.Div([
                            html.H3("Faculty Picture"),
                            html.Img(
                                id='faculty-picture',
                                src='',
                                style={'height': '200px', 'width': '200px', 'object-fit': 'contain', 'display': 'block', 'margin': '0 auto'}
                            )
                        ], className='item'),
                        
                        html.Div([
                            html.H3("University Image"),
                            html.Img(
                                id='university-image',
                                src='',
                                style={'height': '200px', 'width': '200px', 'object-fit': 'contain', 'display': 'block', 'margin': '0 auto'}
                            )
                        ], className='item'),
                        
                        html.Div([
                            html.H3("Faculty Contact Information"),
                            dash_table.DataTable(
                                id='faculty-contact-table',
                                columns=[
                                    {"name": "Field", "id": "field"},
                                    {"name": "Value", "id": "value"}
                                ],
                                style_table={'overflowX': 'auto', 'overflowY': 'auto', 'maxHeight': '300px'},
                                style_cell={
                                    'textAlign': 'left',
                                    'maxWidth': '250px',
                                    'whiteSpace': 'normal',
                                    'padding': '10px'
                                },
                                style_header={
                                    'backgroundColor': 'lightgrey',
                                    'fontWeight': 'bold'
                                },
                                style_data={
                                    'backgroundColor': 'white',
                                    'color': 'black'
                                },
                                page_size=5  # Show all rows
                            )
                        ], className='item'),
                        
                        ##################
                        # For Add and Remove   
                        ################## 
                        html.Div([
                            html.H3("Contact List"),
                            dash_table.DataTable(
                                id='contact-list',
                                columns=[
                                    {"name": "Name", "id": "name"},
                                    #{"name": "University", "id": "university"}
                                ],
                                style_table={'overflowX': 'auto', 'overflowY': 'auto', 'maxHeight': '300px'},
                                style_cell={
                                    'textAlign': 'left',
                                    'maxWidth': '250px',
                                    'whiteSpace': 'normal',
                                    'padding': '10px'
                                },
                                style_header={
                                    'backgroundColor': 'lightgrey',
                                    'fontWeight': 'bold'
                                },
                                style_data={
                                    'backgroundColor': 'white',
                                    'color': 'black'
                                },
                                editable=False,
                                row_deletable=True,
                                selected_rows=[],
                                page_size=5
                            ),
                            
                            dbc.Button("Add", id="add-to-contact-list", n_clicks=0),
                            dbc.Button("Remove", id="remove-from-contact-list", n_clicks=0),
                        ], className='item'),
                    ]),
                    
                    # Hidden div to store the previous clicks
                    dcc.Store(id='prev-clicks', data={'add': 0, 'remove': 0})
                    
                ], className='contact_list_container'),
                
            ]),
        
        
        ###################
        # Part 2
        ###################
        html.Div(
            className='part2',
            children=[
                ###################
                # Keyword Search
                ###################
                html.Div(
                    className='kwsearch_container',
                    children=[
                        html.H2("Keyword Search"),
                        html.Div([
                            widget_kwsearch__input := dcc.Input(type='text', value='data mining'),
                            widget_kwsearch__button := html.Button('filter', n_clicks=0)]),
                        
                        widget_kwsearch__table := dash_table.DataTable(
                            style_cell={'textAlign': 'left'},
                            style_table={'height': '20em', 'overflowY': 'auto'}),
                    ]),
                
                html.Div(
                    className='top5kw_container',
                    children=[
                        html.H2("Top-5 keywords over time"),
                        dcc.Graph(figure=graph_top5kw()),
                    ]), 
                
                html.Div(
                    className='rlist_container',
                    children=[
                        html.H2("Reading List"),
                        html.Div([
                            widget_rlist__input := dcc.Input(type='text', value='', placeholder='Title'),
                            widget_rlist__add := html.Button('add', id='add', n_clicks=0),
                            widget_rlist__table := dash_table.DataTable(
                                id='table',
                                row_deletable=True,
                                style_cell={'textAlign': 'left'},
                                style_table={'maxHeight': '20em', 'overflowY': 'auto'}),
                            html.Div([widget_rlist__summary := dcc.Markdown()],
                                     className='rlist_summary')
                        ]),
                    ]),
            ]),
        
        
        ##################
        #  Part 3
        ##################
        html.Div(
            className='part3',
            children=[
                html.Div(
                    className='recommended_reading_list_container',
                    children=[
                        html.H2("Recommend Reading List"),
                        html.Div([
                            html.H3("Select a Keyword"),
                            dcc.Dropdown(
                                id='keyword-dropdown-reading-list',
                                options=[{'label': 'Keyword 1', 'value': 'keyword1'}, {'label': 'Keyword 2', 'value': 'keyword2'}],
                                placeholder='Select a keyword'
                            )
                        ], className='item'),
                        html.Div([
                            html.H3("Select Year Range"),
                            dcc.RangeSlider(
                                id='year-range-slider',
                                min=2000,
                                max=2024,
                                step=1,
                                value=[2000, 2024],
                                marks={i: str(i) for i in range(2000, 2024)}
                            )
                        ], className='item'),
                        html.Div([
                            html.H3("Select a Paper"),
                            dash_table.DataTable(
                                id='top-papers-table',
                                columns=[
                                    {"name": "Title", "id": "title"},
                                    {"name": "Author", "id": "author"},
                                    {"name": "School", "id": "school"},
                                    {"name": "Score", "id": "score"},
                                    {"name": "Year", "id": "year"}
                                ],
                                data=[],
                                style_table={'overflowX': 'auto', 'overflowY': 'auto', 'maxHeight': '300px'},
                                style_cell={
                                    'textAlign': 'left',
                                    'maxWidth': '250px',
                                    'whiteSpace': 'normal',
                                    'padding': '10px'
                                },
                                style_header={
                                    'backgroundColor': 'lightgrey',
                                    'fontWeight': 'bold'
                                },
                                style_data={
                                    'backgroundColor': 'white',
                                    'color': 'black'
                                },
                                row_selectable='single',
                                selected_rows=[],  # For selecting rows
                                page_size=15  # Show all rows
                            ),
                            html.Div(id='no-papers-message', style={'color': 'red'})
                        ], className='item'),
                        
                        html.Div([
                            dbc.Button("Add to Reading List", id="add-to-reading-list", n_clicks=0),
                            dbc.Button("Remove from Reading List", id="remove-from-reading-list", n_clicks=0),
                        ], className='item'),
                        
                        html.Div([
                            html.H3("Personal Reading List"),
                            dash_table.DataTable(
                                id='reading-list-table',
                                columns=[
                                    {"name": "Title", "id": "title"},
                                    {"name": "Author", "id": "author"},
                                    {"name": "School", "id": "school"},
                                    {"name": "Score", "id": "score"},
                                    {"name": "Year", "id": "year"}
                                ],
                                style_table={'overflowX': 'auto', 'overflowY': 'auto', 'maxHeight': '300px'},
                                style_cell={
                                    'textAlign': 'left',
                                    'maxWidth': '250px',
                                    'whiteSpace': 'normal',
                                    'padding': '10px'
                                },
                                style_header={
                                    'backgroundColor': 'lightgrey',
                                    'fontWeight': 'bold'
                                },
                                style_data={
                                    'backgroundColor': 'white',
                                    'color': 'black'
                                },
                                row_deletable=True,
                                page_size=10
                            ),
                            
                        ], className='item'),
                        
                        dcc.Store(id='reading-list', data=[])
                    ]),
                ]),
        
        dcc.Store(id='faculty_contact_list', data=[]),
        dcc.Store(id='contact_list', data=[]),
        dcc.Store(id='faculty-data', data=[]),
    ])


##################################
#  Call Back Section
####################################
   
@app.callback(
    Output(component_id='keyword-scores', component_property='figure'),
    [Input(component_id='university', component_property='value')]
)
def update_keyword_scores(university):
    df = neo4j_util.get_keyword_scores_by_school(university)
    fig = {
        'data': [{
            'values': df['total score'],
            'labels': df['keyword'],
            'type': 'pie',
            'marker': {'colors': ['blue', 'red', 'green', 'orange', 'purple', 'pink', 'brown', 'gray', 'yellow', 'teal']}
        }],
        'layout': {
            'title': f'Top 10 keyword scores for {university}'
        }
    }
    return fig

##################################
#  Keyword Search
@callback(
    Output(widget_kwsearch__table, 'data'),
    Input(widget_kwsearch__button, 'n_clicks'),
    State(widget_kwsearch__input, 'value'))
def widget_kwsearch__callback(n_clicks, input):
    data = mysql_util.kw_search(input)
    table= [{'keyword':x} for x in data]
    return table
    
##################################
#  Keyword Explorer - kwtrend widget
@callback(
    Output(widget_kwtrend__title, 'children'),
    Output(widget_kwtrend__graph, 'figure'),
    Input(widget_kwexplorer__button, 'n_clicks'),
    State(widget_kwexplorer__input, 'value'))
def widget_kwtrend__callback(n_clicks, input):
    #data = mysql_util.count_publications_by_keyword(input);
    data = mongo_util.count_publications_by_keyword(input);
    df = pd.DataFrame(data, columns=['year', '#publications'])
    fig = px.line(df, x='year', y='#publications', color_discrete_sequence=[colorscheme[0]])
    title = ['Publications with Keyword ', html.U(input)]
    return title, fig

##################################
#  Keyword Explorer - top10 professor widget
@callback(
    Output(widget_top10_prof_krc__title, 'children'),
    Output(widget_top10_prof_krc__graph, 'figure'),
    Input(widget_kwexplorer__button, 'n_clicks'),
    State(widget_kwexplorer__input, 'value'))
def widget_top10_prof_krc__callback(n_clicks, input):
    #data = mysql_util.count_publications_by_keyword(input);
    data = mysql_util.top10_professor_by_krc(input);
    df = pd.DataFrame(data, columns=['name', 'krc'])
    fig = px.pie(df, values='krc', names='name', color_discrete_sequence=colorscheme)
    fig.update_traces(textinfo='none')
    title = ['Top-10 Professors by Keyword ', html.U(input)]
    return title, fig

##################################
#  Keyword Explorer - top10 university widget
@callback(
    Output(widget_top10_uni_krc__title, 'children'),
    Output(widget_top10_uni_krc__graph, 'figure'),
    Input(widget_kwexplorer__button, 'n_clicks'),
    State(widget_kwexplorer__input, 'value'))
def widget_top10_uni_krc__callback(n_clicks, input):
    data = neo4j_util.top10_university_by_krc(input)
    df = pd.DataFrame(data, columns=['name', 'krc'])
    fig = px.pie(df, values='krc', names='name', color_discrete_sequence=colorscheme)
    fig.update_traces(textinfo='none')
    title = ['Top-10 Universities by Keyword ', html.U(input)]
    return title, fig


##################################
#  Keyword Explorer - top10 papers widget
@callback(
    Output(widget_top10_paper_krc__title, 'children'),
    Output(widget_top10_paper_krc__table, 'data'),
    Input(widget_kwexplorer__button, 'n_clicks'),
    State(widget_kwexplorer__input, 'value'))
def widget_top10_paper_krc__callback(n_clicks, input):
    #data = [(f'paper{x}', (x+1)*100) for x in range(10)]
    data = neo4j_util.top10_paper_by_krc(input)
    table = [{'title':title, 'krc':krc} for title, krc in data]
    title = ['Top-10 Papers by Keyword ', html.U(input)]
    return title, table


##################################
#  Contact Information

@callback(
    Output('keyword-dropdown', 'options'),
    Input(widget_kwsearch__table, 'data'))
def update_keyword_dropdown(table_data):
    # Extract the list of keywords from the table data
    keywords = [row['keyword'] for row in table_data]
    
    # Format the options for the dropdown
    options = [{'label': keyword, 'value': keyword} for keyword in keywords]
    
    return options

@callback(
    Output('faculty-dropdown', 'options'),
    Input('keyword-dropdown', 'value')
)
def update_faculty_dropdown(selected_keyword):
    if not selected_keyword:
        return [{'label': 'No faculty found', 'value': ''}]
    faculties = mysql_util.top10_professor_by_krc(selected_keyword)
    return [{'label': faculty, 'value': faculty} for faculty, _ in faculties]

@callback(
    [Output('faculty-picture', 'src'),
     Output('university-image', 'src'),
     Output('faculty-contact-table', 'data')],
    Input('faculty-dropdown', 'value')
)
def update_faculty_info(selected_faculty):
    if not selected_faculty:
        return '', '', []

    # Retrieve faculty details
    faculty_details = mysql_util.get_faculty_details(selected_faculty)

    if faculty_details is None:
        return '', '', []

    picture_src = faculty_details.get('PictureURL', '')
    print('faculty_details:', faculty_details)
    university_name = faculty_details.get('University', 'Unknown University')

    # Retrieve university image URL
    university_image_url = mysql_util.get_university_image_url(university_name)

    faculty_info = [
        {'field': 'Name', 'value': faculty_details.get('FacultyName', '')},
        {'field': 'Position', 'value': faculty_details.get('Position', '')},
        {'field': 'Phone', 'value': faculty_details.get('Phone', '')},
        {'field': 'University', 'value': faculty_details.get('University', 'Unknown University')},
        {'field': 'Email', 'value': faculty_details.get('Email', '')}
    ]

    return picture_src, university_image_url, faculty_info

#add or remove from contact list
@app.callback(
    Output('contact-list', 'data'),
    Output('prev-clicks', 'data'),
    Input('add-to-contact-list', 'n_clicks'),
    Input('remove-from-contact-list', 'n_clicks'),
    State('faculty-dropdown', 'value'),
    State('contact-list', 'data'),
    State('prev-clicks', 'data')
)
def update_contact_list(add_clicks, remove_clicks, selected_faculty, contact_list, prev_clicks):
    # Initialize list if None
    if contact_list is None:
        contact_list = []

    # Handle add
    if add_clicks > prev_clicks['add'] and selected_faculty:
        # Avoid duplicates
        if not any(faculty['name'] == selected_faculty for faculty in contact_list):
            contact_list.append({'name': selected_faculty})
        prev_clicks['add'] = add_clicks

    # Handle remove
    if remove_clicks > prev_clicks['remove']:
        contact_list = [faculty for faculty in contact_list if faculty['name'] != selected_faculty]
        prev_clicks['remove'] = remove_clicks

    return contact_list, prev_clicks

##################################
#  Reading List
@callback(
    Output(widget_rlist__table, 'data'),
    Input(widget_rlist__add, 'n_clicks'),
    Input(widget_rlist__table, 'data'),
    State(widget_rlist__table, 'data_previous'),
    State(widget_rlist__input, 'value'))
def widget_rlist__callback(add_button, table_data, table_data_prev, input):
    triggered_id = ctx.triggered_id
    print('triggered_id', triggered_id)
    if triggered_id == 'add':
        p = mysql_util.get_publication(input)
        print('p', p);
        print('input', input)
        mysql_util.rlist_add(p)
    elif triggered_id == 'del':
        p = mysql_util.get_publication(input)
        mysql_util.rlist_del(p, input)
    elif triggered_id == 'table':
        for row in table_data_prev:
            if row in table_data: continue
            # deleted row
            print('removed: ', row)
            mysql_util.rlist_del(row['paper'])

    # reload data
    data = mysql_util.rlist_get()
    table= [{'paper':x} for x in data]
    return table

@callback(
    Output(widget_rlist__summary, 'children'),
    Input(widget_rlist__table, 'active_cell'),
    State(widget_rlist__table, 'data'))
def widget_rlist__alert(active_cell, data):
    if not active_cell: return ""
    item = data[active_cell['row']]['paper']
    summary = mysql_util.rlist_summary_get(item)
    if not summary:
        summary = chatgpt_util.get_summary(item)
        mysql_util.rlist_summary_set(item, summary)

    print('summary:', summary)
    return summary


###################
#Recommand List
###################

@app.callback(
    Output('keyword-dropdown-reading-list', 'options'),
    Input(widget_kwsearch__table, 'data')
)
def update_keyword_reading_list_dropdown(table_data):
    if not table_data:
        return []
    keywords = [row['keyword'] for row in table_data]
    options = [{'label': keyword, 'value': keyword} for keyword in keywords]
    return options


@app.callback(
    [Output('top-papers-table', 'data'),
     Output('no-papers-message', 'children')],
    [Input('keyword-dropdown-reading-list', 'value'),
     Input('year-range-slider', 'value')]
)
def update_top_papers_table(selected_keyword, selected_years):


    if not selected_keyword:
        return [], "Please select a keyword to see the papers."

    # Ensure selected_years is a list with two elements
    if len(selected_years) != 2:
        return [], "Invalid year range selected."

    # Extract start and end years
    start_year, end_year = selected_years

    # Fetch top papers based on keyword and year range
    top_papers_df = mysql_util.get_top_papers_by_keyword_and_year(selected_keyword, start_year, end_year)
    
    # Check if DataFrame is empty
    if top_papers_df.empty:
        return [], "No papers available for the selected criteria."
    
    # Convert DataFrame to dictionary for DataTable
    top_papers_data = top_papers_df.to_dict('records')
    return top_papers_data, ""


@app.callback(
    [Output('reading-list', 'data'),
     Output('reading-list-table', 'data')],
    [Input('add-to-reading-list', 'n_clicks'),
     Input('remove-from-reading-list', 'n_clicks')],
    [State('top-papers-table', 'selected_rows'),
     State('top-papers-table', 'data'),
     State('reading-list', 'data')]
)
def update_reading_list(add_clicks, remove_clicks, selected_rows, papers_data, current_list):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    # Extract the triggered button
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if not papers_data:
        raise PreventUpdate

    # Ensure current_list is initialized
    if current_list is None:
        current_list = []

    # Initialize the updated list with current list
    updated_list = current_list.copy()

    if selected_rows:
        selected_row = selected_rows[0]
        paper_to_manage = papers_data[selected_row]  # Get the paper from the selected row

        if triggered_id == 'add-to-reading-list' and add_clicks:
            # Add paper to the reading list
            if paper_to_manage not in updated_list:
                updated_list.append(paper_to_manage)
                print(f"Added paper: {paper_to_manage}")  # Debugging line

        if triggered_id == 'remove-from-reading-list' and remove_clicks:
            # Remove paper from the reading list
            if paper_to_manage in updated_list:
                updated_list.remove(paper_to_manage)
                print(f"Removed paper: {paper_to_manage}")  # Debugging line

    return updated_list, updated_list


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
