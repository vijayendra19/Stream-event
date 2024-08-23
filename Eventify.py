import streamlit as st
import pandas as pd

# Initialize session state
if 'events' not in st.session_state:
    st.session_state['events'] = []
if 'guests' not in st.session_state:
    st.session_state['guests'] = []

# Function to create an event
def create_event():
    with st.form(key='event_form'):
        event_name = st.text_input('Event Name')
        event_date = st.date_input('Event Date')
        event_time = st.time_input('Event Time')
        event_location = st.text_input('Event Location')
        event_description = st.text_area('Event Description')
        submit_button = st.form_submit_button(label='Create Event')
        
        if submit_button:
            st.session_state['events'].append({
                'name': event_name,
                'date': event_date,
                'time': event_time,
                'location': event_location,
                'description': event_description
            })
            st.success('Event created successfully!')

# Function to manage guests
def manage_guests():
    with st.form(key='guest_form'):
        guest_name = st.text_input('Guest Name')
        guest_email = st.text_input('Guest Email')
        submit_button = st.form_submit_button(label='Add Guest')
        
        if submit_button:
            st.session_state['guests'].append({
                'name': guest_name,
                'email': guest_email
            })
            st.success('Guest added successfully!')

# Function to track responses
def track_responses():
    st.write('### Guest List')
    for guest in st.session_state['guests']:
        st.write(f"{guest['name']} ({guest['email']})")

# Streamlit app layout
st.title('Event Planning App')

st.sidebar.title('Navigation')
option = st.sidebar.selectbox('Select a page:', ['Create Event', 'Manage Guests', 'Track Responses'])

if option == 'Create Event':
    st.header('Create Event')
    create_event()
elif option == 'Manage Guests':
    st.header('Manage Guests')
    manage_guests()
elif option == 'Track Responses':
    st.header('Track Responses')
    track_responses()
