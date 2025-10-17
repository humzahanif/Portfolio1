import streamlit as st
from pathlib import Path
import base64
from datetime import datetime
try:
    from config import *
except ImportError:
    PERSONAL_INFO = {"name": "Hamza Hanif", "email": "humzahanif786@gmail.com", "phone": "+923452275566"}
    PROJECTS = []
    CHATBOT_KB = {}

st.set_page_config(
    page_title="Hamza Hanif - Portfolio",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'ai_chat_history' not in st.session_state:
    st.session_state.ai_chat_history = [{"role": "assistant", "content": "Hi! I'm your AI assistant. Ask me anything about Hamza's skills, projects, or experience! 👋"}]
if 'ai_chat_visible' not in st.session_state:
    st.session_state.ai_chat_visible = False

def load_css(theme='dark'):
    if theme == 'light':
        bg_color = '#f5f5f5'
        text_color = '#212121'
        card_bg = '#e0e0e0'
        border_color = '#9e9e9e'
        accent_color = '#424242'
        secondary_text = '#616161'
        heading_color = '#212121'
    else:
        bg_color = '#121212'
        text_color = '#ffffff'  # Brighter white for better contrast
        card_bg = '#1e1e1e'
        border_color = '#424242'
        accent_color = '#ffffff'  # Brighter accent color
        secondary_text = '#b0b0b0'  # Lighter gray for better readability
        heading_color = '#ffffff'  # White for headings in dark mode
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=BenchNine:wght@300;400;700&family=Open+Sans:wght@300;400;600;700&display=swap');
    
    /* Main app background */
    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    
    /* Main content area */
    .main .block-container {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    
    /* Text elements */
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4,
    .stMarkdown h5,
    .stMarkdown h6,
    .stMarkdown li {{
        color: {text_color} !important;
    }}
    
    /* Cards and containers */
    .stButton > button,
    .stAlert,
    .stExpander,
    .stTabs [data-baseweb="tab"] {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border-color: {border_color} !important;
    }}
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div[data-baseweb="select"] > div,
    .stSlider > div > div[data-testid="stThumbValue"] {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border-color: {border_color} !important;
    }}
    
    /* Tables */
    .stDataFrame,
    .stDataFrame th,
    .stDataFrame td {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border-color: {border_color} !important;
    }}
    
    [data-testid="stSidebar"] .stButton > button {{
        background-color: {card_bg} !important;
        color: #0000ff !important;
        border: 2px solid #0000ff !important;
        margin: 8px 0;
        width: 100%;
        padding: 0.6rem 1rem;
        border-radius: 6px;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.2s ease;
    }}
    
    [data-testid="stSidebar"] .stButton > button:hover {{
        background-color: #0000ff !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 2px 8px rgba(0,0,255,0.3) !important;
    }}
    
    [data-testid="stSidebar"] .stButton > button p {{
        color: #0000ff !important;
        margin: 0 !important;
        font-weight: 500 !important;
    }}
    
    [data-testid="stSidebar"] .stButton > button:hover p {{
        color: white !important;
    }}
    
    .block-container {{
        padding: 2rem 1.5rem !important;
        max-width: 1200px !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {heading_color} !important;
        font-family: 'BenchNine', sans-serif !important;
    }}
    
    .hero-section {{
        background: url('images/li.jpg') center/cover no-repeat;
        position: relative;
        padding: 6rem 2rem;
        color: {text_color};
        text-align: center;
        margin: -2rem -1rem 2rem -1rem;
        box-shadow: inset 0 0 0 2000px {f'rgba(255, 255, 255, 0.85)' if theme == 'light' else 'rgba(0, 0, 0, 0.7)'};
    }}
    
    .hero-title {{
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        font-family: 'BenchNine', sans-serif;
        color: {accent_color};
        text-shadow: 2px 2px 4px {f'rgba(255,255,255,0.5)' if theme == 'light' else 'rgba(0,0,0,0.8)'};
        letter-spacing: 2px;
    }}
    
    .stButton > button {{
        background: #0000ff;
        color: white;
        border: 2px solid #0000ff;
        padding: 1rem 2.5rem;
        border-radius: 0;
        font-weight: 700;
        font-family: 'BenchNine', sans-serif;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background: transparent;
        color: #0000ff;
        border: 2px solid #0000ff;
        transform: scale(1.05);
    }}
    
    .portfolio-card {{
        background: {card_bg};
        border-radius: 0;
        padding: 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        margin-bottom: 2rem;
        border: 3px solid {border_color};
        overflow: hidden;
    }}
    
    .portfolio-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 8px 20px rgba(66,105,225,0.3);
        border-color: #424242;
    }}
    
    .featured-card {{
        background: {card_bg};
        border-radius: 0;
        padding: 0;
        margin-bottom: 1.5rem;
        border: 2px solid {border_color};
        transition: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        overflow: hidden;
        cursor: default;
    }}
    
    .featured-card h4 {{
        background: #0000ff;
        color: white;
        padding: 1rem;
        margin: 0;
        font-family: 'BenchNine', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        font-size: 1.2rem;
    }}
    
    .portfolio-card h4 {{
        background: #0000ff;
        color: white;
        padding: 1rem;
        margin: 0;
        font-family: 'BenchNine', sans-serif;
        font-size: 1.3rem;
        text-align: center;
        font-weight: 700;
        text-transform: uppercase;
    }}
    
    .contact-card {{
        background: {card_bg};
        border-radius: 0;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        border: 2px solid {border_color};
    }}
    
    .footer {{
        text-align: center;
        padding: 2rem;
        color: #666;
        margin-top: 3rem;
    }}
    
    [data-testid="stSidebar"] {{
        background: {bg_color} !important;
        border-right: 3px solid #0000ff !important;
        color: {text_color} !important;
    }}
    
    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    
    [data-testid="stSidebar"] a {{
        color: {accent_color} !important;
    }}
    
    [data-testid="stSidebar"] a:hover {{
        color: {hover_color if 'hover_color' in locals() else accent_color} !important;
        text-decoration: underline;
    }}
    
    [data-testid="stSidebar"] img {{
        border: 3px solid #0000ff !important;
        padding: 0.5rem !important;
        background: #212121 !important;
        border-radius: 5px !important;
        box-shadow: 0 2px 8px rgba(0,0,255,0.3) !important;
    }}
    
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] {{
        background: #0000ff !important;
        color: white !important;
        border: 2px solid #0000ff !important;
    }}
    
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover {{
        background: #1a1a1a !important;
        border-color: #0000ff !important;
    }}
    
    .info-box {{
        background: {card_bg};
        border: 2px solid #0000ff;
        padding: 1.5rem;
        margin: 1rem 0;
        color: {text_color};
    }}
    
    .info-box strong {{
        color: #0000ff;
    }}
    
    .info-box h3 {{
        color: {heading_color} !important;
    }}
    
    .info-box p {{
        color: {text_color};
    }}
    
    .stChatMessage {{
        background: {card_bg} !important;
        border: 1px solid {border_color} !important;
    }}
    
    .stChatMessage p {{
        color: {text_color} !important;
    }}
    
    .stChatMessage[data-testid="user-message"] {{
        background: #1a237e !important;
    }}
    
    .stChatMessage[data-testid="user-message"] p {{
        color: #ffffff !important;
    }}
    
    .stChatMessage[data-testid="assistant-message"] {{
        background: {card_bg} !important;
    }}
    
    .stChatMessage[data-testid="assistant-message"] p {{
        color: {text_color} !important;
    }}
    
    img {{
        border: 3px solid {border_color};
        transition: all 0.3s ease;
    }}
    
    img:hover {{
        border-color: #424242;
        transform: scale(1.02);
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

KB = {
    'personal': {
        'keywords': ['name', 'who', 'about', 'intro'],
        'response': "Hamza Hanif is a Web Developer, Designer, and AI Chatbot Developer in Karachi, Pakistan."
    },
    'skills': {
        'keywords': ['skill', 'technology', 'programming', 'language'],
        'response': "Skills: HTML5, CSS, JavaScript, Bootstrap, Python, PHP, MySQL, Flask, WordPress, Streamlit."
    },
    'education': {
        'keywords': ['education', 'study', 'certificate', 'course'],
        'response': "Education: ACCP (Aptech), Advanced Diploma in Media Studies.\nCertificates: English, Networking, CEH, Communication Design, GenAI, AI Nexus."
    },
    'experience': {
        'keywords': ['experience', 'work', 'freelance', 'job'],
        'response': "Freelancer in Web Development, Design, and AI Chatbot Development."
    },
    'projects': {
        'keywords': ['project', 'portfolio', 'work', 'aqua', 'techflow'],
        'response': "19+ projects including AQUA WORLD, TechFlow Solutions, AI Assistants, Google Calendar AI, Stock Analysis, Image Generator, Weather Radar, Crypto Trading, and more!"
    },
    'contact': {
        'keywords': ['contact', 'email', 'phone', 'linkedin', 'reach', 'hire'],
        'response': "Contact: Email: humzahanif786@gmail.com, Mobile: +923452275566, LinkedIn: linkedin.com/in/humzahanif786"
    },
    'services': {
        'keywords': ['service', 'offer', 'build', 'help', 'develop'],
        'response': "Services: Web Development & Design, AI Chatbots (Text/Voice/WhatsApp), Responsive Websites, E-commerce Solutions"
    }
}

def process_message(message):
    msg_lower = message.lower()
    if any(word in msg_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        return "Hello! Ask me about skills, projects, CV, education, experience, or contact info!"
    if any(word in msg_lower for word in ['thank', 'thanks']):
        return "You're welcome! Feel free to ask anything else."
    for category, data in KB.items():
        if any(keyword in msg_lower for keyword in data['keywords']):
            return data['response']
    return "Ask me about: Skills & technologies, Projects & portfolio, Education, Experience, Contact info, Services"

try:
    if 'PROJECTS' not in dir() or not PROJECTS:
        raise NameError
except NameError:
    PROJECTS = [
        {"name": "AQUA WORLD", "folder": "AQUA WORLD"},
        {"name": "TechFlow Solutions Chatbot Text", "folder": "TechFlow Solutions Chatbot Text"},
        {"name": "TechFlow Solutions WhatsApp", "folder": "TechFlow Solutions Whatsapp"},
        {"name": "TechFlow Solutions Voice", "folder": "TechFlow Solutions Voice"},
        {"name": "TechFlow Solutions Calling", "folder": "TechFlow Solutions Calling"},
        {"name": "TechFlow Calling Assistant", "folder": "TechFlow Calling Assistant"},
        {"name": "TechFlow Solutions AI Assistant", "folder": "TechFlow Solutions AI Assistant"},
        {"name": "ElevenLabs Remake", "folder": "IIElevenLabs Remake"},
        {"name": "Google Calendar AI Agent", "folder": "Google Calendar AI Agent"},
        {"name": "Cartesia Remake", "folder": "Cartesia Remake"},
        {"name": "AI Stock Analysis Agent", "folder": "AI Stock Analysis Agent"},
        {"name": "AI Image Generator Pro", "folder": "AI Image Generator Pro"},
        {"name": "Advanced Weather Radar & Satellite System", "folder": "Advanced Weather Radar & Satellite System"},
        {"name": "Advanced Translation Agent", "folder": "Advanced Translation Agent"},
        {"name": "Advanced RXN Chemistry Portal", "folder": "Advanced RXN Chemistry Portal"},
        {"name": "Advanced Live Crypto Chart", "folder": "Advanced Live Crypto Chart"},
        {"name": "Advanced Image AI Agent", "folder": "Advanced Image AI Agent"},
        {"name": "Advanced AI Search Agent", "folder": "Advanced AI Search Agent"},
        {"name": "Advanced Crypto Trading Agent", "folder": "Advanced Crypto Trading Agent"},
        {"name": "Allin1Technologies", "folder": "Allin1technologies"}
    ]

def get_image_path(folder_name):
    img_dir = Path(f"images/{folder_name}")
    if img_dir.exists():
        images = list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.jpeg"))
        if images:
            return str(images[0]).replace("\\", "/")
    return None

def get_all_images(folder_name):
    img_dir = Path(f"images/{folder_name}")
    if img_dir.exists():
        # Get all image files, handling spaces and special characters in filenames
        image_patterns = ["*.png", "*.jpg", "*.jpeg"]
        images = []
        for pattern in image_patterns:
            try:
                images.extend(img_dir.glob(pattern))
            except Exception as e:
                print(f"Error loading {pattern} files: {e}")
        
        # Sort images by name
        images = sorted(images, key=lambda x: str(x).lower())
        
        # Convert to forward slashes and return
        return [str(img).replace("\\", "/") for img in images]
    return []

@st.cache_data
def load_image(image_path):
    from PIL import Image
    try:
        # Convert to Path object and resolve any relative paths
        img_path = Path(image_path).resolve()
        if img_path.exists():
            try:
                return Image.open(str(img_path))
            except Exception as img_error:
                print(f"Error opening image {img_path}: {img_error}")
        else:
            print(f"Image not found: {img_path}")
    except Exception as e:
        error_msg = f"Error loading image {image_path}: {str(e)}"
        st.error(error_msg)
        print(error_msg)
    return None

def home_page():
    st.markdown("""
    <style>
    button[data-testid="baseButton-secondary"] {
        color: white !important;
        background: #0000ff !important;
        border: 2px solid #0000ff !important;
    }
    button[data-testid="baseButton-secondary"]:hover {
        background: #0051ff !important;
    }
    button[data-testid="baseButton-secondary"] p {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if 'slider_index' not in st.session_state:
        st.session_state.slider_index = 0
    
    slides = [
        {
            "title": "Web Developer & Designer",
            "text": "I'm a web developer and designer passionate about building modern, responsive websites that not only look great but also work seamlessly.",
            "image": "images/li.jpg"
        },
        {
            "title": "AI-Based Chatbot Development",
            "text": "I develop AI-powered chatbots that provide instant support, answer questions, and enhance customer engagement.",
            "image": "images/li.jpg"
        }
    ]
    
    current_slide = slides[st.session_state.slider_index]
    bg_image_base64 = ""
    if Path(current_slide['image']).exists():
        with open(current_slide['image'], "rb") as img_file:
            bg_image_base64 = base64.b64encode(img_file.read()).decode()
    
    # Get current theme for text color
    theme = st.session_state.get('theme', 'dark')
    text_color = '#000000' if theme == 'light' else '#ffffff'
    
    st.markdown(f"""
    <div class="hero-section" style="background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('data:image/jpeg;base64,{bg_image_base64}'); background-size: cover; min-height: 400px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 3rem 2rem;">
        <div class="hero-title" style="color: {text_color};">{current_slide['title']}</div>
        <p style="font-size: 1.2rem; color: {text_color}; text-align: center; max-width: 800px;">"{current_slide['text']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        resume_url = "https://hamzahanif.techbyanum.com/cv/resume"
        cv_path = Path("cv/CVpdf/Hamza Hanif Resume.pdf")
        b64_pdf = ""
        if cv_path.exists():
            with open(cv_path, "rb") as file:
                b64_pdf = base64.b64encode(file.read()).decode()
        
        st.markdown(f"""
        <div style="display: flex; gap: 1rem; justify-content: center;">
            <a href="{resume_url}" target="_blank" style="display: inline-block; width: 180px; padding: 0.75rem 1rem; background: #0000ff; color: white; text-align: center; text-decoration: none; border: 2px solid #0000ff; border-radius: 0.5rem; font-weight: bold;" onmouseover="this.style.background='#0000ff';" onmouseout="this.style.background='#0000ff'">📄 View CV</a>
            <a href="data:application/pdf;base64,{b64_pdf}" download="Hamza_Hanif_Resume.pdf" style="display: inline-block; width: 180px; padding: 0.75rem 1rem; background: #0000ff; color: white; text-align: center; text-decoration: none; border: 2px solid #0000ff; border-radius: 0.5rem; font-weight: bold;" onmouseover="this.style.background='#0000ff';" onmouseout="this.style.background='#0000ff'">📥 Download CV</a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col1:
        if st.button("◀", use_container_width=True, key="prev_slide"):
            st.session_state.slider_index = (st.session_state.slider_index - 1) % len(slides)
            st.rerun()
    
    with col2:
        dots = "⬤ " if st.session_state.slider_index == 0 else "○ "
        dots += "⬤" if st.session_state.slider_index == 1 else "○"
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0;">
            <p style="color: #424242; font-size: 1.5rem; margin-bottom: 0.5rem;">{dots}</p>
            <p style="color: #757575;">Slide {st.session_state.slider_index + 1} of {len(slides)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("▶", use_container_width=True, key="next_slide"):
            st.session_state.slider_index = (st.session_state.slider_index + 1) % len(slides)
            st.rerun()
    
    st.markdown("<h2>Portfolio</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #979090; margin-bottom: 2rem;'>Featured Projects</p>", unsafe_allow_html=True)
    
    featured_projects = PROJECTS[:6]
    for i in range(0, len(featured_projects), 3):
        cols = st.columns(3, gap="large")
        for j, col in enumerate(cols):
            if i + j < len(featured_projects):
                project = featured_projects[i + j]
                with col:
                    st.markdown(f'<div class="featured-card"><h4>{project["name"]}</h4></div>', unsafe_allow_html=True)
                    img_path = get_image_path(project['folder'])
                    if img_path and Path(img_path).exists():
                        img = load_image(img_path)
                        if img:
                            st.image(img, use_container_width=True)

def portfolio_page():
    st.markdown("<h2>Portfolio</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        view_mode = st.selectbox("View", ["Expanded", "Compact"], label_visibility="collapsed")
    with col3:
        images_per_row = st.selectbox("Per Row", [2, 3, 4], index=1, label_visibility="collapsed")
    
    st.markdown("---")
    
    for idx, project in enumerate(PROJECTS):
        st.markdown(f'<div class="portfolio-card" style="margin: 2rem 0 1rem 0;"><h4>{idx + 1}. {project["name"]}</h4></div>', unsafe_allow_html=True)
        all_images = get_all_images(project['folder'])
        
        if all_images:
            st.markdown(f"<p style='color: #424242; font-weight: bold; margin-bottom: 1rem;'>📸 {len(all_images)} Screenshots</p>", unsafe_allow_html=True)
            
            if view_mode == "Compact":
                with st.expander(f"View all {len(all_images)} images", expanded=False):
                    for i in range(0, len(all_images), images_per_row):
                        cols = st.columns(images_per_row, gap="medium")
                        for j, col in enumerate(cols):
                            if i + j < len(all_images):
                                with col:
                                    img = load_image(all_images[i + j])
                                    if img:
                                        st.image(img, use_container_width=True, caption=f"Screenshot {i+j+1}")
            else:
                for i in range(0, len(all_images), images_per_row):
                    cols = st.columns(images_per_row, gap="medium")
                    for j, col in enumerate(cols):
                        if i + j < len(all_images):
                            with col:
                                img = load_image(all_images[i + j])
                                if img:
                                    st.image(img, use_container_width=True, caption=f"Screenshot {i+j+1}")

def resume_page():
    theme = st.session_state.get('theme', 'dark')
    
    if theme == 'light':
        bg_color = '#ffffff'
        text_color = '#212529'
        card_bg = '#f8f9fa'
        border_color = '#dee2e6'
        accent_color = '#0d6efd'
        hover_color = '#0b5ed7'
        link_color = '#0a58ca'
        heading_color = '#212529'
        text_color1 = '#212529'
        muted_text = '#6c757d'
        project_bg = '#f8f9fa'
    else:
        bg_color = '#1a1a1a'
        text_color = '#f8f9fa'
        card_bg = '#2d2d2d'
        border_color = '#495057'
        accent_color = '#3d8bfd'
        hover_color = '#6ea8fe'
        link_color = '#85b6ff'
        text_color1 = '#ffffff'
        heading_color = '#ffffff'
        muted_text = '#adb5bd'
        project_bg = '#2d2d2d'

    st.markdown(f"""
    <style>
        .resume-section {{
            margin-bottom: 2rem;
        }}
        .section-header {{
            font-size: 1.3rem;
            font-weight: 700;
            color: {heading_color} !important;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {border_color};
        }}
        .resume-grid {{
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 2rem;
            margin-bottom: 1.5rem;
        }}
        .grid-left {{
            font-weight: 600;
            color: {heading_color};
        }}
        .grid-right {{
            color: {muted_text};
        }}
        .grid-right a {{
            color: {link_color};
            text-decoration: none;
            transition: color 0.2s;
        }}
        .grid-right a:hover {{
            color: {hover_color};
            text-decoration: underline;
        }}
        .item-row {{
            margin-bottom: 2rem;
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 2rem;
            align-items: start;
        }}
        .item-left {{
            font-weight: 600;
            color: {heading_color};
        }}
        .item-right {{
            color: {muted_text};
            line-height: 1.6;
        }}
        .project-item {{
            margin-bottom: 1.5rem;
            padding: 1rem;
            background: {card_bg};
            border-left: 4px solid {accent_color};
            border-radius: 4px;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .project-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        .project-name {{
            font-weight: 600;
            color: {text_color1};
            margin-bottom: 0.5rem;
        }}
        .project-name a {{
            color: {link_color};
            text-decoration: none;
            transition: color 0.2s;
        }}
        .project-name a:hover {{
            color: {hover_color};
            text-decoration: underline;
        }}
        .project-tech {{
            color: {muted_text};
            font-size: 0.9rem;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 class='section-header'>PERSONAL DETAILS</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="resume-grid" style="margin-top: 1rem;">
        <div class="grid-left">Email:</div>
        <div class="grid-right"><a href="mailto:humzahanif786@gmail.com">humzahanif786@gmail.com</a></div>
    </div>
    <div class="resume-grid">
        <div class="grid-left">Portfolio:</div>
        <div class="grid-right"><a href="https://hamzahanif.techbyanum.com/index-1">Hamza Hanif</a></div>
    </div>
    <div class="resume-grid">
        <div class="grid-left">LinkedIn:</div>
        <div class="grid-right"><a href="http://www.linkedin.com/in/humzahanif786">Hamza Hanif</a></div>
    </div>
    <div class="resume-grid">
        <div class="grid-left">Mobile:</div>
        <div class="grid-right">+923452275566</div>
    </div>
    <div class="resume-grid">
        <div class="grid-left">Location:</div>
        <div class="grid-right">Karachi, Pakistan</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 class='section-header'>EDUCATION</h3>
    </div>
    <div class="item-row" style="margin-top: 1rem;">
        <div class="item-left">Aptech Certified Computer Professional Program</div>
        <div class="item-right">APTECH</div>
    </div>
    <div class="item-row">
        <div class="item-left">Advanced Diploma in Media Studies</div>
        <div class="item-right">Arena Multimedia</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 class='section-header'>CERTIFICATES</h3>
    </div>
    """, unsafe_allow_html=True)
    
    certificates = [
        ("ENGLISH LEARNING PROFICIENCY CERTIFICATE", "Askari English Learning Centre 2009"),
        ("COMPREHENSIVE ENGLISH LANGUAGE COURSE", "Innovative English Learning Centre"),
        ("NETWORKING", "Vocational Training Centre"),
        ("SERVER MANAGEMENT", "Vocational Training Centre"),
        ("CEH Training", "Moon International"),
        ("CERTIFICATE IN COMMUNICATION DESIGN", "Arena Multimedia"),
        ("ADVANCED DIPLOMA IN SOFTWARE ENGINEERING", "Aptech"),
        ("BASICS OF 3D ANIMATION", "Arena Multimedia"),
        ("GenAI Accelerator", "Aptech"),
        ("AI Nexus Architectures and Agents", "Aptech"),
    ]
    
    for cert_name, institute in certificates:
        st.markdown(f"""
        <div class="item-row"style="margin-bottom: 1.5rem;">
            <div class="item-left">{cert_name}</div>
            <div class="item-right">{institute}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h3 class='section-header'>EXPERIENCE</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="item-row" style="margin-top: 1rem;">
        <div class="item-left">FREELANCER</div>
        <div class="item-right">Web Developer & Designer</div>
    </div>
    <div class="item-row">
        <div class="item-left">FREELANCER</div>
        <div class="item-right">AI-Based Chatbot Development</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 class='section-header'>SKILLS</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="item-row" style="margin-top: 1rem;">
        <div class="item-left">Programming Languages</div>
        <div class="item-right">Html5, CSS, JavaScript, Bootstrap, Python, PHP</div>
    </div>
    <div class="item-row">
        <div class="item-left">Software</div>
        <div class="item-right">Visual Studio Code</div>
    </div>
    <div class="item-row">
        <div class="item-left">Database</div>
        <div class="item-right">MySQL</div>
    </div>
    <div class="item-row">
        <div class="item-left">Frameworks</div>
        <div class="item-right">Flask, Streamlit</div>
    </div>
    <div class="item-row">
        <div class="item-left">Content Management System</div>
        <div class="item-right">WordPress</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 class='section-header'>PROJECTS</h3>
    </div>
    """, unsafe_allow_html=True)
    
    projects = [
        ("Aqua Website On HTML", "Lang: HTML, CSS, JavaScript | S/F: Visual Studio Code", ""),
        ("TechFlow Solutions Chatbot Text", "Lang: HTML, CSS, JavaScript, Bootstrap, Python | S/F: Visual Studio Code", "https://hamzahanif.techbyanum.com/chatbot/Chatbottoggle"),
        ("TechFlow Solutions WhatsApp", "Lang: HTML, CSS, JavaScript, Bootstrap, Python | S/F: Visual Studio Code", "https://hamzahanif.techbyanum.com/chatbot/chatbotwhatsapp"),
        ("TechFlow Solutions Voice", "Lang: HTML, CSS, JavaScript, Bootstrap, Python | S/F: Visual Studio Code", "https://hamzahanif.techbyanum.com/chatbot/voicechatbot"),
        ("TechFlow Solutions Calling", "Lang: HTML, CSS, JavaScript, Bootstrap, Python | S/F: Visual Studio Code", "https://hamzahanif.techbyanum.com/chatbot/chatbotcalling"),
        ("TechFlow Calling Assistant", "Lang: HTML, CSS, JavaScript, Bootstrap, Python | S/F: Visual Studio Code", "https://hamzahanif.techbyanum.com/chatbot/chatbotvoice"),
        ("TechFlow Solutions AI Assistant", "Lang: Python | S/F: Visual Studio Code", "https://techflow-ai-assistant.streamlit.app"),
        ("ElevenLabs Remake", "Lang: Python | S/F: Visual Studio Code", "https://iielevenlabs-remake.streamlit.app"),
        ("Google Calendar AI Agent", "Lang: Python | S/F: Visual Studio Code", "https://app-calendar-ai-agent.streamlit.app"),
        ("Cartesia Remake", "Lang: Python | S/F: Visual Studio Code", "https://cartesia-remakes.streamlit.app"),
        ("AI Stock Analysis Agent", "Lang: Python | S/F: Visual Studio Code", "https://ai-stock-analysis-agent.streamlit.app"),
        ("AI Image Generator Pro", "Lang: Python | S/F: Visual Studio Code", "https://ai-image-generator-pro.streamlit.app"),
        ("Advanced Weather Radar & Satellite System", "Lang: Python | S/F: Visual Studio Code", "https://advanced-weather-radar-satellite-system.streamlit.app"),
        ("Advanced Translation Agent", "Lang: Python | S/F: Visual Studio Code", "https://advanced-translation-agent.streamlit.app"),
        ("Advanced RXN Chemistry Portal", "Lang: Python | S/F: Visual Studio Code", "https://advanced-rxn-chemistry.streamlit.app"),
        ("Advanced Live Crypto Chart", "Lang: Python | S/F: Visual Studio Code", "https://advanced-live-crypto-chart.streamlit.app"),
        ("Advanced Image AI Agent", "Lang: Python | S/F: Visual Studio Code", "https://advanced-image-editor-ai-agent.streamlit.app"),
        ("Advanced AI Search Agent", "Lang: Python | S/F: Visual Studio Code", "https://advanced-ai-search-agent.streamlit.app"),
        ("Advanced Crypto Trading Agent", "Lang: Python | S/F: Visual Studio Code", "https://advanced-crypto-trading-agent.streamlit.app"),
        ("Allin1Technologies", "Lang: HTML, CSS, JavaScript, PHP, MySQL | S/F: Visual Studio Code", ""),
    ]
    
    for idx, (project_name, tech, url) in enumerate(projects, 1):
        if url:
            project_html = f"""
            <div class="project-item">
                <div class="project-name">{idx}. <a href="{url}" target="_blank">{project_name}</a></div>
                <div class="project-tech">{tech}</div>
            </div>
            """
        else:
            project_html = f"""
            <div class="project-item">
                <div class="project-name">{idx}. {project_name}</div>
                <div class="project-tech">{tech}</div>
            </div>
            """
        st.markdown(project_html, unsafe_allow_html=True)

def contacts_page():
    theme = st.session_state.get('theme', 'dark')
    
    if theme == 'light':
        bg_color = '#ffffff'
        card_bg = '#f8f9fa'
        text_color = '#212529'
        border_color = '#dee2e6'
        accent_color = '#0d6efd'
        hover_color = '#0b5ed7'
        link_color = '#0a58ca'
        muted_text = '#6c757d'
        disabled_bg = '#e9ecef'
        disabled_text = '#6c757d'
        heading_color = '#212529'
    else:
        bg_color = '#1a1a1a'
        card_bg = '#2d2d2d'
        text_color = '#f8f9fa'
        border_color = '#495057'
        accent_color = '#0d6efd'
        hover_color = '#3d8bfd'
        link_color = '#85b6ff'
        muted_text = '#adb5bd'
        disabled_bg = '#343a40'
        disabled_text = '#adb5bd'
        heading_color = '#FFFFFF'  
    
    st.markdown(f"""
    <style>
        .contact-card {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }}
        .contact-card:hover {{
            box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
            border-color: {accent_color};
        }}
        .contact-info p {{
            margin: 0.75rem 0;
            color: {text_color};
        }}
        .contact-info strong {{
            color: {accent_color};
        }}
        .contact-info a {{
            color: {link_color};
            text-decoration: none;
            transition: color 0.2s;
        }}
        .contact-info a:hover {{
            color: {hover_color};
            text-decoration: underline;
        }}
        .btn-send-msg {{
            background: {accent_color} !important;
            color: white !important;
            border: 2px solid {accent_color} !important;
        }}
        .btn-send-msg:hover {{
            background: {hover_color} !important;
            border-color: {hover_color} !important;
        }}
        .map-container {{
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 2rem;
            border: 1px solid {border_color};
        }}
        h2, h3 {{
            color: {heading_color} !important;
        }}
    </style>
    
    <h2 style='color: {heading_color};'>📧 Contact Me</h2>
    <div class="map-container">
        <iframe 
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d462118.02904823136!2d66.59499074999999!3d24.8614622!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3eb33e06651d4bbf%3A0x9cf92f44555a0c23!2sKarachi%2C%20Pakistan!5e0!3m2!1sen!2s!4v1234567890123" 
            width="100%" 
            height="400" 
            style="border:0;" 
            allowfullscreen="" 
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade">
        </iframe>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown(f"<h3 style='color: {heading_color};'>📱 Contact Information</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="contact-card">
            <div class="contact-info">
                <p><strong>📧 Email:</strong> <a href="mailto:humzahanif786@gmail.com">humzahanif786@gmail.com</a></p>
                <p><strong>📞 Phone:</strong> <a href="tel:+923452275566">+923452275566</a></p>
                <p><strong>💼 LinkedIn:</strong> <a href="https://www.linkedin.com/in/humzahanif786" target="_blank">linkedin.com/in/humzahanif786</a></p>
                <p><strong>📍 Location:</strong> Karachi, Pakistan</p>
                <p><strong>⏰ Availability:</strong> 9 AM - 6 PM (PKT)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<h3 style='color: {heading_color};'>📝 Send a Message</h3>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <style>
            .stTextInput>div>div>input, 
            .stTextArea>div>div>textarea {{
                background-color: {card_bg} !important;
                
                border-color: {border_color} !important;
            }}
            .stTextInput>div>div>input:focus, 
            .stTextArea>div>div>textarea:focus {{
                border-color: {accent_color} !important;
                box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
                
            }}
            .stTextInput>label, 
            .stTextArea>label {{
                color: {heading_color} !important;
            }}
            .stTextInput>div>div>input::placeholder, 
            .stTextArea>div>div>textarea::placeholder {{
                
                opacity: 1;
            }}
            .stTextInput>div>div>input, 
            .stTextArea>div>div>textarea {{
                
            }}
        </style>
        """, unsafe_allow_html=True)
        
        name = st.text_input("Your Name *", key="contact_name")
        email = st.text_input("Your Email *", key="contact_email")
        subject = st.text_input("Subject *", key="contact_subject")
        message = st.text_area("Message *", height=150, key="contact_message")
        
        if name and email and subject and message:
            import urllib.parse
            mailto_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            mailto_link = f"mailto:humzahanif786@gmail.com?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(mailto_body)}"
            
            st.markdown(f"""
            <a href="{mailto_link}" class="stButton" style="text-decoration: none;">
                <button class="btn-send-msg" style="width: 100%; padding: 0.75rem; border-radius: 0.5rem; font-weight: bold; cursor: pointer; margin-top: 1rem;">
                    📧 Send Message
                </button>
            </a>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="width: 100%; padding: 0.75rem; background: {disabled_bg}; color: {disabled_text}; text-align: center; border-radius: 0.5rem; font-weight: bold; margin-top: 1rem; cursor: not-allowed; border: 1px solid {border_color};">
                📧 Send Message (Fill all required fields)
            </div>
            """, unsafe_allow_html=True)

def chatbot_page():
    theme = st.session_state.get('theme', 'dark')
    text_color = '#212121' if theme == 'light' else '#ffffff'
    bg_color = '#f5f5f5' if theme == 'light' else '#121212'
    card_bg = '#e0e0e0' if theme == 'light' else '#1e1e1e'
    border_color = '#9e9e9e' if theme == 'light' else '#424242'
    secondary_text = '#616161' if theme == 'light' else '#b0b0b0'
    
    st.markdown(f"""
    <style>
    /* Button styles */
    .stButton > button {{
        font-weight: bold !important;
        background: transparent !important;
        border: 2px solid #0000ff !important;
        color: #0000ff !important;
    }}
    .stButton > button:hover {{
        background: #0000ff !important;
        color: white !important;
    }}
    
    /* Input field styles */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stChatInput > div > div > textarea {{
        color: {text_color} !important;
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
    }}
    
    /* Chat input specific */
    .stChatInput > div > div > textarea {{
        color: {text_color} !important;
    }}
    
    /* Focus states */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stChatInput > div > div > textarea:focus {{
        border-color: #0000ff !important;
        box-shadow: 0 0 0 0.2rem rgba(0, 0, 255, 0.25) !important;
        color: {text_color} !important;
    }}
    
    /* Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stChatInput > label {{
        color: {text_color} !important;
    }}
    
    /* Chat message bubbles */
    .stChatMessage {{
        color: {text_color} !important;
    }}
    
    /* Chat input placeholder */
    .stChatInput ::placeholder {{
        color: {secondary_text} !important;
        opacity: 1;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Add additional styling for chat input
    st.markdown("""
    <style>
        /* Override Streamlit's default chat input styles */
        .stChatInput {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1rem;
            background: var(--background-color);
            z-index: 100;
        }
        
        /* Ensure chat messages don't get hidden behind the fixed input */
        .stChatMessageContainer {
            padding-bottom: 120px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    if 'chat_mode' not in st.session_state:
        st.session_state.chat_mode = 'text'
    
    st.markdown("""
    <style>
        div[data-testid="column"] {
            padding: 0 4px !important;
        }
        .stButton > button {
            width: 100%;
            border-radius: 8px !important;
            padding: 8px 0 !important;
            margin: 4px 0 !important;
            border: 2px solid #0000ff !important;
            background: transparent !important;
            color: #0000ff !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            background: #0000ff !important;
            color: white !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,255,0.2) !important;
        }
        .stButton > button[data-testid="baseButton-secondary"] {
            background: #0000ff !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns(4, gap="small")
    
    with cols[0]:
        if st.button("💬 Text Chat", 
                   use_container_width=True, 
                   key="text_chat_btn",
                   type="primary" if st.session_state.get('chat_mode') == 'text' else "secondary"):
            st.session_state.chat_mode = 'text'
            st.rerun()
            
    with cols[1]:
        if st.button("🎤 Voice Chat", 
                   use_container_width=True, 
                   key="voice_chat_btn",
                   type="primary" if st.session_state.get('chat_mode') == 'voice' else "secondary"):
            st.session_state.chat_mode = 'voice'
            st.rerun()
            
    with cols[2]:
        if st.button("📱 WhatsApp", 
                   use_container_width=True, 
                   key="whatsapp_btn",
                   type="primary" if st.session_state.get('chat_mode') == 'whatsapp' else "secondary"):
            st.session_state.chat_mode = 'whatsapp'
            st.rerun()
            
    with cols[3]:
        if st.button("📞 Call Now", 
                   use_container_width=True, 
                   key="call_btn",
                   type="primary" if st.session_state.get('chat_mode') == 'call' else "secondary"):
            st.session_state.chat_mode = 'call'
            st.rerun()
    
    if st.session_state.chat_mode == 'voice':
        st.markdown("### 🎤 Voice Chat Assistant")
        
        # Use theme-aware colors for the info message
        theme = st.session_state.get('theme', 'dark')
        if theme == 'light':
            st.markdown("""
            <div style="background-color: #e6f0ff; color: #0047b3; padding: 0.75rem; border-radius: 0.5rem; border-right: 4px solid #4d94ff; margin: 1rem 0;">
                💡 <strong>How to use:</strong> Click the microphone button, speak your question, then send your message
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #1a2b4a; color: #8ab4f8; padding: 0.75rem; border-radius: 0.5rem; border-left: 4px solid #4d94ff; margin: 1rem 0;">
                💡 <strong>How to use:</strong> Click the microphone button, speak your question, then send your message
            </div>
            """, unsafe_allow_html=True)
        
        st.components.v1.html("""
        <div style="background: linear-gradient(135deg, #0000ff 0%, #0051ff 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center;">
            <h2 style="margin-bottom: 1rem;">🎤 Voice-Enabled AI Assistant</h2>
            <p style="margin-bottom: 2rem;">Click the microphone to speak your question</p>
            
            <button id="voiceBtn" onclick="toggleVoice()" style="
                background: white;
                color: #0000ff;
                border: none;
                padding: 1.5rem 3rem;
                border-radius: 50px;
                font-size: 2rem;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            ">
                🎤
            </button>
            
            <p id="status" style="margin-top: 1.5rem; font-size: 1.1rem; font-weight: bold;">Ready to listen...</p>
            <p id="transcript" style="margin-top: 1rem; font-size: 1rem; min-height: 30px; background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px;"></p>
            
            <button id="copyBtn" onclick="copyTranscript()" style="
                background: #4CAF50;
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 5px;
                font-size: 1rem;
                cursor: pointer;
                margin-top: 1rem;
                display: none;
            ">
                📋 Copy Transcript
            </button>
        </div>
        
        <script>
        let recognition;
        let isListening = false;
        
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'en-US';
            
            recognition.onstart = () => {
                document.getElementById('status').textContent = '🔴 Listening...';
                document.getElementById('voiceBtn').style.background = '#ff4444';
                document.getElementById('voiceBtn').style.color = 'white';
            };
            
            recognition.onresult = (event) => {
                const transcript = Array.from(event.results)
                    .map(result => result[0].transcript)
                    .join('');
                document.getElementById('transcript').textContent = transcript;
            };
            
            recognition.onend = () => {
                isListening = false;
                document.getElementById('voiceBtn').style.background = 'white';
                document.getElementById('voiceBtn').style.color = '#0000ff';
                
                const finalTranscript = document.getElementById('transcript').textContent;
                if (finalTranscript) {
                    document.getElementById('status').textContent = '✅ Transcript ready! Copy it below.';
                    document.getElementById('copyBtn').style.display = 'inline-block';
                } else {
                    document.getElementById('status').textContent = 'No speech detected. Try again.';
                }
            };
            
            recognition.onerror = (event) => {
                document.getElementById('status').textContent = 'Error: ' + event.error;
                isListening = false;
            };
        }
        
        function toggleVoice() {
            if (!recognition) {
                alert('Speech recognition not supported');
                return;
            }
            if (isListening) {
                recognition.stop();
                isListening = false;
            } else {
                document.getElementById('transcript').textContent = '';
                document.getElementById('copyBtn').style.display = 'none';
                recognition.start();
                isListening = true;
            }
        }
        
        function copyTranscript() {
            const transcript = document.getElementById('transcript').textContent;
            navigator.clipboard.writeText(transcript).then(() => {
                const btn = document.getElementById('copyBtn');
                btn.textContent = '✅ Copied!';
                btn.style.background = '#2196F3';
                setTimeout(() => {
                    btn.textContent = '📋 Copy Transcript';
                    btn.style.background = '#4CAF50';
                }, 2000);
            });
        }
        </script>
        """, height=450)
        
        st.markdown("---")
        st.markdown("### 💬 Voice Response")
        
        if "voice_messages" not in st.session_state:
            st.session_state.voice_messages = []
        
        # Create a container for the input row
        input_container = st.container()
        with input_container:
            col_input, col_send = st.columns([4, 1])
            with col_input:
                # Get current theme colors
                theme = st.session_state.get('theme', 'dark')
                colors = {
                    'light': {
                        'text': '#212121',
                        'border': '#9e9e9e',
                        'accent': '#424242',
                        'muted': '#616161',
                        'bg': '#ffffff'
                    },
                    'dark': {
                        'text': '#ffffff',
                        'border': '#424242',
                        'accent': '#bdbdbd',
                        'muted': '#9e9e9e',
                        'bg': '#1e1e1e'
                    }
                }
                colors = colors.get(theme, colors['dark'])
                
                st.markdown(f"""
                <style>
                    div[data-testid="stTextInput"] > div > div > input {{
                        color: {colors['text']} !important;
                        background-color: {colors['bg']} !important;
                        border: 1px solid {colors['border']} !important;
                        padding: 0.5rem 1rem !important;
                        height: 42px !important;
                        box-sizing: border-box !important;
                        border-radius: 4px !important;
                    }}
                    div[data-testid="stTextInput"] > div > div > input:focus {{
                        border-color: {colors['accent']} !important;
                        box-shadow: 0 0 0 1px {colors['accent']} !important;
                    }}
                    div[data-testid="stTextInput"] > label {{
                        color: {colors['text']} !important;
                        margin-bottom: 0.25rem !important;
                    }}
                    div[data-testid="stTextInput"] > div > div > input::placeholder {{
                        color: {colors['muted']} !important;
                        opacity: 0.7 !important;
                    }}
                    /* Align button with input field */
                    .stButton > button {{
                        height: 42px !important;
                        margin-top: 1.5rem !important;
                        border-radius: 4px !important;
                        font-weight: 500 !important;
                    }}
                </style>
                """, unsafe_allow_html=True)
                user_input = st.text_input(
                    "Your question:",
                    key="voice_text_input",
                    placeholder="Type or paste your voice transcript here",
                    label_visibility="visible"
                )
            with col_send:
                st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
                send_voice = st.button("📤 Send", key="voice_send_btn", use_container_width=True)
        
        if send_voice and user_input:
            response = process_message(user_input)
            st.session_state.voice_messages.append({"role": "user", "content": user_input})
            st.session_state.voice_messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.session_state.voice_messages:
            st.markdown("---")
            st.markdown("### 💬 Conversation")
            for msg in st.session_state.voice_messages[-4:]:
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**AI:** {msg['content']}")
                    st.components.v1.html(f"""
                    <button onclick="speakResponse('{msg['content']}')" style="
                        background: #0000ff;
                        color: white;
                        border: none;
                        padding: 0.5rem 1rem;
                        border-radius: 5px;
                        cursor: pointer;
                        margin-top: 0.5rem;
                    ">
                        🔊 Play Audio
                    </button>
                    <script>
                    function speakResponse(text) {{
                        const utterance = new SpeechSynthesisUtterance(text);
                        utterance.rate = 0.9;
                        window.speechSynthesis.speak(utterance);
                    }}
                    </script>
                    """, height=50)
            
            if st.button("🗑️ Clear Voice Chat"):
                st.session_state.voice_messages = []
                st.rerun()
    
    elif st.session_state.chat_mode == 'whatsapp':
        st.markdown("""
        <div class="info-box">
            <p>📱 WhatsApp Chat</p>
            <p>Click the button below to start a WhatsApp conversation:</p>
            <a href="https://wa.me/923452275566?text=Hi%20Hamza!" target="_blank" style="display: inline-block; background: #25D366; color: white; padding: 1rem 2rem; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 1rem;">
                💬 Open WhatsApp
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.chat_mode == 'call':
        st.markdown("""
        <div class="info-box">
            <p>📞 Contact Options</p>
        </div>
        """, unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            **📞 Phone Call**
            [+923452275566](tel:+923452275566)
            
            **📧 Email**
            [humzahanif786@gmail.com](mailto:humzahanif786@gmail.com)
            """)
        with col_b:
            st.markdown("""
            **💼 LinkedIn**
            [linkedin.com/in/humzahanif786](http://www.linkedin.com/in/humzahanif786)
            
            **⏰ Available**
            9 AM - 6 PM (PKT)
            """)
    
    elif st.session_state.chat_mode == 'info':
        with st.expander("What can I help you with?"):
            st.markdown("""
            **Ask me about:**
            - 👤 Personal Info
            - 🛠️ Skills & technologies
            - 💼 Projects & portfolio
            - 🎓 Education & certificates
            - 💻 Experience
            - 📧 Contact information
            - 🚀 Services offered
            """)
    
    else:
        # Modern Text Chat Interface with improved layout
        st.markdown(f"""
        <style>
            /* Root variables for theming */
            :root {{
                --primary-color: #0000ff;
                --primary-light: #4d94ff;
                --bg-color: {'#f8f9fa' if theme == 'light' else '#121212'};
                --card-bg: {'#ffffff' if theme == 'light' else '#1e1e1e'};
                --text-color: {'#212121' if theme == 'light' else '#ffffff'};
                --border-color: {'#e0e0e0' if theme == 'light' else '#424242'};
                --muted-text: {'#616161' if theme == 'light' else '#b0b0b0'};
                --shadow: {'0 4px 20px rgba(0, 0, 0, 0.1)' if theme == 'light' else '0 4px 20px rgba(0, 0, 0, 0.3)'};
            }}
            
            /* Main chat container */
            .chat-interface {{
                display: flex;
                flex-direction: column;
                height: 70vh;
                max-width: 100%;
                margin: 0 auto;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: var(--shadow);
                background: var(--card-bg);
                border: 1px solid var(--border-color);
            }}
            
            /* Chat header */
            .chat-header {{
                background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
                color: white;
                padding: 1rem;
                text-align: center;
                font-weight: 600;
                font-size: 1.2rem;
                position: relative;
                z-index: 10;
            }}
            
            /* Messages area */
            .chat-messages {{
                flex: 1;
                padding: 1rem;
                overflow-y: auto;
                background-color: var(--bg-color);
                scroll-behavior: smooth;
                display: flex;
                flex-direction: column;
                gap: 0.75rem;
            }}
            
            /* Message bubbles */
            .message {{
                max-width: 80%;
                padding: 0.75rem 1rem;
                border-radius: 1rem;
                line-height: 1.5;
                position: relative;
                animation: fadeIn 0.3s ease-out;
                word-wrap: break-word;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }}
            
            /* User message */
            .user-message {{
                background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
                color: white;
                margin-left: auto;
                border-bottom-right-radius: 0.25rem;
            }}
            
            /* Assistant message */
            .assistant-message {{
                background-color: var(--card-bg);
                color: var(--text-color);
                margin-right: auto;
                border: 1px solid var(--border-color);
                border-bottom-left-radius: 0.25rem;
            }}
            
            /* Input area */
            .chat-input-container {{
                padding: 1rem;
                background: var(--card-bg);
                border-top: 1px solid var(--border-color);
                display: flex;
                gap: 0.75rem;
                align-items: center;
            }}
            
            /* Input field */
            .chat-input {{
                flex: 1;
                padding: 0.75rem 1.25rem;
                border: 1px solid var(--border-color);
                border-radius: 2rem;
                font-size: 1rem;
                transition: all 0.3s ease;
                background-color: var(--bg-color);
                color: var(--text-color);
                min-height: 2.5rem;
            }}
            
            .chat-input:focus {{
                outline: none;
                border-color: var(--primary-color);
                box-shadow: 0 0 0 2px rgba(0, 0, 255, 0.1);
            }}
            
            /* Send button */
            .send-button {{
                background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
                color: white;
                border: none;
                border-radius: 50%;
                width: 2.75rem;
                height: 2.75rem;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.2s ease;
                flex-shrink: 0;
            }}
            
            .send-button:hover {{
                transform: scale(1.05);
                box-shadow: 0 4px 12px rgba(0, 0, 255, 0.2);
            }}
            
            /* Clear button */
            .clear-button {{
                display: block;
                margin: 0.75rem auto;
                background: transparent;
                color: var(--muted-text);
                border: 1px solid var(--border-color);
                padding: 0.4rem 1.25rem;
                border-radius: 1.5rem;
                cursor: pointer;
                transition: all 0.2s ease;
                font-size: 0.9rem;
            }}
            
            .clear-button:hover {{
                background: rgba(255, 0, 0, 0.05);
                color: #ff4d4d;
                border-color: #ff4d4d;
            }}
            
            /* Animations */
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {{
                width: 6px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: transparent;
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: var(--muted-text);
                border-radius: 3px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: var(--primary-color);
            }}
            
            /* Typing indicator */
            .typing-indicator {{
                display: flex;
                gap: 0.5rem;
                padding: 0.75rem 1rem;
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-radius: 1rem;
                width: fit-content;
                margin-bottom: 0.75rem;
            }}
            
            .typing-dot {{
                width: 8px;
                height: 8px;
                background-color: var(--muted-text);
                border-radius: 50%;
                display: inline-block;
                animation: typingAnimation 1.4s infinite ease-in-out both;
            }}
            
            .typing-dot:nth-child(1) {{ animation-delay: -0.32s; }}
            .typing-dot:nth-child(2) {{ animation-delay: -0.16s; }}
            
            @keyframes typingAnimation {{
                0%, 80%, 100% {{ transform: scale(0); }}
                40% {{ transform: scale(1); }}
            }}
        </style>
        """, unsafe_allow_html=True)
        
        # Theme variables
        theme = st.session_state.get('theme', 'dark')
        theme_colors = {
            'light': {
                '--background-color': '#f8f9fa',
                '--card-bg': '#ffffff',
                '--text-color': '#212121',
                '--border-color': '#e0e0e0',
            },
            'dark': {
                '--background-color': '#121212',
                '--card-bg': '#1e1e1e',
                '--text-color': '#ffffff',
                '--border-color': '#333333',
            }
        }
        
        # Apply theme
        theme_vars = theme_colors[theme]
        for var, value in theme_vars.items():
            st.markdown(f"""
            <style>
                :root {{
                    {var}: {value};
                }}
            </style>
            """, unsafe_allow_html=True)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi there! I'm your AI assistant. How can I help you today? 🚀"}
            ]
        
        # Chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Chat header
        st.markdown('<div class="chat-header">💬 AI Assistant</div>', unsafe_allow_html=True)
        
        # Messages area with better spacing
        st.markdown('''
        <div class="chat-messages" id="chat-messages" style="padding: 1rem;">
            <div style="margin-bottom: 1.5rem;"></div>  <!-- Extra space at the top -->
        ''', unsafe_allow_html=True)
        
        # Display messages with proper spacing
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f'''
                <div class="message user-message">
                    {message["content"]}
                </div>
                ''', unsafe_allow_html=True)
            else:
                # Add margin to the welcome message
                margin_style = 'margin-bottom: 40px;' if i == 0 and "Hi there! I'm your AI assistant" in message["content"] else ''
                st.markdown(f'''
                <div class="message assistant-message" style="{margin_style}">
                    {message["content"]}
                </div>
                ''', unsafe_allow_html=True)
        
        # chat-messages div is closed by Streamlit automatically
        
        # Input area
        input_col, button_col = st.columns([6, 1])
        
        with input_col:
            user_input = st.text_input(
                "Type your message...",
                key="chat_input",
                label_visibility="collapsed",
                on_change=None
            )
        
        with button_col:
            if st.button("➤", key="send_button", use_container_width=True):
                if user_input.strip():
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    
                    # Get AI response
                    response = process_message(user_input)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Rerun to update the chat
                    st.rerun()
        
        # Chat container is closed by Streamlit automatically
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi there! I'm your AI assistant. How can I help you today? 🚀"}
            ]
            st.rerun()
        
        # Auto-scroll to bottom
        st.markdown("""
        <script>
            const messages = document.getElementById('chat-messages');
            messages.scrollTop = messages.scrollHeight;
        </script>
        """, unsafe_allow_html=True)

def main():
    if 'page' not in st.session_state:
        st.session_state.page = "About"
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'  # Set default to light mode
    
    load_css(st.session_state.theme)
    
    with st.sidebar:
        st.image("images/logo1.png", use_container_width=True)
        st.markdown("---")
        
        current_theme = st.session_state.theme
        button_label = "☀️ Light Mode" if current_theme == "dark" else "🌙 Dark Mode"
        if st.button(button_label, use_container_width=True, key="theme_toggle"):
            st.session_state.theme = "light" if current_theme == "dark" else "dark"
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🏠 About", use_container_width=True):
            st.session_state.page = "About"
        if st.button("💼 Portfolio", use_container_width=True):
            st.session_state.page = "Portfolio"
        if st.button("📄 Resume", use_container_width=True):
            st.session_state.page = "Resume"
        if st.button("📧 Contacts", use_container_width=True):
            st.session_state.page = "Contacts"
        if st.button("🤖 AI Chatbot", use_container_width=True):
            st.session_state.page = "Chatbot"
        
        st.markdown("---")
        st.markdown("### 📞 Quick Contact")
        st.markdown("**Email**: [humzahanif786@gmail.com](mailto:humzahanif786@gmail.com)")
        st.markdown("**Phone**: [+92 345 2275566](tel:+923452275566)")
        st.markdown("---")
        st.markdown(f"© {datetime.now().year} Hamza Hanif")
    
    if st.session_state.page == "About":
        home_page()
    elif st.session_state.page == "Portfolio":
        portfolio_page()
    elif st.session_state.page == "Resume":
        resume_page()
    elif st.session_state.page == "Contacts":
        contacts_page()
    elif st.session_state.page == "Chatbot":
        chatbot_page()
    
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>Hamza Hanif</strong> - Web Developer, Designer & AI Chatbot Developer</p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()