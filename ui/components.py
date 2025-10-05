import streamlit as st

def render_example_questions_popup():
    """
    Render example questions inline on first launch.
    Blocks the app until user clicks "Got it!".
    """
    # Initialize session state for popup control
    if 'show_examples_popup' not in st.session_state:
        st.session_state.show_examples_popup = True
    
    # Only show on first visit
    if st.session_state.show_examples_popup:
        # Welcome message with better structure
        st.markdown("""
            <div class="welcome-banner">
                <div class="welcome-content">
                    <h2 class="welcome-title">Thermal Event Libraries for Grid Planning</h2>
                    <p class="welcome-subtitle">Ask natural language questions to explore the effect of extreme events on your NERC service territory</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for the examples
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
                <div class="example-section">
                    <h4>🌡️ Heat Wave Questions</h4>
                    <div class="question-item">• Worst historical heat waves in my service territory of <strong>PJM</strong>?</div>
                    <div class="question-item">• Spatial extent of worst heat waves in my service territory of <strong>MRO US</strong>?</div>
                    <div class="question-item">• What's the twenty worst heatwave event in <strong>ERCOT</strong>?</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="example-section">
                    <h4>❄️ Cold Wave Questions</h4>
                    <div class="question-item">• Worst five historical cold snaps in my <strong>Pacific Northwest</strong>?</div>
                    <div class="question-item">• What are all coldsnap events after <strong>2000</strong> in <strong>RFC</strong> and neighbouring regions of <strong>MRO US, GATEWAY, NEWYORK, CENTRAL</strong>?</div>
                    <div class="question-item">• What are all coldsnap events after year <strong>2010</strong>?</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Button to dismiss and continue
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("Got it! ✓", type="primary", use_container_width=True, key="dismiss_examples"):
                st.session_state.show_examples_popup = False
                st.rerun()
        
        # Add spacing after examples
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Stop execution here - don't render the rest of the app
        st.stop()

def render_header():
    """
    Render the fixed header for the application.
    """
    st.markdown("""
        <div class="fixed-header">
            <div class='custom-header'>
                <h1>GridCoPilot</h1>
                <p>AI-powered analysis and visualization for long-term grid planning</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Add informational banner about analysis scope
    st.markdown("""
        <div style="background-color: #f0f8ff; border-left: 4px solid #1f77b4; padding: 10px; margin: 10px 0; border-radius: 5px;">
            <p style="margin: 0; color: #1f77b4; font-size: 14px;">
                📍 <strong>NERC Region-Level Analysis:</strong> This page provides detailed NERC region-level insights and analysis, for county level detailed analysis <a href="http://10.15.34.79:8501/" style="color: #1f77b4; text-decoration: underline;">click here</a>
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """
    Render the sidebar content.
    """
    with st.sidebar:
        st.title("About GridCoPilot")
        st.info(
            "GridCoPilot is a GenAI powered tool that streamlines compliance analysis and visualization for "
            "extreme weather events. "
            "It processes heatwave and coldsnap datasets to provide textual and visual insights for transmission planning requirements."
        )
        
        # Add "Developed at" label
        st.markdown("### Developed at")
        
        # Load and display PNNL logo
        st.image('assets/pnnl.png', use_column_width=True)
        
        # Add "Sponsored by" label
        st.markdown("### Sponsored by")
        # Add sponsor logos
        st.image('assets/opengraph-image.png', use_column_width=True)
        
        st.subheader("Quick Links")
        st.markdown("- [Documentation](#)")
        st.markdown("- [User Guide](#)")
        st.markdown("- [FAQ](#)")

def render_chat_message(question, response, response_time, chat_index):
    """
    Render a single chat message (question and response).
    
    Args:
        question (str): The user's question
        response (str): The AI's response
        response_time (float): Time taken to generate the response
        chat_index (int): The index of this chat in the conversation
    """
    # Display the question
    st.markdown(f"""
        <div class='chat-message user'>
            <div class='header'>
                <span class='title'>Question {chat_index+1}</span>
                <span class='time'>{st.session_state.get('current_time', '')}</span>
            </div>
            <div class='content'>{question}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display the response header
    st.markdown(f"""
        <div class='chat-message assistant'>
            <div class='header'>
                <span class='title'>Analysis</span>
                <span class='time'>Response time: {response_time:.2f}s</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_dashboard_metrics():
    """
    Render the dashboard metrics section.
    """
    st.subheader("Extreme Weather Analysis Highlights")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="NERC Regions Monitored", value="20", delta="Complete Coverage")
    with col2:
        st.metric(label="Counties Analyzed", value="3,100+", delta="Nationwide")
    with col3:
        st.metric(label="Event Definition Used", value="Def 6", delta="Standards Compliant")
    st.subheader("Key Analysis Features")
    st.info("❄️ Cold snap analysis available for extreme low temperature events affecting grid reliability and planning.")