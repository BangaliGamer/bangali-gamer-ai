import streamlit as st
from agent import BangaliGamerAgent
from knowledge import save_knowledge

# ওয়েবসাইটের নাম এবং আইকন সেট করা
st.set_page_config(page_title="Bangali Gamer AI", page_icon="🎮")

st.title("🎮 Bangali Gamer AI Agent")

# সাইডবারে (বাম পাশে) Admin বা Customer মোড সিলেক্ট করার অপশন
mode = st.sidebar.radio("লগইন মোড সিলেক্ট করুন:", ("Customer Mode", "Admin Mode"))
is_admin = (mode == "Admin Mode")

# সেশন ক্লিয়ার এবং এজেন্ট লোড করা
if "agent" not in st.session_state or st.session_state.mode != mode:
    st.session_state.agent = BangaliGamerAgent(is_admin=is_admin)
    st.session_state.mode = mode
    st.session_state.messages = [] # মোড চেঞ্জ করলে আগের চ্যাট মুছে যাবে

# আগের মেসেজগুলো স্ক্রিনে দেখানো
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# নতুন চ্যাট ইনপুট বক্স
if prompt := st.chat_input("আপনার মেসেজ এখানে লিখুন..."):
    # ইউজারের মেসেজ স্ক্রিনে দেখানো
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # এআই-এর উত্তর জেনারেট করা
    with st.chat_message("assistant"):
        response_text = st.session_state.agent.get_response(prompt)
        
        # অ্যাডমিন মোডে ডেটা সেভ করার লজিক
        if is_admin and "[SAVE_KNOWLEDGE:" in response_text:
            start_idx = response_text.find("[SAVE_KNOWLEDGE:") + 16
            end_idx = response_text.find("]", start_idx)
            if end_idx != -1:
                new_fact = response_text[start_idx:end_idx].strip()
                save_knowledge(new_fact)
                
                # সিস্টেমের নোটিফিকেশন সুন্দর করে দেখানো
                response_text = response_text[:response_text.find("[SAVE_KNOWLEDGE:")].strip()
                response_text += f"\n\n✅ **[System: '{new_fact}' successfully saved to Knowledge Base!]**"
        
        # এআই-এর ফাইনাল মেসেজ স্ক্রিনে দেখানো
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
