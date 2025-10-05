import streamlit as st
import time
from langchain_openai import AzureChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent

from utils.database import create_sql_database
from config.config import OPENAI_API_BASE, OPENAI_API_KEY, OPENAI_MODEL

@st.cache_resource
def get_llm():
    """
    Initialize and cache the LLM instance.
    
    Returns:
        AzureChatOpenAI: Configured Azure OpenAI LLM instance
    """
    return AzureChatOpenAI(
        azure_endpoint=OPENAI_API_BASE,
        azure_deployment=OPENAI_MODEL,
        api_version="2024-12-01-preview",
        api_key=OPENAI_API_KEY,  # type: ignore
    )

@st.cache_resource
def setup_agent(_llm):
    """
    Set up and cache the SQL agent.
    
    Args:
        _llm (ChatOpenAI): LLM instance
        
    Returns:
        Agent: Configured SQL agent
    """
    db = create_sql_database()
    return create_sql_agent(_llm, db=db, agent_type="openai-tools", verbose=True, top_k=600)

@st.cache_data(show_spinner=False)
def get_response(question, _agent_executor, prompt):
    """
    Get a response to a question, with caching.
    
    Args:
        question (str): The question to ask
        _agent_executor (Agent): The agent to use
        prompt (str): The prompt template
        
    Returns:
        tuple: (response, response_time, visualization_code)
    """
    if question in st.session_state.qa_cache:
        return st.session_state.qa_cache[question], 0, None
    
    start_time = time.time()
    
    # Use the synchronous invoke method instead of async
    try:
        result = _agent_executor.invoke(prompt.format(question=question))
        response = result['output']
    except Exception as e:
        # show error and fallback message
        st.error(f"Error getting response: {e}")
        response = "I'm sorry, I encountered an error while processing your question. Please try again."
    
    end_time = time.time()
    response_time = end_time - start_time
    
    # Skip LLM-based visualization generation - let the automated system handle it
    # The enhanced visualization system will automatically detect temperature event data
    # and create animated choropleth maps when appropriate
    viz_code = None
    
    # Cache the new response
    st.session_state.qa_cache[question] = (response, viz_code)
    
    return response, response_time, viz_code