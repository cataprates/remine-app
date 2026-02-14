import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. INITIAL SETUP
# ==========================================
st.set_page_config(page_title="RE-MINE", page_icon="🟣", layout="centered", initial_sidebar_state="collapsed")

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
# 2. CSS MASTER INJECTION
# ==========================================
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Audiowide&family=Inter:wght@400;500;600&display=swap');

.stApp { background-color: #727272 !important; }
[data-testid="stHeader"] { display: none !important; }

.custom-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #727272 !important;
    z-index: 99999;
    text-align: center;
    padding: 50px 0 20px 0;
}
.custom-header h1 {
    font-family: 'Audiowide', sans-serif !important;
    color: #DDA0DD !important; 
    font-size: 3rem !important;
    margin: 0 !important;
    letter-spacing: 2px !important;
    line-height: 1 !important;
}

[data-testid="stMainBlockContainer"] {
    background-color: #FFFFFF !important;
    border-radius: 30px 30px 0 0 !important;
    margin-top: 100px !important; 
    padding: 20px 15px 150px 15px !important; 
    max-width: 800px !important;
    min-height: 100vh !important;
}

[data-testid="stBottom"] {
    background-color: #FFFFFF !important; 
    z-index: 99998 !important;
}
[data-testid="stBottom"] > div {
    background-color: #FFFFFF !important;
    padding: 10px 20px 30px 20px !important; 
    max-width: 800px !important;
    margin: 0 auto !important;
}

[data-testid="stChatInput"] { background-color: transparent !important; }
[data-testid="stChatInput"] > div {
    background-color: #222222 !important;
    border-radius: 50px !important;
    border: none !important;
    padding: 5px 15px !important;
}
[data-testid="stChatInput"] textarea {
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stChatInput"] button { color: #DDA0DD !important; }
[data-testid="stChatInput"] svg { fill: #DDA0DD !important; }

[data-testid="stChatMessageAvatar"] { display: none !important; }
[data-testid="stChatMessage"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin-bottom: 20px !important;
    gap: 0 !important; 
}

[data-testid="stChatMessageContent"] {
    background-color: #222222 !important;
    color: #FFFFFF !important;
    padding: 15px 20px !important;
    width: fit-content !important;
    max-width: 85% !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stChatMessage"][data-testid*="assistant"] {
    flex-direction: row !important;
    justify-content: flex-start !important;
}
[data-testid="stChatMessage"][data-testid*="assistant"] [data-testid="stChatMessageContent"] {
    border-radius: 2
