import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 1. API CONFIGURATION (SECURE MODE)
# ==========================================
# The app now securely pulls the key from Streamlit's hidden vault!
CHAVE_API = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=CHAVE_API)

# Initialize the model
model = genai.GenerativeModel('models/gemini-2.5-flash')

# ==========================================
# 2. UI & STATE SETUP
# ==========================================
st.set_page_config(page_title="RE-MINE: Urban Mining", page_icon="💎", layout="centered")

st.title("💎 RE-MINE: Trash to Treasure")
st.write("Scan old electronics, discover their hidden value, and learn where to sell them.")

# Initialize a native Gemini Chat Session to remember context
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Initialize UI message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages in the UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# 3. CAMERA & INITIAL ANALYSIS
# ==========================================
foto = st.camera_input("📸 Take a photo of the electronic component")

if foto:
    img = Image.open(foto)
    st.image(img, caption="Analyzing for precious metals...", use_container_width=True)
    
    # The Global & Monetization Prompt
    prompt = """
    You are RE-MINE, an expert AI in urban mining and e-waste recycling. 
    Analyze the provided image and give a structured report:
    1. **Identify**: What is this object?
    2. **The Loot**: What precious metals are inside (Gold, Silver, Palladium, Copper, etc.)? Give a rough estimated value in USD.
    3. **The Hustle**: How can the user make money from this? Suggest global options (e.g., selling boards on eBay, local scrap yards, specialized e-waste refiners).
    4. **The Tear-Down**: Brief, safe instructions on how to extract the valuable parts.
    ⚠️ ALWAYS include a bold warning if you suspect lithium batteries or hazardous capacitors.
    Keep the tone encouraging, expert, and conversational.
    """
    
    try:
        with st.chat_message("assistant"):
            with st.spinner("Extracting data..."):
                # Send image and prompt to the chat session (so it remembers the image)
                response = st.session_state.chat_session.send_message([prompt, img])
                st.markdown(response.text)
                
                # Save to UI history
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Analysis Error: {e}")

# ==========================================
# 4. CONVERSATIONAL AI CHAT
# ==========================================
if pergunta := st.chat_input("Ask me anything about selling or dismantling this..."):
    
    # Show user message
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.messages.append({"role": "user", "content": pergunta})
    
    # Get AI response 
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            res = st.session_state.chat_session.send_message(pergunta)
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
