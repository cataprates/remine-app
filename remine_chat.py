import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. API CONFIGURATION (SECURE)
# ==========================================
CHAVE_API = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=CHAVE_API)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# ==========================================
# 2. UI SETUP & MODERN DESIGN INJECTION
# ==========================================
st.set_page_config(page_title="RE-MINE: Urban Mining", page_icon="💎", layout="centered")

# --- CUSTOM MODERN DESIGN (CSS INJECTION) ---
custom_css = """
<style>
/* 1. Sleek modern font (Poppins) */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif !important;
}

/* 2. Premium Dark Gradient Background */
.stApp {
    background: linear-gradient(135deg, #121212, #1e1e1e);
    color: #ffffff;
}

/* 3. Glassmorphism Chat Bubbles */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* 4. Glowing Neon Camera Box */
[data-testid="stCameraInput"] {
    border-radius: 20px;
    overflow: hidden;
    border: 2px solid #00FF41; /* Hacker Matrix Green */
    box-shadow: 0 4px 15px rgba(0, 255, 65, 0.2);
}

/* 5. Hide ugly default Streamlit menus */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 6. Premium Gradient Title */
h1 {
    font-weight: 600 !important;
    background: -webkit-linear-gradient(#00FF41, #008F11);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
# --------------------------------------------

st.title("RE-MINE")
st.write("Scan old electronics, discover their hidden value, and learn where to sell them.")

# ==========================================
# 3. CHAT MEMORY SETUP
# ==========================================
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# 4. CAMERA & ANALYSIS
# ==========================================
foto = st.camera_input("📸 Scan Component")

if foto:
    img = Image.open(foto)
    st.image(img, caption="Extracting data...", use_container_width=True)
    
    # Upgraded structured prompt for prettier AI answers
    prompt = """
    You are RE-MINE, an expert AI in urban mining. 
    Format your response EXACTLY like this using markdown and emojis:
    
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
    
    try:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing metals..."):
                response = st.session_state.chat_session.send_message([prompt, img])
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Analysis Error: {e}")

# ==========================================
# 5. CHAT INPUT
# ==========================================
if pergunta := st.chat_input("Ask me how to dismantle or sell this..."):
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.messages.append({"role": "user", "content": pergunta})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            res = st.session_state.chat_session.send_message(pergunta)
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
