import openai
import streamlit as st
# import sqlite3
from datetime import datetime
import sqlalchemy
import mysql.connector

if 'last_submission' not in st.session_state:
    st.session_state.last_submission = ''
if 'widget_value' not in st.session_state:
    st.session_state.widget_value = ''

# If messages does not exist in state, initialize it
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Set your OpenAI API key here, or use an environment variable
openai.api_key = st.secrets["API_KEY"]

# If the user_id hasn't been set in session_state yet, try to retrieve it from the hidden input
js_code = """
<div style="color: black;">
    <script>
        setTimeout(function() {
            const userID = document.getElementById("userID").value;
            if (userID) {
                window.Streamlit.setSessionState({"user_id": userID});
            }
        }, 1000);  // Delaying the execution by 1 second to ensure DOM is ready
    </script>
</div>
"""

st.markdown(js_code, unsafe_allow_html=True)

# getting user_id from the hidden input
user_id = st.session_state.get('user_id', 'unknown_user_id')  # Replace with your actual user identification method

# getting current date and time
current_date = datetime.now().strftime("%Y-%m-%d")
current_hour = datetime.now().strftime("%H:%M:%S")

st.title('Chatbot')

# Custom CSS for the chat interface
st.markdown(
    """
    <style>
        .message {
            margin: 10px;
            padding: 10px;
            border-radius: 10px;
            width: 70%;
        }
        .user {
            margin-left: auto;
            background-color: #2D2928;
        }
        .bot {
            margin-right: auto;
            background-color: #2D2928;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Connect to the database
conn = mysql.connector.connect(
    user=st.secrets['sql_user'],
    password=st.secrets['sql_password'],
    database=st.secrets['sql_database'],
    host=st.secrets['sql_host'],
    port=st.secrets['sql_port']
)

cursor = conn.cursor()

# Define and execute the table creation query
create_table_query = '''
CREATE TABLE IF NOT EXISTS conversations (
    user_id VARCHAR(255),
    date VARCHAR(255),
    hour VARCHAR(255),
    content MEDIUMTEXT
)
'''

cursor.execute(create_table_query)
conn.commit()
# Close the cursor and connection
cursor.close()

# Get the query parameters
params = st.experimental_get_query_params()
userID = params.get("userID", ["unknown id"])[0]
#st.write(f"User ID: {userID}")

def submit():
    st.session_state.last_submission = st.session_state.widget_value
    st.session_state.widget_value = ''

def save_conversation(content):
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_hour = datetime.now().strftime("%H:%M:%S")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (user_id, date, hour, content) VALUES (%s, %s, %s, %s)", 
                   (userID, current_date, current_hour, content))
    conn.commit()
    cursor.close()

start_message = {
    "role": "system", 
    "content": "You are a helpful and nice 50-year old human secretary called Kit who is passionate about your job. You answer things personally. You can answer all questions personally. You never mention your age, name, or that you're human, you just behave naturally. You are now talking to a friend of yours, so act like one."
}

# Display chat messages
for msg in st.session_state.messages:
    st.markdown(f"<div class='message {msg['class']}'>{msg['text']}</div>", unsafe_allow_html=True)

# Display modified text input
user_input = st.text_input("You: ", value=st.session_state.widget_value, on_change=submit, key='widget_value')

if 'chat' not in st.session_state:
    st.session_state.chat = []

if st.button('Send'):
    st.session_state.messages.append({'class': 'user', 'text': f"You: {st.session_state.last_submission}"})
    user_message = {"role": "user", "content": st.session_state.last_submission}
    st.session_state.chat.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        max_tokens=2000,
        messages=[start_message, *st.session_state.chat]
    )

    bot_response = response['choices'][0]['message']['content']
    bot_message = {"role": "system", "content": bot_response}
    st.session_state.chat.append(bot_message)
    st.session_state.messages.append({'class': 'bot', 'text': f"Kit: {bot_response}"})

    # Save the conversation to SQLite
    conversation_content = f"You: {st.session_state.last_submission}\nBot: {bot_response}"
    save_conversation(conversation_content)
    #st.write(conversation_content)
    
    st.session_state.last_submission = ''
    st.rerun()  # Clear input box by rerunning the app
