def get_custom_css():
    """
    Return custom CSS for styling the application.
    
    Returns:
        str: CSS code
    """
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f5f7fa;
        color: #333;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        margin-top: 80px;
    }
    header {
        background-color: transparent;
    }
    .custom-header {
        text-align: center;
        color: white;
        padding: 15px 10px; /* Increased padding to accommodate larger font */
    }
    .custom-header h1 {
        color: #fbbf24;
        margin: 0;
        font-size: 2.4em; /* Increased from 1.8em */
        font-weight: 700;
        letter-spacing: 0.5px; /* Added letter spacing for better readability */
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3); /* Added subtle text shadow for depth */
    }
    .custom-header p {
        color: #e5e7eb;
        font-size: 1.1em; /* Increased from 0.9em */
        margin: 8px 0 0; /* Slightly increased top margin */
        font-weight: 300; /* Lighter weight for subtitle */
    }
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999999;
        background-color: #1e3a8a;
        padding: 12px 0; /* Increased from 10px */
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .chat-container {
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        overflow: hidden;
    }
    .chat-message {
        padding: 1.5rem;
    }
    .chat-message .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .chat-message .header .title {
        font-weight: 600;
    }
    .chat-message .header .time {
        font-size: 0.8em;
        color: #6b7280;
    }
    .chat-message .content {
        margin-top: 0.5rem;
        line-height: 1.5;
    }
    .chat-message.user {
        background-color: #e8f0fe;
    }
    .chat-message.user .header .title {
        color: #1967d2;
    }
    .chat-message.assistant {        background-color: #f0f9ff;
    }
    .chat-message.assistant .header .title {
        color: #0369a1;
    }
    .stTextInput>div>div>input {
        background-color: white;
        border: 1px solid #d1d5db;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
    .sidebar .sidebar-content {
        background-color: #f9fafb;
        padding: 2rem;
        border-right: 1px solid #e5e7eb;
    }
    .sidebar img {
        max-width: 80%;
        margin: 0 auto 1.5rem;
        display: block;
        border-radius: 0.375rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stAlert {
        background-color: #e5e7eb;
        color: #1f2937;
        border-radius: 0.375rem;
        border-left: 5px solid #3b82f6;
    }
    
    /* Enhanced text formatting */
    .chat-message .content {
        margin-top: 0.5rem;
        line-height: 1.5;
    }
    
    /* Key insights formatting */
    h2 {
        font-size: 1.3em;
        color: #1e3a8a;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    /* Lists in responses */
    .stMarkdown ul {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stMarkdown li {
        margin-bottom: 0.25rem;
    }
    
    /* Tables in responses */
    .stMarkdown table {
        border-collapse: collapse;
        width: 100%;
        margin: 1rem 0;
    }
    
    .stMarkdown th, .stMarkdown td {
        padding: 8px;
        text-align: left;
        border: 1px solid #ddd;
    }
    
    .stMarkdown th {
        background-color: #f8f9fa;
        font-weight: 600;
    }
    
    /* Supporting visualization section */
    h3 {
        font-size: 1.1em;
        color: #4b5563;
        margin-top: 0.5rem;
        border-top: 1px dashed #e5e7eb;
        padding-top: 1rem;
    }
    
    /* Highlight key numbers */
    strong {
        color: #1e3a8a;
        font-weight: 600;
    }
    
    /* Welcome banner - gradient style with better colors */
    .welcome-banner {
        background: linear-gradient(135deg, #3b5998 0%, #4f6bb5 100%);
        border-radius: 8px;
        padding: 18px 24px;
        margin: 20px 0 25px 0;
        box-shadow: 0 3px 12px rgba(59, 89, 152, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .welcome-content {
        max-width: 900px;
        margin: 0 auto;
        text-align: center;
    }
    
    .welcome-title {
        font-size: 1.15em;
        font-weight: 600;
        color: #fde68a;
        margin: 0 0 8px 0;
        letter-spacing: 0.3px;
    }
    
    .welcome-subtitle {
        font-size: 0.9em;
        font-weight: 400;
        color: #e5e7eb;
        margin: 0;
        line-height: 1.5;
    }
    
    /* Example sections - inline display */
    .example-section {
        background: #f8f9ff;
        border-radius: 8px;
        padding: 18px;
        margin: 15px 0;
        border-left: 4px solid #1e3a8a;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.08);
    }
    
    .example-section h4 {
        margin: 0 0 12px 0;
        color: #1e3a8a;
        font-size: 1.15em;
        font-weight: 600;
        border: none;
        padding: 0;
    }
    
    .question-item {
        margin: 10px 0;
        padding: 10px 12px;
        background: white;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(30, 58, 138, 0.1);
        color: #2d3748;
        font-size: 0.95em;
        line-height: 1.5;
        transition: all 0.2s ease;
        cursor: default;
    }
    
    .question-item:hover {
        transform: translateX(3px);
        box-shadow: 0 2px 5px rgba(30, 58, 138, 0.15);
    }
    
    .question-item strong {
        color: #1e3a8a;
        font-weight: 600;
        background: #fef3c7;
        padding: 2px 5px;
        border-radius: 3px;
    }
    
    /* Ensure button is visible and clickable */
    .stButton {
        margin: 20px 0;
    }
    
    .stButton button {
        font-size: 1.1em !important;
        padding: 0.65rem 2.5rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5) !important;
    }</style>
    """