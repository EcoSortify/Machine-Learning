import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Load environment variables
load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_LOCATION")
SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

# Setup credentials
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH)
scoped_credentials = credentials.with_scopes([
    "https://www.googleapis.com/auth/cloud-platform"
])
scoped_credentials.refresh(Request())

# Initialize Google GenAI Client
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    credentials=scoped_credentials
)

# Define model and system instruction
model = "projects/838338694702/locations/us-central1/endpoints/1199379169415266304"
system_instruction = """
Kamu adalah chabot aplikasi EcoSortify bernama "SortiBot" yang mengkhususkan diri dalam menjawab pertanyaan seputar edukasi pengetahuan dan pemilahan sampah. Tujuan kamu adalah memberikan jawaban yang edukatif, jelas, dan mudah dipahami oleh pengguna umum dalam bahasa Indonesia. Jawaban kamu harus berbobot dan komprehensif, tetapi tetap ringkas dan tidak terlalu kaku atau terlalu formal. Gunakan gaya bahasa yang ramah, khas seperti chatbot yang siap membantu pengguna. Gunakan konteks dari pertanyaan yang saya berikan untuk memberikan jawaban terbaik. Jawaban tidak perlu terlalu panjang, tapi harus mengandung informasi yang akurat dan bermanfaat. Jika saya memberikan pertanyaan, cukup jawab langsung sesuai instruksi di atas. Tapi jika diperlukan, berikan tambahan penjelasan lebih lengkap lainnya.

Ketentuan:
- Jangan pernah mencantumkan cite berupa format seperti ini [cite: number] atau [source: number] di akhir jawaban yang kamu berikan.
- Jangan menggunakan bahasa "Gue" atau "Lu".
- Jika ada yang menanyakan kamu itu siapa (memperkenalkan diri), jawab sesuai instruksi yang sudah saya berikan.
"""

# Streamlit UI
st.set_page_config(page_title="EcoSortify Chatbot", page_icon="🧠", layout="centered")
st.title("🤖 EcoSortify Chatbot")

# Inisialisasi session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "contents" not in st.session_state:
    st.session_state.contents = []

# Tampilkan riwayat chat
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

# Input dari user
user_prompt = st.chat_input("Tanyakan sesuatu...")
if user_prompt:
    # Tampilkan pesan user
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append(("user", user_prompt))

    # Tambahkan ke contents
    st.session_state.contents.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_prompt)]
    ))

    # Konfigurasi pemanggilan model
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=1,
        max_output_tokens=8192,
        system_instruction=system_instruction,
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
    )

    # Panggil model dan tampilkan hasil
    response_stream = client.models.generate_content_stream(
        model=model,
        contents=st.session_state.contents,
        config=generate_content_config,
    )

    assistant_reply = ""
    with st.chat_message("assistant"):
        placeholder = st.empty()
        for chunk in response_stream:
            if chunk.text:
                assistant_reply += chunk.text
                placeholder.markdown(assistant_reply)
        placeholder.markdown(assistant_reply)

    # Simpan ke history dan contents
    st.session_state.chat_history.append(("assistant", assistant_reply))
    st.session_state.contents.append(types.Content(
        role="assistant",
        parts=[types.Part.from_text(text=assistant_reply)]
    ))
    print(len(st.session_state.contents))

# Tombol untuk reset chat
# if st.button("🔄 Reset Chat"):
#     st.session_state.chat_history = []
#     st.session_state.contents = []
#     st.experimental_rerun()