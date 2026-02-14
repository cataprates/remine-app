import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. INITIAL SETUP (MUST BE FIRST)
# ==========================================
st.set_page_config(page_title="RE-MINE", page_icon="🟣", layout="centered", initial_sidebar_state="collapsed")

# ==========================================
# 2. API CONFIGURATION
# ==========================================
CHAVE_API = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=CHAVE_API)

instrucoes_sistema = """
You are RE-MINE, an expert AI in urban mining. 
Format your response EXACTLY like this using markdown:
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
# 3. CSS MASTER INJECTION (BUG FIXES)
# ==========================================
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Audiowide&family=Inter:wght@400;500;600&display=swap');

/* 1. Global Background */
.stApp {
    background-color: #727272 !important; 
}

/* Hide Streamlit's default header */
[data-testid="stHeader"] {
    display: none !important;
}

/* 2. Custom Fixed Header (Grey Area) */
.custom-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #727272 !important;
    z-index: 99999;
    text-align: center;
    padding: 50px 0 20px 0; /* Pushes it down safely below mobile clocks/batteries */
}
.custom-header h1 {
    font-family: 'Audiowide', sans-serif !important;
    color: #DDA0DD !important; /* Canva Lilac */
    font-size: 3rem !important;
    margin: 0 !important;
    letter-spacing: 2px !important;
    line-height: 1 !important;
}

/* 3. The White Chat Area */
[data-testid="stMainBlockContainer"] {
    background-color: #FFFFFF !important;
    border-radius: 30px 30px 0 0 !important;
    margin-top: 100px !important; /* Pushes the white box down so the grey header shows */
    padding: 20px 15px 150px 15px !important; /* Massive bottom padding so text doesn't hide behind input */
    max-width: 800px !important;
    min-height: 100vh !important;
}

/* 4. Chat Input Bar Fix (Stops the overlapping bug!) */
[data-testid="stBottom"] {
    background-color: #FFFFFF !important; /* Solid white hides scrolling text! */
    z-index: 99998 !important;
}
[data-testid="stBottom"] > div {
    background-color: #FFFFFF !important;
    padding: 10px 20px 30px 20px !important; 
    max-width: 800px !important;
    margin: 0 auto !important;
}

/* The Black Pill Input */
[data-testid="stChatInput"] {
    background-
