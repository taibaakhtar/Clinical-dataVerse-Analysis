# import dash
# from dash import dcc, html, Input, Output
# import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.express as px
# from wordcloud import WordCloud
# import base64
# from io import BytesIO
# import pickle
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# import os
# import datetime as dt

# # Load preprocessed data
# with open('D:/Data Science projects/assignment/2.o/data.pkl', 'rb') as file:
#     data = pickle.load(file)

# # Define symptoms for dropdown
# symptoms = ['Bleeding', 'Chills', 'Cough', 'Diarrhea', 'Dizziness', 'Dyspnea', 'Fatigue', 'Fever', 'Headache',
#             'Loss of appetite', 'Nausea', 'Numbness', 'Pain', 'Rash', 'Seizure', 'Shortness of breath', 'Sweating',
#             'Swelling', 'Tingling', 'Vomiting', 'Weakness', 'Stress']

# # Google Calendar API setup
# SCOPES = ['https://www.googleapis.com/auth/calendar']


# def authenticate_google_calendar():
#     """Authenticate and return Google Calendar API service."""
#     creds = None
#     if os.path.exists('token.json'):
#         from google.oauth2.credentials import Credentials
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)

#     if not creds or not creds.valid:
#         flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
#         creds = flow.run_local_server(port=0)
#         with open('token.json', 'w') as token_file:
#             token_file.write(creds.to_json())

#     return build('calendar', 'v3', credentials=creds)


# service = authenticate_google_calendar()


# # Generate WordCloud
# def generate_wordcloud(text):
#     wc = WordCloud(background_color='white', width=800, height=400).generate(' '.join(text))
#     img = BytesIO()
#     wc.to_image().save(img, format='PNG')
#     img.seek(0)
#     return base64.b64encode(img.read()).decode('utf-8')


# # Determine Risk Level
# def determine_risk(symptoms, conditions):
#     high_risk_conditions = {'cancer', 'stroke', 'ARDS', 'failure', 'pneumonia'}
#     high_risk_symptoms = {'seizure', 'shortness of breath', 'numbness', 'vomiting', 'fatigue'}
#     medium_risk_conditions = {'diabetes', 'hypertension', 'metastases'}

#     if any(condition in high_risk_conditions for condition in conditions) or \
#             len([symptom for symptom in symptoms if symptom in high_risk_symptoms]) >= 2:
#         return "High"
#     elif any(condition in medium_risk_conditions for condition in conditions) or \
#             len([symptom for symptom in symptoms if symptom in high_risk_symptoms]) == 1:
#         return "Medium"
#     else:
#         return "Low"


# # Prepare data for visualizations
# symptom_counts = data['symptoms'].explode().value_counts().reset_index()
# symptom_counts.columns = ['Symptom', 'Count']

# disease_counts = data['diseases'].explode().value_counts().reset_index()
# disease_counts.columns = ['Disease', 'Count']

# gender_counts = data['gender'].value_counts().reset_index()
# gender_counts.columns = ['Gender', 'Count']

# age_distribution = data['age'].dropna()

# # Initialize Dash app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# server = app.server

# # App layout
# app.layout = dbc.Container([
#     dbc.Row([
#         # Sidebar
#         dbc.Col([
#             html.H5("Clinical Dataverse Analytics", style={'color': '#2c8cff'}),
#             html.H3("High-Risk Patient Identification", className="mt-4"),
#             dcc.Dropdown(
#                 options=[{'label': symptom, 'value': symptom} for symptom in symptoms],
#                 id='high-risk-filter', multi=True, placeholder="Filter by Symptoms"
#             ),
#             html.Div(id='high-risk-output', className='mt-3'),
#             dcc.DatePickerSingle(
#                 id='meeting-date',
#                 date=None,
#                 display_format='YYYY-MM-DD',
#                 className="mt-3"
#             ),
#             html.Button("Schedule Meeting", id='schedule-button', n_clicks=0, className='btn btn-primary mt-3'),
#             html.Div(id='schedule-output', className='mt-3')
#         ], width=3, className="bg-light p-3 vh-100 border-end"),

#         # Main content
#         dbc.Col([
#             html.H1("Doctor-Patient Conversation Dashboard", className="text-center my-4"),
#             html.Hr(),
#             # Overview section
#             dbc.Row([
#                 dbc.Col(dbc.Card(dbc.CardBody([
#                     html.H4("Overview", className="card-title"),
#                     html.P(f"Total Conversations: {len(data)}"),
#                     html.P(f"Unique Symptoms: {len(set([item for sublist in data['symptoms'] for item in sublist]))}"),
#                     html.P(f"Unique Diseases: {len(set([item for sublist in data['diseases'] for item in sublist]))}")
#                 ])), width=3),

#                 dbc.Col(dcc.Graph(
#                     id='symptom-bar-chart',
#                     figure=px.bar(symptom_counts, x='Symptom', y='Count', title="Most Common Symptoms")
#                 ), width=7)
#             ]),

#             # WordCloud and Disease Pie Chart
#             dbc.Row([
#                 dbc.Col([
#                     html.H4("Symptom Word Cloud"),
#                     html.Img(src=f"data:image/png;base64,{generate_wordcloud([item for sublist in data['symptoms'] for item in sublist])}", style={"width": "70%"})
#                 ], width=6),

#                 dbc.Col(dcc.Graph(
#                     id='disease-trends',
#                     figure=px.pie(disease_counts, names='Disease', values='Count', title="Disease Distribution")
#                 ), width=6)
#             ]),

#             # Age and Gender Distribution
#             dbc.Row([
#                 dbc.Col(dcc.Graph(
#                     id='gender-pie-chart',
#                     figure=px.pie(gender_counts, names='Gender', values='Count', title="Gender Distribution")
#                 ), width=6),

#                 dbc.Col(dcc.Graph(
#                     id='age-histogram',
#                     figure=px.histogram(age_distribution, x=age_distribution, nbins=20, title="Age Distribution",
#                                         labels={'x': 'Age', 'y': 'Count'})
#                 ), width=6)
#             ])
#         ], width=9)
#     ])
# ], fluid=True)


# @app.callback(
#     [Output('high-risk-output', 'children'), Output('schedule-output', 'children')],
#     [Input('high-risk-filter', 'value'), Input('schedule-button', 'n_clicks'), Input('meeting-date', 'date')]
# )
# def identify_high_risk(selected_symptoms, n_clicks, meeting_date):
#     if selected_symptoms:
#         filtered = data[data['symptoms'].apply(lambda x: all(symptom in x for symptom in selected_symptoms))]
#         if not filtered.empty:
#             filtered['Risk Level'] = filtered.apply(lambda row: determine_risk(row['symptoms'], row['diseases']), axis=1)

#             risk_message = html.Div([
#                 html.P(f"Patients at risk: {len(filtered)}"),
#                 html.Table([
#                     html.Thead(html.Tr([html.Th("Patient ID"), html.Th("Summary"), html.Th("Risk Level")])),
#                     html.Tbody([
#                         html.Tr([html.Td(row['serial_number']), html.Td(row['data']), html.Td(row['Risk Level'])]) 
#                         for _, row in filtered.iterrows()
#                     ])
#                 ])
#             ])
#             if n_clicks > 0:
#                 if not meeting_date:
#                     return risk_message, html.P("Please select a date for the meeting.")

#                 day_of_week = dt.datetime.strptime(meeting_date, '%Y-%m-%d').strftime('%A')
#                 if day_of_week == "Sunday":
#                     return risk_message, html.P("Sunday, doctors are not available.")

#                 # Schedule meetings with a 30-minute interval
#                 start_time = dt.datetime.strptime(f"{meeting_date} 6:00:00", '%Y-%m-%d %H:%M:%S')
#                 for i, (_, row) in enumerate(filtered.iterrows()):
#                     event = {
#                         'summary': f"Patient {row['serial_number']} ({row['Risk Level']} Risk) Appointment",
#                         'description': f"Patient Data: {row['data']}",
#                         'start': {'dateTime': (start_time + dt.timedelta(minutes=30 * i)).isoformat(), 'timeZone': 'America/New_York'},
#                         'end': {'dateTime': (start_time + dt.timedelta(minutes=30 * i + 30)).isoformat(), 'timeZone': 'America/New_York'}
#                     }
#                     service.events().insert(calendarId='primary', body=event).execute()

#                 return risk_message, html.P(f"Meetings scheduled for {len(filtered)} patients on {meeting_date}.")
#             return risk_message, None
#         return html.P("No patients found."), None
#     return html.P("Select symptoms."), None


# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import base64
from io import BytesIO
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import datetime as dt

# Load preprocessed data
with open('D:/Data Science projects/assignment/2.o/data.pkl', 'rb') as file:
    data = pickle.load(file)

# Define symptoms for dropdown
symptoms = ['Bleeding', 'Chills', 'Cough', 'Diarrhea', 'Dizziness', 'Dyspnea', 'Fatigue', 'Fever', 'Headache',
            'Loss of appetite', 'Nausea', 'Numbness', 'Pain', 'Rash', 'Seizure', 'Shortness of breath', 'Sweating',
            'Swelling', 'Tingling', 'Vomiting', 'Weakness', 'Stress']

# Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate_google_calendar():
    """Authenticate and return Google Calendar API service."""
    creds = None
    if os.path.exists('token.json'):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


service = authenticate_google_calendar()


# Generate WordCloud
def generate_wordcloud(text):
    wc = WordCloud(background_color='white', width=800, height=400).generate(' '.join(text))
    img = BytesIO()
    wc.to_image().save(img, format='PNG')
    img.seek(0)
    return base64.b64encode(img.read()).decode('utf-8')


# Determine Risk Level
def determine_risk(symptoms, conditions):
    high_risk_conditions = {'cancer', 'stroke', 'ARDS', 'failure', 'pneumonia'}
    high_risk_symptoms = {'seizure', 'shortness of breath', 'numbness', 'vomiting', 'fatigue'}
    medium_risk_conditions = {'diabetes', 'hypertension', 'metastases'}

    if any(condition in high_risk_conditions for condition in conditions) or \
            len([symptom for symptom in symptoms if symptom in high_risk_symptoms]) >= 2:
        return "High"
    elif any(condition in medium_risk_conditions for condition in conditions) or \
            len([symptom for symptom in symptoms if symptom in high_risk_symptoms]) == 1:
        return "Medium"
    else:
        return "Low"


# Prepare data for visualizations
symptom_counts = data['symptoms'].explode().value_counts().reset_index()
symptom_counts.columns = ['Symptom', 'Count']

disease_counts = data['diseases'].explode().value_counts().reset_index()
disease_counts.columns = ['Disease', 'Count']

gender_counts = data['gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count']

age_distribution = data['age'].dropna()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

# App layout
app.layout = dbc.Container([
    dbc.Row([
        # Sidebar
        dbc.Col([
            html.H4("Clinical Dataverse Analytics", className="text-primary text-center mb-4"),
            html.H3("High-Risk Patient Identification", className="text-center mb-4"),
            dbc.Card([
                dbc.CardBody([
                    html.Label("Filter by Symptoms", className="form-label text-secondary"),
                    dcc.Dropdown(
                        options=[{'label': symptom, 'value': symptom} for symptom in symptoms],
                        id='high-risk-filter', multi=True, placeholder="Select Symptoms",
                        className="mb-3"
                    ),
                    html.Label("Select Meeting Date", className="form-label text-secondary"),
                    dcc.DatePickerSingle(
                        id='meeting-date',
                        date=None,
                        display_format='YYYY-MM-DD',
                        className="mb-3"
                    ),
                    html.Button("Schedule Meeting", id='schedule-button', n_clicks=0, className="btn btn-primary w-100 mb-3"),
                    html.Div(id='schedule-output', className="mt-3")
                ])
            ], className="p-3 mb-4 shadow"),
            html.Div(id='high-risk-output', className="mt-3")
        ], width=3, className="bg-light p-3 vh-100 border-end"),

        # Main content
        dbc.Col([
            html.H1("Doctor-Patient Conversation Dashboard", className="text-center my-4 text-primary"),
            html.Hr(),
            # Overview section
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H4("Overview", className="card-title text-center text-secondary"),
                    html.P(f"Total Conversations: {len(data)}", className="text-center"),
                    html.P(f"Unique Symptoms: {len(set([item for sublist in data['symptoms'] for item in sublist]))}", className="text-center"),
                    html.P(f"Unique Diseases: {len(set([item for sublist in data['diseases'] for item in sublist]))}", className="text-center")
                ]), className="shadow-sm"), width=4),

                dbc.Col(dcc.Graph(
                    id='symptom-bar-chart',
                    figure=px.bar(symptom_counts, x='Symptom', y='Count', title="Most Common Symptoms")
                ), width=8)
            ], className="mb-4"),

            # WordCloud and Disease Pie Chart
            dbc.Row([
                dbc.Col([
                    html.H4("Symptom Word Cloud", className="text-secondary text-center"),
                    html.Img(src=f"data:image/png;base64,{generate_wordcloud([item for sublist in data['symptoms'] for item in sublist])}", 
                             style={"width": "90%", "margin": "auto", "display": "block"})
                ], width=6, className="shadow-sm"),

                dbc.Col(dcc.Graph(
                    id='disease-trends',
                    figure=px.pie(disease_counts, names='Disease', values='Count', title="Disease Distribution")
                ), width=6)
            ], className="mb-4"),

            # Age and Gender Distribution
            dbc.Row([
                dbc.Col(dcc.Graph(
                    id='gender-pie-chart',
                    figure=px.pie(gender_counts, names='Gender', values='Count', title="Gender Distribution")
                ), width=6, className="shadow-sm"),

                dbc.Col(dcc.Graph(
                    id='age-histogram',
                    figure=px.histogram(age_distribution, x=age_distribution, nbins=20, title="Age Distribution",
                                        labels={'x': 'Age', 'y': 'Count'})
                ), width=6, className="shadow-sm")
            ])
        ], width=9)
    ])
], fluid=True)

# Callbacks remain unchanged
@app.callback(
    [Output('high-risk-output', 'children'), Output('schedule-output', 'children')],
    [Input('high-risk-filter', 'value'), Input('schedule-button', 'n_clicks'), Input('meeting-date', 'date')]
)
def identify_high_risk(selected_symptoms, n_clicks, meeting_date):
    if selected_symptoms:
        filtered = data[data['symptoms'].apply(lambda x: all(symptom in x for symptom in selected_symptoms))]
        if not filtered.empty:
            filtered['Risk Level'] = filtered.apply(lambda row: determine_risk(row['symptoms'], row['diseases']), axis=1)

            risk_message = html.Div([
                html.P(f"Patients at risk: {len(filtered)}", className="text-secondary"),
                html.Table([
                    html.Thead(html.Tr([html.Th("Patient ID"), html.Th("Summary"), html.Th("Risk Level")])),
                    html.Tbody([
                        html.Tr([html.Td(row['serial_number']), html.Td(row['data']), html.Td(row['Risk Level'])]) 
                        for _, row in filtered.iterrows()
                    ])
                ])
            ])
            if n_clicks > 0:
                if not meeting_date:
                    return risk_message, html.P("Please select a date for the meeting.", className="text-danger")

                day_of_week = dt.datetime.strptime(meeting_date, '%Y-%m-%d').strftime('%A')
                if day_of_week == "Sunday":
                    return risk_message, html.P("Sunday, doctors are not available.", className="text-warning")

                start_time = dt.datetime.strptime(f"{meeting_date} 6:00:00", '%Y-%m-%d %H:%M:%S')
                for i, (_, row) in enumerate(filtered.iterrows()):
                    event = {
                        'summary': f"Patient {row['serial_number']} ({row['Risk Level']} Risk) Appointment",
                        'description': f"Patient Data: {row['data']}",
                        'start': {'dateTime': (start_time + dt.timedelta(minutes=30 * i)).isoformat(), 'timeZone': 'America/New_York'},
                        'end': {'dateTime': (start_time + dt.timedelta(minutes=30 * i + 30)).isoformat(), 'timeZone': 'America/New_York'}
                    }
                    service.events().insert(calendarId='primary', body=event).execute()

                return risk_message, html.P(f"Meetings scheduled for {len(filtered)} patients on {meeting_date}.", className="text-success")
            return risk_message, None
        return html.P("No patients found.", className="text-warning"), None
    return html.P("Select symptoms.", className="text-secondary"), None


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
