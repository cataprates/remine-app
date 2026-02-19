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
model = genai.GenerativeModel(
    'models/gemini


