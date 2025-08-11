import streamlit as st
from groq import Groq
from streamlit_js_eval import streamlit_js_eval


# --- Page Configuration ---
st.set_page_config(page_title='Streamlit Chatbot', page_icon=':robot_face:')
st.title('Groq Chatbot')

if 'setup_complete' not in st.session_state:
    st.session_state.setup_complete = False
    
if 'user_message_count' not in st.session_state:
    st.session_state.user_message_count = 0
    
if 'feedback_shown' not in st.session_state:
    st.session_state.feedback_shown = False
    
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
if 'chat_complete' not in st.session_state:
    st.session_state.chat_complete = False

def complete_setup():
    st.session_state.setup_complete = True
    
def show_feedback():
    st.session_state.setup_complete = True

if not st.session_state.setup_complete:
    
    st.subheader('Personal information', divider='rainbow')
    
    if 'name' not in st.session_state:
        st.session_state['name'] = ''
        
    if 'experience' not in st.session_state:
        st.session_state['experience'] = ''
        
    if 'skills' not in st.session_state:
        st.session_state['skills'] = ''
    

    name = st.text_input(label = 'Name', max_chars=40, value=st.session_state['name'], placeholder = 'Enter your name')
    experience = st.text_area(label='Experiance', value=st.session_state['experience'], height=None, max_chars=200, placeholder='Describe your experience')
    skills = st.text_area(label = 'Skills', value=st.session_state['skills'], height=None, max_chars=200, placeholder='List your skills')

    st.write(f"**Your Name:** {name}")
    st.write(f"**Your Experience:** {experience}")
    st.write(f"**Your Skills:** {skills}")

    st.subheader('Company and Position', divider='rainbow')
    
    if 'level' not in st.session_state:
        st.session_state['level'] = 'Junior'
        
    if 'position' not in st.session_state:
        st.session_state['position'] = 'Data Scientist'
        
    if 'company' not in st.session_state:
        st.session_state['company'] = 'Amazon'

    col1, col2 = st.columns(2)
    with col1:
        st.session_state['level'] = st.radio(
            "Choose level",
            key='visibility',
            options=['Junior', 'Mid-level', 'Senior'],  
        )
        
    with col2:
        st.session_state['position'] = st.selectbox(
            "Choose a position",
            ('Data Scientist', 'Full Stack Developer', 'ML Engineer', 'GenAI Engineer','BI Analyst', 'Financial Analyst'),  
        ) 
        
        st.session_state['company'] = st.selectbox(
            "Choose a company",
            ('Amazon', 'Google', 'Meta', 'Nvidia','Tesla','OpenAI','Netflix','Microsoft')
        )
        
    st.write(
        f'**Your information:** {st.session_state['level']} {st.session_state['position']} at {st.session_state['company']}')
    
    if st.button('Start Interview', on_click=complete_setup):
        st.write("Setup complete! Starting interview...")

 
if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:
     
    st.info(
    """
    Start by introducing yourself.
    """,
    icon="🔰"
    )
    # --- API Client Initialization ---
    # Ensure you have your GROQ_API_KEY in Streamlit's secrets
    try:
        client = Groq(api_key=st.secrets['GROQ_API_KEY'])
    except Exception as e:
        st.error("Failed to initialize the Groq client. Make sure your GROQ_API_KEY is set in Streamlit secrets.")
        st.stop()

    # --- Session State Initialization ---
    # This ensures that the variables persist across reruns
    if "groq_model" not in st.session_state:
        st.session_state["groq_model"] = "llama3-8b-8192"

    if not st.session_state.messages:
        # The system message sets the personality of the chatbot
        st.session_state.messages = [{
            'role': 'system', 
            'content': (f'You are an HR executive that interviews an interviewee called {st.session_state['name']} '
                        f'with experience {st.session_state['experience']} and skills {st.session_state['skills']}. '
                        f'You should interview them for the position {st.session_state['level']} {st.session_state['position']} '
                        f'at the company {st.session_state['company']}.')
        }]

    # --- Display Chat History ---
    # This loop displays all messages except the initial system prompt
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if st.session_state.user_message_count < 5:
        # --- Handle User Input ---
        if prompt := st.chat_input("What is up?", max_chars=1000):
            # Add user's message to the session state and display it
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
              
            if st.session_state.user_message_count < 4:    
                # --- Generate and Stream Assistant's Response ---
                with st.chat_message('assistant'):
                    try:
                        # Create a placeholder for the streaming response
                        response_placeholder = st.empty()
                        full_response = ""

                        # Create the chat completion stream from the Groq API
                        stream = client.chat.completions.create(
                            model=st.session_state["groq_model"],
                            messages=[
                                {"role": m["role"], "content": m["content"]}
                                for m in st.session_state.messages
                            ],
                            stream=True,
                        )

                        # Manually iterate over the stream and update the placeholder
                        for chunk in stream:
                            # Safely get content from the chunk
                            content = chunk.choices[0].delta.content or ""
                            if content:
                                full_response += content
                                # Update the placeholder with the latest content and a cursor effect
                                response_placeholder.markdown(full_response + "▌")

                        # Update the placeholder with the final, complete response
                        response_placeholder.markdown(full_response)
                        
                    except Exception as e:
                        st.error(f"An error occurred while communicating with the Groq API: {e}")
                        full_response = "Sorry, I ran into a problem. Please try again."

                # Add the complete assistant response to the session state
                if full_response:
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.user_message_count += 1
            
    if st.session_state.user_message_count >= 5:
        st.session_state.chat_complete = True

if st.session_state.chat_complete and not st.session_state.feedback_shown:
    st.subheader('Feedback', divider='rainbow')
    
    if st.button("Get Feedback", on_click=show_feedback):
        st.write("Fetching feedback...")

if st.session_state.feedback_shown:
    
    conversation_history = "\n".join([f'{msg['content']}' for msg in st.session_state.messages])
    
    feedback_client = Groq(api_key=st.secrets['GROQ_API_KEY'])
    
    feedback_completion = feedback_client.chat.completions.create(
        model= "whisper-large-v3",
        messages=[{
            'role': 'system', 
            'content': """
                You are a helful tool that provides feedback on an interviewee performance.
                Before the Feedback give a score of 1 to 10.
                Follow this format:
                Overal Score: // Your score
                Feedback: // Here you put your feedback
                Give only the feedback do not ask any additional questions.
            """},
            {
                'role': 'user',
                'content': f"This is the interview you need to evaluate. Keep in mind that you are only a tool and shouldn't engage in conversation: {conversation_history}"
            }
        ]
    )
    
    st.write(feedback_completion.choices[0].message.content)
    
    if st.button("Restart Interview", type='primary'):
        streamlit_js_eval(js_expressions="window.location.reload()")