import streamlit as st
from akinator.client import Akinator

st.set_page_config(page_title="Akinator Game", page_icon="🧞", layout="centered")
st.title("🧞 Akinator Game")

def init_state():
    if 'aki' not in st.session_state:
        st.session_state.aki = Akinator()
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'guess' not in st.session_state:
        st.session_state.guess = None

init_state()

question_box = st.empty()
choices_box = st.empty()

st.write("Choose a character in your mind and click Start Game.")

# Start game button
if not st.session_state.game_started:
    if st.button("Start Game 🕹️"):
        st.session_state.aki = Akinator()
        st.session_state.aki.start_game(language='en')
        st.session_state.step = 0
        st.session_state.game_started = True
        st.session_state.guess = None

# Game loop
if st.session_state.game_started:
    question = st.session_state.aki.question
    if question:
        st.markdown(f"**Question {st.session_state.step+1}:** {question}")
        cols = st.columns(5)
        answer = None
        with cols[0]:
            if st.button("Yes"):
                answer = 'y'
        with cols[1]:
            if st.button("No"):
                answer = 'n'
        with cols[2]:
            if st.button("I Don't Know"):
                answer = 'idk'
        with cols[3]:
            if st.button("Probably"):
                answer = 'p'
        with cols[4]:
            if st.button("Probably Not"):
                answer = 'pn'

        if answer:
            st.session_state.aki.answer(answer)
            st.session_state.step += 1
            # If ready to guess, trigger choose
            if st.session_state.aki.progression > 80 and st.session_state.aki.win:
                st.session_state.aki.choose()
                st.session_state.game_started = False
            st.rerun()
    else:
        st.markdown("Loading question...")

# Show guess/result
if not st.session_state.game_started and st.session_state.aki.win:
    name = st.session_state.aki.name_proposition
    desc = st.session_state.aki.description_proposition
    img = st.session_state.aki.photo
    st.success(f"I guess: **{name}**\n{desc}")
    if img:
        st.image(img, width=200)
    if st.button("Play Again"):
        for key in ['aki', 'step', 'game_started']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun() 