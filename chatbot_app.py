import streamlit as st
import difflib

# ---- Load dialog pairs ----
def load_dialogs(file_path):
    dialog_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' in line:
                q, a = line.strip().split('\t')
                dialog_dict[q.lower()] = a
    return dialog_dict

# ---- Get response using fuzzy match ----
def get_response(user_input, dialog_dict):
    user_input = user_input.lower().strip()
    matches = difflib.get_close_matches(user_input, dialog_dict.keys(), n=1, cutoff=0.6)
    if matches:
        return dialog_dict[matches[0]]
    else:
        return "🤖 Sorry, I didn’t understand that. Could you rephrase it?"

# ---- Load dialogs ----
dialog_dict = load_dialogs("dialogs.txt")

# ---- Streamlit Chat UI ----
st.set_page_config(page_title="Chatbot", layout="centered")
st.markdown("<h2 style='text-align: center;'>💬 Customer Support Chatbot</h2>", unsafe_allow_html=True)

# ---- Store conversation history ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- Input field ----
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Type your message here...")
    submitted = st.form_submit_button("Send")

# ---- Process input ----
if submitted and user_input:
    response = get_response(user_input, dialog_dict)
    st.session_state.chat_history.append(("🧑‍💻 You", user_input))
    st.session_state.chat_history.append(("🤖 Bot", response))

# ---- Display chat history like bubbles ----
for sender, message in st.session_state.chat_history:
    if sender == "🧑‍💻 You":
        st.markdown(
            f"""
            <div style='text-align: right; color:black; background-color: #00ced1; padding: 8px; border-radius: 10px; margin: 5px 0;'>
                <b>{sender}:</b> {message}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            f"""
            <div style='text-align: left; color: black; background-color: #ff69b4; padding: 8px; border-radius: 10px; margin: 5px 0;'>
                <b>{sender}:</b> {message}
            </div>
            """, unsafe_allow_html=True)
