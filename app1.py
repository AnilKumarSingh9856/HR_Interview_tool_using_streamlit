import streamlit as st
from groq import Groq

# --- Page Configuration ---
st.set_page_config(page_title='Interview Bot', page_icon=':robot_face:')
st.title('AI Interviewer')

# --- Session State Initialization ---
# Using a single 'stage' variable simplifies the logic flow
if 'stage' not in st.session_state:
    st.session_state.stage = "setup"

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'user_info' not in st.session_state:
    st.session_state.user_info = {
        "name": "", "experience": "", "skills": "",
        "level": "Junior", "position": "Data Scientist", "company": "Amazon"
    }

# --- Functions to change stage ---
def start_interview():
    st.session_state.stage = "interview"
    # Initialize the system prompt only once when the interview starts
    st.session_state.messages = [{
        'role': 'system',
        'content': (
            f"You are an HR executive conducting a behavioral interview. You are interviewing a candidate named {st.session_state.user_info['name']} "
            f"with experience in '{st.session_state.user_info['experience']}' and skills in '{st.session_state.user_info['skills']}'. "
            f"You are hiring for a {st.session_state.user_info['level']} {st.session_state.user_info['position']} "
            f"at {st.session_state.user_info['company']}. "
            "Your goal is to ask exactly 5 non-technical, behavioral questions, one at a time. Focus on topics like teamwork, problem-solving, past experiences, and cultural fit. "
            "Do not ask any technical questions, coding problems, or brain teasers. "
            "Do not greet the user; ask the first question immediately."
        )
    }]

def get_feedback():
    st.session_state.stage = "feedback"

# --- STAGE 1: SETUP ---
if st.session_state.stage == "setup":
    st.subheader('Personal Information', divider='rainbow')
    
    name = st.text_input('Name', value=st.session_state.user_info['name'], placeholder='Enter your name')
    experience = st.text_area('Experience', value=st.session_state.user_info['experience'], placeholder='Describe your experience')
    skills = st.text_area('Skills', value=st.session_state.user_info['skills'], placeholder='List your skills')

    st.subheader('Company and Position', divider='rainbow')
    
    col1, col2 = st.columns(2)
    with col1:
        level = st.radio(
            "Choose level",
            options=['Junior', 'Mid-level', 'Senior'],
            index=['Junior', 'Mid-level', 'Senior'].index(st.session_state.user_info['level'])
        )
    with col2:
        position = st.selectbox(
            "Choose a position",
            ('Data Scientist', 'Full Stack Developer', 'ML Engineer', 'GenAI Engineer','BI Analyst', 'Financial Analyst'),
            index=('Data Scientist', 'Full Stack Developer', 'ML Engineer', 'GenAI Engineer','BI Analyst', 'Financial Analyst').index(st.session_state.user_info['position'])
        )
        company = st.selectbox(
            "Choose a company",
            ('Amazon', 'Google', 'Meta', 'Nvidia','Tesla','OpenAI','Netflix','Microsoft'),
            index=('Amazon', 'Google', 'Meta', 'Nvidia','Tesla','OpenAI','Netflix','Microsoft').index(st.session_state.user_info['company'])
        )

    # --- Validation for starting interview ---
    all_fields_filled = name and experience and skills
    if not all_fields_filled:
        st.warning("Please fill in your Name, Experience, and Skills to start the interview.")

    if st.button('Start Interview', type="primary", disabled=not all_fields_filled):
        # Save all form data to session state before starting
        st.session_state.user_info = {
            "name": name, "experience": experience, "skills": skills,
            "level": level, "position": position, "company": company
        }
        start_interview()
        st.rerun()

# --- STAGE 2: INTERVIEW ---
if st.session_state.stage == "interview":
    st.info("The interview will consist of 5 questions. Please answer each one.", icon="ℹ️")
    
    try:
        client = Groq(api_key=st.secrets['GROQ_API_KEY'])
    except Exception as e:
        st.error("Failed to initialize the Groq client. Make sure your GROQ_API_KEY is set in Streamlit secrets.")
        st.stop()

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Count how many questions the user has answered
    user_message_count = sum(1 for msg in st.session_state.messages if msg['role'] == 'user')

    # --- Generate the FIRST question automatically ---
    if len(st.session_state.messages) == 1: # Only system prompt exists
        with st.chat_message('assistant'):
            response_placeholder = st.empty()
            full_response = ""
            stream = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                if content:
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()

    # --- Handle subsequent chat interactions ---
    if user_message_count < 5:
        if prompt := st.chat_input("Your answer..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
    else:
        st.success("Interview complete! Click the button below to get your feedback.")
        if st.button("Get Feedback", on_click=get_feedback):
            st.rerun()

    # Generate assistant response if the last message was from the user
    if st.session_state.messages and st.session_state.messages[-1]['role'] == 'user' and user_message_count < 5:
        with st.chat_message('assistant'):
            response_placeholder = st.empty()
            full_response = ""
            stream = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                if content:
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()

# --- STAGE 3: FEEDBACK ---
if st.session_state.stage == "feedback":
    st.subheader('Feedback', divider='rainbow')
    
    with st.spinner("Analyzing your interview and generating feedback..."):
        try:
            client = Groq(api_key=st.secrets['GROQ_API_KEY'])
            
            # Create a clean conversation history for the feedback model
            conversation_history = "\n".join(
                [f"Interviewer: {msg['content']}" if msg['role'] == 'assistant' else f"Candidate: {msg['content']}"
                for msg in st.session_state.messages if msg['role'] != 'system']
            )

            feedback_prompt = [{
                'role': 'system',
                'content': (
                    "You are an expert HR analyst. Your task is to provide constructive feedback on an interview transcript. "
                    "First, provide an overall score from 1 to 10. Then, give detailed feedback on the candidate's performance. "
                    "Follow this format exactly:\n\n"
                    "**Overall Score:** [Your score out of 10]\n\n"
                    "**Feedback:**\n[Your detailed feedback here]"
                )
            }, {
                'role': 'user',
                'content': f"Please evaluate the following interview transcript:\n\n{conversation_history}"
            }]

            feedback_completion = client.chat.completions.create(
                model="llama3-8b-8192", # Use a chat model for feedback
                messages=feedback_prompt,
                stream=False,
            )
            st.markdown(feedback_completion.choices[0].message.content)

        except Exception as e:
            st.error(f"Could not generate feedback. Error: {e}")

    # Use on_click to restart the interview while preserving user_info
    st.button("Restart Interview", type='primary', on_click=start_interview)

