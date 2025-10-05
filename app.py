import streamlit as st
import time
import streamlit.components.v1 as components

# Local imports
from ui.styles import get_custom_css
from ui.components import render_header, render_sidebar, render_chat_message, render_dashboard_metrics, render_example_questions_popup
from ui.auth import render_landing_page
from models.llm_service import get_llm, setup_agent, get_response
from utils.response_formatter import enhance_response_presentation
from utils.visualization import execute_viz_code
from config.config import APP_TITLE, APP_ICON, BASE_PROMPT_PATH

# App configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check authentication first - show landing page if not authenticated
if not render_landing_page():
    # User is not authenticated, landing page is displayed
    # Stop execution here - don't show the main app
    st.stop()

# User is authenticated - proceed with main app
# Apply custom styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Render page header (always visible)
render_header()

# Show example questions popup for new users (blocks app until dismissed)
render_example_questions_popup()

# Render sidebar (only after popup is dismissed)
render_sidebar()

# In app.py

# Load the prompt
@st.cache_data
def load_prompt():
    """Load the base prompt template from file."""
    try:
        with open(BASE_PROMPT_PATH, "r") as file:    
            return file.read()
    except FileNotFoundError:
        st.error(f"Could not find prompt file at {BASE_PROMPT_PATH}")
        # Fallback in case file is not found
        return """You are an expert analyst for power systems and energy markets. Answer the following question: {question}"""
    
# Initialize LLM and setup agent
llm = get_llm()
agent_executor = setup_agent(llm)

# Load the prompt
PROMPT = load_prompt()

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'qa_cache' not in st.session_state:
    st.session_state.qa_cache = {}

# Set current time for timestamps
st.session_state['current_time'] = time.strftime('%H:%M:%S')

# Get user input
question = st.text_input(
    "Ask a question about your power system planning data",
    placeholder="E.g., 'What's the worst heatwave in ERCOT?' or 'What's the worst coldwave in MRO US in 2023?'",
    key="input"
)

# Process user input
if st.button("Analyze"):
    with st.spinner("Generating insights and visualization..."):
        response, response_time, viz_code = get_response(question, agent_executor, PROMPT)
    st.session_state.history.append({"question": question, "response": response, "time": response_time, "viz_code": viz_code})

# Display chat history and visualizations
if st.session_state.history:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for i, chat in enumerate(st.session_state.history):
        # Display the question and response header
        render_chat_message(chat['question'], chat['response'], chat['time'], i)
        
        # Process and display the enhanced content with proper markdown rendering
        enhanced_response = enhance_response_presentation(chat['response'])
        # If response contains an HTML table snippet, render it via components.html
        if "<div" in enhanced_response and "<table" in enhanced_response:
            # Split out any markdown before the table
            pre, html_part = enhanced_response.split("<div", 1)
            table_html = "<div" + html_part
            # Extract complete div block containing the table
            close_idx = table_html.find("</div>")
            if close_idx != -1:
                close_idx += len("</div>")
                table_block = table_html[:close_idx]
                rest = table_html[close_idx:]
            else:
                table_block = table_html
                rest = ""
            # Render any leading markdown (e.g., headers)
            if pre.strip():
                st.markdown(pre, unsafe_allow_html=True)
            # Render the scrollable table
            components.html(table_block, height=450, scrolling=True)
            # Render following content (e.g., insights)
            if rest.strip():
                st.markdown(rest, unsafe_allow_html=True)
        else:
            st.markdown(enhanced_response, unsafe_allow_html=True)
        
        # Execute and display the visualization with a connecting element
        if chat['viz_code'] or True:  # Always try to generate visualization
            st.markdown("### Supporting Visualization")
            fig = execute_viz_code(chat['viz_code'], chat['response'])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No specific visualization could be generated for this response.")
    st.markdown("</div>", unsafe_allow_html=True)

# Render dashboard metrics
render_dashboard_metrics()