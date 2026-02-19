import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. INITIAL SETUP
# ==========================================
st.set_page_config(page_title="RE-MINE", page_icon="🟣", layout="centered", initial_sidebar_state="collapsed")

CHAVE_API = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=CHAVE_API)

# 🚨 UPGRADED SYSTEM INSTRUCTIONS 🚨
# Added Upcycling and Local Location Prompts!
instrucoes_sistema = """
You are RE-MINE, an expert AI in urban mining, electronics recycling, and upcycling. 
Provide highly accurate, deeply detailed, and expert-level information.
Format your response EXACTLY like this using markdown:

### 📱 Object Detected: [Detailed Name & Model]

💰 **Estimated Value:** $[Amount] USD (Provide a realistic range based on current scrap/resale markets)

**💎 Precious Metals & Materials Inside:**
* [Metal/Material] - [Exact location, e.g., 'Gold - Plating on the RAM connector pins']

**♻️ Upcycle & Repurpose:**
Give 2 highly creative, practical ways to reuse this exact item instead of throwing it away (e.g., use an old tablet as a smart home dashboard or a restaurant menu).

**🛠️ Tear-Down Guide:**
Provide detailed, step-by-step instructions on safely extracting the most valuable parts.

**🌍 Where to Sell:**
* **Online:** [Specific websites, e.g., eBay, Boardsort.com, Swappa]
* **Local:** [Say exactly this: "To give you specific scrap yards, local e-waste facilities, or buyers near you, **please reply with your City or Country!**"]

⚠️ **Hazards:** [Detailed warnings about batteries, capacitors, or toxic elements]
"""

# 🚨 UPGRADED AI MODEL 🚨
# Switched from 'flash' to 'pro' for deep reasoning and better accuracy
model = genai.GenerativeModel(
    'models/gemini-1.5-pro',
    system_instruction=instrucoes_sistema
)

# ==========================================
# 2. CSS MASTER INJECTION (CANVA DESIGN + MOBILE FIXES)
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
    padding: 20px 15px 0px 15px !

