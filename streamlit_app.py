import streamlit as st
from app.agent import BangaliGamerAgent
from app.knowledge import save_knowledge

st.set_page_config(page_title="Bangali Gamer AI", page_icon="🎮")
st.title("🎮 Bangali Gamer AI Agent")

mode = st.sidebar.radio("লগইন মোড সিলেক্ট করুন:", ("Customer Mode", "Admin Mode"))
is_admin = (mode == "Admin Mode")

if "agent" not in st.session_state or st.session_state.mode != mode:
    st.session_state.agent = BangaliGamerAgent(is_admin=is_admin)
    st.session_state.mode = mode
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("আপনার মেসেজ এখানে লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = st.session_state.agent.get_response(prompt)
        
        if is_admin and "[SAVE_KNOWLEDGE:" in response_text:
            start_idx = response_text.find("[SAVE_KNOWLEDGE:") + 16
            end_idx = response_text.find("]", start_idx)
            if end_idx != -1:
                new_fact = response_text[start_idx:end_idx].strip()
                save_knowledge(new_fact)
                
                response_text = response_text[:response_text.find("[SAVE_KNOWLEDGE:")].strip()
                response_text += f"\n\n✅ **[System: '{new_fact}' successfully saved to Knowledge Base!]**"
        
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
