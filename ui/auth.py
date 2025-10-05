"""
Authentication module for handling access validation.
"""
import streamlit as st
import re
from config.config import VALID_ACCESS_CODES


def is_valid_code_format(code):
    """
    Check if the validation code matches the expected format (6 alphanumeric characters).
    
    Args:
        code (str): The validation code to check
        
    Returns:
        bool: True if the format is valid, False otherwise
    """
    if not code:
        return False
    # Check for exactly 6 alphanumeric characters
    pattern = r'^[A-Za-z0-9]{6}$'
    return bool(re.match(pattern, code))


def validate_access_code(code):
    """
    Validate if the provided code is in the list of valid access codes.
    
    Args:
        code (str): The validation code to verify
        
    Returns:
        bool: True if the code is valid, False otherwise
    """
    if not code:
        return False
    
    # Convert to uppercase for case-insensitive comparison
    code_upper = code.upper().strip()
    
    # Check against valid codes (also converted to uppercase)
    valid_codes_upper = [c.upper() for c in VALID_ACCESS_CODES]
    return code_upper in valid_codes_upper


def render_landing_page():
    """
    Render the elegant landing page with validation code entry.
    
    Returns:
        bool: True if user is authenticated, False otherwise
    """
    # Initialize session state for authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'validation_error' not in st.session_state:
        st.session_state.validation_error = ""
    
    # If already authenticated, return True
    if st.session_state.authenticated:
        return True
    
    # Inject landing page CSS first
    st.markdown(get_landing_page_css(), unsafe_allow_html=True)
    
    # Create the animated background
    st.markdown("""
        <div class="landing-background">
            <div class="floating-shapes">
                <div class="shape shape-1"></div>
                <div class="shape shape-2"></div>
                <div class="shape shape-3"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Create split-screen layout with two columns
    left_col, right_col = st.columns([1.2, 1], gap="large")
    
    # LEFT SIDE - Branding and Information
    with left_col:
        # Logo section
        st.markdown("""
            <div style="padding: 2rem 2rem 1rem 2rem;">
                <div style="margin-bottom: 1.5rem;">
                    <div class="logo-pulse" style="font-size: 5rem; margin-bottom: 1rem; 
                         filter: drop-shadow(0 4px 12px rgba(251, 191, 36, 0.4));">⚡</div>
                    <h1 class="gradient-text" style="font-size: 4rem; font-weight: 800; 
                         background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #fbbf24 100%);
                         -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                         background-clip: text; margin: 0; letter-spacing: -1px; line-height: 1.1;">
                        GridCoPilot
                    </h1>
                    <p style="font-size: 1.3rem; color: #6b7280; font-weight: 500; margin: 0.8rem 0;
                         letter-spacing: 0.5px;">
                        Power System Intelligence Platform
                    </p>
                    <div style="width: 80px; height: 4px; background: linear-gradient(90deg, #3b82f6, #fbbf24); 
                         margin: 1rem 0 0 0; border-radius: 2px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Alpha badge
        st.markdown("""
            <div style="padding: 0 2rem; margin: 1rem 0;">
                <div style="display: inline-flex; align-items: center; 
                     background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
                     color: white; padding: 0.7rem 1.8rem; border-radius: 50px; font-size: 0.85rem;
                     box-shadow: 0 4px 15px rgba(251, 191, 36, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.3) inset;">
                    <span style="margin-right: 0.6rem; font-size: 1.2rem;">🔒</span>
                    <span style="font-weight: 700; letter-spacing: 1px;">ALPHA RELEASE</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Description
        st.markdown("""
            <div style="padding: 0 2rem; margin: 1.5rem 0;">
                <h2 style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.8rem;">
                    GenAI-Powered Grid Planning
                </h2>
                <p style="font-size: 1.05rem; line-height: 1.8; color: #4b5563; margin: 0;">
                    Analyze extreme weather events for long-term transmission planning.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # RIGHT SIDE - Access Code Entry
    with right_col:
        # Auth card header
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px);
                 border-radius: 24px; padding: 3rem 2.5rem 2rem 2.5rem; margin: 2rem auto;
                 box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.5) inset;
                 border: 1px solid rgba(255, 255, 255, 0.8); max-width: 500px; text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔐</div>
                <h3 style="font-size: 1.8rem; font-weight: 700; color: #1f2937; margin: 0 0 0.5rem 0;">
                    Secure Access
                </h3>
                <p style="font-size: 0.95rem; color: #6b7280; margin: 0;">
                    Enter your validation code to continue
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Input field for validation code
        validation_code = st.text_input(
            "Validation Code",
            max_chars=6,
            placeholder="ABC123",
            label_visibility="collapsed",
            key="validation_code_input",
            help="Enter your 6-character alphanumeric access code"
        )
        
        # Submit button
        submit_button = st.button("🔓  Unlock Access", use_container_width=True, type="primary", key="submit_auth")
        
        # Handle validation
        if submit_button:
            if not validation_code:
                st.session_state.validation_error = "Please enter a validation code"
            elif not is_valid_code_format(validation_code):
                st.session_state.validation_error = "Invalid format. Code must be 6 alphanumeric characters"
            elif validate_access_code(validation_code):
                st.session_state.authenticated = True
                st.session_state.validation_error = ""
                st.rerun()
            else:
                st.session_state.validation_error = "Invalid access code. Please check your code and try again"
        
        # Display error message if any
        if st.session_state.validation_error:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
                     border: 2px solid #fecaca; color: #dc2626; padding: 1.2rem;
                     border-radius: 12px; margin-top: 1.5rem; text-align: center;
                     box-shadow: 0 4px 12px rgba(220, 38, 38, 0.1);">
                    <span style="font-size: 1.3rem; margin-right: 0.5rem;">⚠️</span>
                    <span style="font-weight: 500;">{st.session_state.validation_error}</span>
                </div>
            """, unsafe_allow_html=True)
        
        # Helper text
        st.markdown("""
            <div style="text-align: center; margin-top: 2rem; padding: 1rem; 
                 background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%); 
                 border-radius: 12px; border: 1px solid #dbeafe;">
                <p style="font-size: 0.85rem; color: #1e40af; margin: 0; font-weight: 500; line-height: 1.5;">
                    💡 Codes are case-insensitive<br>and exactly 6 characters
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Footer inside card
        st.markdown("""
            <div style="text-align: center; margin-top: 2.5rem; padding-top: 1.5rem; 
                 border-top: 1px solid #e5e7eb;">
                <p style="font-size: 0.85rem; color: #6b7280; line-height: 1.6;">
                    Need an access code?<br>
                    <span style="color: #3b82f6; font-weight: 500;">Contact your administrator</span>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Close card container
        st.markdown('</div>', unsafe_allow_html=True)
    
    return False


def get_landing_page_css():
    """
    Return custom CSS for the landing page.
    
    Returns:
        str: CSS code for landing page styling
    """
    return """
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Base styling */
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        max-width: 100% !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Full height container */
    .main {
        height: 100vh;
        overflow: hidden;
    }
    
    /* Animated background */
    .landing-background {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 25%, #fef3c7 50%, #fee2e2 75%, #f0f9ff 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        z-index: -1;
        opacity: 0.5;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating shapes */
    .floating-shapes {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: -1;
        pointer-events: none;
    }
    
    .shape {
        position: absolute;
        border-radius: 50%;
        filter: blur(60px);
        opacity: 0.15;
        animation: float 20s infinite ease-in-out;
    }
    
    .shape-1 {
        width: 300px;
        height: 300px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        top: 10%;
        left: 10%;
        animation-delay: 0s;
    }
    
    .shape-2 {
        width: 250px;
        height: 250px;
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        top: 60%;
        right: 10%;
        animation-delay: 7s;
    }
    
    .shape-3 {
        width: 200px;
        height: 200px;
        background: linear-gradient(135deg, #06b6d4, #3b82f6);
        bottom: 10%;
        left: 50%;
        animation-delay: 14s;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        25% { transform: translate(30px, -30px) rotate(90deg); }
        50% { transform: translate(-20px, 20px) rotate(180deg); }
        75% { transform: translate(40px, 10px) rotate(270deg); }
    }
    
    /* Left panel - Info section */
    .info-panel {
        padding: 3rem 2rem;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        animation: slideInLeft 0.6s ease-out;
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Right panel - Auth card */
    .auth-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3rem 2.5rem;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.5) inset;
        position: relative;
        animation: slideInRight 0.6s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.8);
        margin: 2rem 0;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .card-glow {
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #fbbf24);
        border-radius: 24px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
        filter: blur(20px);
    }
    
    .auth-card:hover .card-glow {
        opacity: 0.3;
    }
    
    /* Logo pulse animation */
    .logo-pulse {
        animation: logoPulse 3s ease-in-out infinite;
        display: inline-block;
    }
    
    @keyframes logoPulse {
        0%, 100% { 
            transform: scale(1) rotate(0deg);
            filter: drop-shadow(0 4px 12px rgba(251, 191, 36, 0.4));
        }
        50% { 
            transform: scale(1.1) rotate(5deg);
            filter: drop-shadow(0 8px 24px rgba(251, 191, 36, 0.6));
        }
    }
    
    /* Gradient text animation */
    .gradient-text {
        animation: gradientTextShift 5s ease infinite;
        background-size: 200% auto;
    }
    
    @keyframes gradientTextShift {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 100% center; }
    }
    
    /* Alpha badge modern */
    .alpha-badge-modern {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        padding: 0.7rem 1.8rem;
        border-radius: 50px;
        font-size: 0.85rem;
        box-shadow: 
            0 4px 15px rgba(251, 191, 36, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.3) inset;
        animation: badgeGlow 2s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .alpha-badge-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: badgeShine 3s infinite;
    }
    
    @keyframes badgeGlow {
        0%, 100% { 
            box-shadow: 0 4px 15px rgba(251, 191, 36, 0.4),
                        0 0 0 1px rgba(255, 255, 255, 0.3) inset;
        }
        50% { 
            box-shadow: 0 6px 25px rgba(251, 191, 36, 0.6),
                        0 0 0 1px rgba(255, 255, 255, 0.3) inset;
        }
    }
    
    @keyframes badgeShine {
        0% { left: -100%; }
        50%, 100% { left: 200%; }
    }
    
    /* Style the Streamlit text input */
    .stTextInput > div > div > input {
        text-align: center;
        font-size: 1.8rem !important;
        letter-spacing: 0.6rem;
        font-weight: 700;
        text-transform: uppercase;
        border: 2px solid #e5e7eb !important;
        border-radius: 16px !important;
        padding: 1.3rem 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        font-family: 'Inter', monospace !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 
            0 0 0 4px rgba(59, 130, 246, 0.1),
            0 8px 20px rgba(59, 130, 246, 0.15) !important;
        transform: translateY(-2px);
        background: #ffffff;
    }
    
    .stTextInput > div > div > input::placeholder {
        letter-spacing: 0.4rem;
        opacity: 0.4;
    }
    
    /* Style the submit button */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        padding: 1rem 2.5rem !important;
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 
            0 4px 15px rgba(59, 130, 246, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 
            0 8px 25px rgba(59, 130, 246, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* Error box modern */
    .error-box {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 2px solid #fecaca;
        color: #dc2626;
        padding: 1.2rem;
        border-radius: 12px;
        margin-top: 1.5rem;
        font-size: 0.95rem;
        animation: errorShake 0.5s ease;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.1);
    }
    
    @keyframes errorShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    /* Responsive design */
    @media (max-width: 1024px) {
        .info-panel {
            padding: 2rem 1.5rem;
            height: auto;
        }
        
        .auth-card {
            padding: 2rem 1.5rem;
            margin: 1rem 0;
        }
    }
    
    @media (max-width: 768px) {
        .info-panel h1 {
            font-size: 3rem !important;
        }
        
        .info-panel h2 {
            font-size: 1.3rem !important;
        }
        
        .stTextInput > div > div > input {
            font-size: 1.4rem !important;
            letter-spacing: 0.4rem;
        }
        
        .logo-pulse {
            font-size: 4rem !important;
        }
    }
    </style>
    """
