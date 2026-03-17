import streamlit as st

# -------- SAFE IMPORT --------
try:
    from akinator.client import Akinator
except:
    Akinator = None

st.set_page_config(page_title="Akinator Game", page_icon="🧞", layout="centered")
st.title("🧞 Akinator Game")

# -------- CHECK MODULE --------
if Akinator is None:
    st.error("❌ Akinator module failed to load on server.")
    st.info("This app may not work online due to dependency issues.")
    st.stop()

# ---------------- STATE INIT ----------------
def init_state():
    if 'aki' not in st.session_state:
        st.session_state.aki = None
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'error' not in st.session_state:
        st.session_state.error = False

init_state()

# ---------------- ERROR MODE ----------------
if st.session_state.error:
    st.error("⚠️ Akinator API failed. The game crashed.")

    if st.button("🔄 Restart Game"):
        st.session_state.clear()
        st.rerun()

    st.stop()

# ---------------- START GAME ----------------
if not st.session_state.game_started:
    st.write("Think of a character and click Start Game.")

    if st.button("Start Game 🕹️"):
        try:
            aki = Akinator()
            aki.start_game(language='en')

            st.session_state.aki = aki
            st.session_state.step = 0
            st.session_state.game_started = True

            st.rerun()

        except Exception:
            st.session_state.error = True
            st.rerun()

# ---------------- GAME LOOP ----------------
if st.session_state.game_started and st.session_state.aki:
    aki = st.session_state.aki

    try:
        question = aki.question
    except:
        st.session_state.error = True
        st.rerun()

    if question:
        st.markdown(f"**Question {st.session_state.step + 1}:** {question}")
        st.write(f"Confidence: {aki.progression:.2f}%")

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

        # -------- ANSWER --------
        if answer:
            try:
                with st.spinner("Thinking..."):
                    aki.answer(answer)
                    st.session_state.step += 1

                st.rerun()

            except Exception:
                st.session_state.error = True
                st.rerun()

        # -------- SAFE AUTO GUESS --------
        if getattr(aki, "win", False):
            try:
                aki.choose()
                st.session_state.game_started = False
                st.rerun()
            except Exception:
                st.session_state.error = True
                st.rerun()

    else:
        st.markdown("Loading question...")

# ---------------- RESULT ----------------
if not st.session_state.game_started and st.session_state.aki:
    aki = st.session_state.aki

    if getattr(aki, "win", False):
        st.success(f"I guess: **{aki.name_proposition}**\n\n{aki.description_proposition}")

        if aki.photo:
            st.image(aki.photo, width=200)

        if st.button("Play Again"):
            st.session_state.clear()
            st.rerun()