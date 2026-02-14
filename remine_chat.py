import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. API CONFIGURATION
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
# 2. UI SETUP & CANVA CSS INJECTION
# ==========================================
st.set_page_config(page_title="RE-MINE", page_icon="🟣", layout="centered")

custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Audiowide&family=Inter:wght@400;500;600&display=swap');

/* 1. Entire App Background (Canva Grey) */
[data-testid="stAppViewContainer"], .stApp {
    background-color: #727272 !important; 
}

/* 2. Hide Streamlit's Default Header */
[data-testid="stHeader"] {
    display: none !important;
}

/* 3. The "RE-MINE" Title (Pinned to the top grey area) */
.canva-title {
    position: fixed;
    top: 0px;
    left: 0;
    width: 100%;
    background-color: #727272;
    color: #DDA0DD; /* Canva Lilac */
    font-family: 'Audiowide', sans-serif;
    font-size: 3.5rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    text-align: center;
    padding: 20px 0 10px 0;
    z-index: 99999; /* Keeps it above everything */
    margin: 0;
}

/* 4. The White Chat Card */
[data-testid="stMainBlockContainer"] {
    background-color: #FFFFFF !important;
    border-radius: 25px 25px 0 0 !important;
    margin-top: 90px !important; /* Pushes the white box down so the title fits! */
    padding: 20px !important;
    padding-bottom: 100px !important;
    max-width: 600px !important;
    min-height: 100vh !important; /* Stretches white to the bottom */
}

/* 5. Make the bottom input area white so it blends seamlessly */
[data-testid="stBottom"] {
    background-color: transparent !important;
}
[data-testid="stBottom"] > div {
    background-color: #FFFFFF !important;
    max-width: 600px !important;
    margin: 0 auto !important;
    padding-bottom: 25px !important;
}

/* 6. Chat Bubbles (Canva Black) */
[data-testid="stChatMessageAvatar"] {
    display: none !important; /* Hides the default robot/user icons */
}
[data-testid="stChatMessage"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin-bottom: 15px !important;
}
[data-testid="stChatMessageContent"] {
    background-color: #222222 !important; /* Black bubbles */
    color: #FFFFFF !important; /* White text */
    padding: 15px 20px !important;
    border-radius: 15px !important;
    border-bottom-left-radius: 4px !important; /* The sharp tail effect */
    width: fit-content !important;
    max-width: 90% !important;
    font-family: 'Inter', sans-serif !important;
}

/* 7. Chat Input Bar (Black Pill) */
[data-testid="stChatInput"] {
    background-color: transparent !important;
}
[data-testid="stChatInput"] > div {
    background-color: #222222 !important; /* Black pill */
    border-radius: 50px !important;
    border: none !important;
    padding: 5px 15px !important;
}
[data-testid="stChatInput"] textarea {
    color: #FFFFFF !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #888888 !important;
}
/* Turn the send/paperclip icons Lilac */
[data-testid="stChatInput"] button {
    color: #DDA0DD !important; 
}
[data-testid="stChatInput"] svg {
    fill: #DDA0DD !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Inject the custom Canva title
st.markdown('<h1 class="canva-title">RE-MINE</h1>', unsafe_allow_html=True)

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
