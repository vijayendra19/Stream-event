import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Function to send invitations
def send_invitations():
    st.write('### Send Invitations')
    event_options = [event['name'] for event in st.session_state['events']]
    selected_event = st.selectbox('Select Event', event_options)
    
    if st.button('Send Invitations'):
        event = next(event for event in st.session_state['events'] if event['name'] == selected_event)
        for guest in st.session_state['guests']:
            send_email(guest['email'], event)
        st.success('Invitations sent successfully!')

# Function to send email
def send_email(to_email, event):
    from_email = 'your_email@example.com'
    from_password = 'your_password'
    
    subject = f"Invitation to {event['name']}"
    body = f"""
    You are invited to {event['name']}!
    
    Date: {event['date']}
    Time: {event['time']}
    Location: {event['location']}
    
    Description:
    {event['description']}
    
    Please RSVP.
    """
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        st.write(f"Invitation sent to {to_email}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Function to track responses
def track_responses():
    st.write('### Events and Guest List')
    for event in st.session_state['events']:
        st.write(f"**Event Name:** {event['name']}")
        st.write(f"**Date:** {event['date']}")
        st.write(f"**Time:** {event['time']}")
        st.write(f"**Location:** {event['location']}")
        st.write(f"**Description:** {event['description']}")
        st.write('**Guest List:**')
        for guest in st.session_state['guests']:
            st.write(f"- {guest['name']} ({guest['email']})")
        st.write('---')

# Streamlit app layout
st.title('Event Planning App')

st.sidebar.title('Navigation')
option = st.sidebar.selectbox('Select a page:', ['Create Event', 'Manage Guests', 'Send Invitations', 'Track Responses'])

if option == 'Create Event':
    st.header('Create Event')
    create_event()
elif option == 'Manage Guests':
    st.header('Manage Guests')
    manage_guests()
elif option == 'Send Invitations':
    st.header('Send Invitations')
    send_invitations()
elif option == 'Track Responses':
    st.header('Track Responses')
    track_responses()
