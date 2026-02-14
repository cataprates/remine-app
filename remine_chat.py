import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. API CONFIGURATION & AI BRAIN (SECURE)
# ==========================================
CHAVE_API = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=CHAVE_API)

instrucoes_sistema = """
You are RE-MINE, an expert AI in urban mining. 
When analyzing photos of electronics, format your response EXACTLY like this using markdown:

### 📱 Object Detected: [Name]

💰 **Estimated Value:** $[Amount] USD

**💎 Precious Metals Inside:**
* [Metal] - [Location]

**🛠️ Tear-Down Guide:**
1. [Step 1]

**🌍 Where to Sell:**
[Global selling options]

⚠️ [Hazard warnings if any]
"""

model = genai.GenerativeModel(
    'models/gemini-2.5-flash',
    system_instruction=instrucoes_sistema
)

# ==========================================
# 2. UI SETUP & CANVA DESIGN INJECTION
# ==========================================
st.set_page_config(page_title="RE-MINE: Urban Mining", page_icon="🟣", layout="centered")

custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Audiowide&family=Inter:wght@400;600&display=swap');

/* Main Background (Grey from your Canva) */
.stApp {
    background-color: #6A6A6A !important;
}

/* --- HEADER --- */
header[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* "RE-MINE" Title */
h1 {
    font-family: 'Audiowide', sans-serif !important;
    color: #DDA0DD !important; /* Lilac/Purple from your Canva */
    font-size: 3.5rem !important;
    text-transform: uppercase !important;
    letter-spacing: 3px !important;
    text-align: center !important;
    padding-top: 1rem !important;
}

/* Hide Streamlit stuff */
#MainMenu, footer {display: none !important;}
[data-testid="stHeaderActionElements"] {display: none !important;}

/* --- CHAT AREA (WHITE BOX) --- */
.stMainBlockContainer {
    background-color: #FFFFFF !important;
    border-radius: 25px 25px 0 0 !important;
    padding: 20px !important;
    margin-top: 20px !important;
    max-width: 800px !important;
}

/* --- CHAT BUBBLES (BLACK) --- */
[data-testid="stChatMessage"] {
    background-color: #1E1E1E !important; 
    color: #FFFFFF !important;
    border-radius: 20px !important;
    padding: 15px 20px !important;
    margin-bottom: 20px !important;
    border: none !important;
}

/* User Bubble alignment (Creates the sharp tail corner) */
[data-testid="stChatMessage"][data-testid*="user"] {
    border-bottom-right-radius: 4px !important; 
    background-color: #2A2A2A !important;
}

/* AI Bubble alignment (Creates the sharp tail corner) */
[data-testid="stChatMessage"][data-testid*="assistant"] {
    border-bottom-left-radius: 4px !important; 
}

/* Hide default avatars to match your Canva */
[data-testid="stChatMessageAvatar"] {
    display: none !important;
}

/* --- CHAT INPUT (BLACK PILL) --- */
[data-testid="stChatInput"] {
    padding-bottom: 20px !important;
    background-color: #FFFFFF !important; 
}

[data-testid="stChatInput"] > div {
    background-color: #1E1E1E !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 5px 15px !important;
}

/* Text and icons inside input */
[data-testid="stChatInput"] textarea {
    color: #FFFFFF !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #888888 !important;
}
[data-testid="stChatInput"] button {
    color: #DDA0DD !important; /* Lilac accent for the paperclip/send button */
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("RE-MINE")

# ==========================================
# 3. CHAT MEMORY SETUP
# ==========================================
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Upload a photo of an electronic device, and I'll tell you its hidden value.", "image": None}]

# Render previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("image"):
            st.image(msg["image"], width=250)
        if msg["content"]:
            st.markdown(msg["content"])

# ==========================================
# 4. CHAT INPUT WITH PAPERCLIP
# ==========================================
prompt = st.chat_input("Ask me anything...", accept_file=True, file_type=["png", "jpg", "jpeg"])

if prompt:
    user_text = prompt.text
    user_files = prompt.files
    
    with st.chat_message("user"):
        img_to_show = None
        if user_files:
            img_to_show = Image.open(user_files[0])
            st.image(img_to_show, width=250)
        if user_text:
            st.markdown(user_text)
            
    st.session_state.messages.append({
        "role": "user", 
        "content": user_text, 
        "image": img_to_show
    })
    
    gemini_input = []
    if user_files:
        gemini_input.append(img_to_show)
    
    if user_text:
        gemini_input.append(user_text)
    elif user_files:
        gemini_input.append("Please analyze this electronic component and give me the breakdown.")
        
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                res = st.session_state.chat_session.send_message(gemini_input)
                st.markdown(res.text)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": res.text, 
                    "image": None
                })
            except Exception as e:
                st.error(f"Analysis Error: {e}")
