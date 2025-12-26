import streamlit as st
import random

st.set_page_config(page_title="Almost Impossible Chess Puzzle", layout="centered")

# --- CSS ---
st.markdown("""
<style>
.sq-dark { background-color:#769656; }
.sq-light { background-color:#eeeed2; }
.sq-blue { background-color:#3498db; }
.sq-gold { background-color:#f1c40f; }
.square-btn button {
    width:45px !important;
    height:45px !important;
    padding:0 !important;
    margin:0 !important;
    font-weight:bold;
}
.intro-box {
    border-left: 5px solid #769656;
    padding: 20px;
    background-color: #f3f3f3;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- INIT ---
def init_game():
    st.session_state.board = [random.randint(0,1) for _ in range(64)]
    st.session_state.key = random.randint(0,63)
    st.session_state.phase = "P1"
    st.session_state.p1_flip = None
    st.session_state.p2_guess = None

if "phase" not in st.session_state:
    st.session_state.phase = "INTRO"

# --- INTRO ---
if st.session_state.phase == "INTRO":
    st.markdown("""
    <div class="intro-box">
    <h1>The Almost Impossible Chess Board Puzzle</h1>
    <p><b>Player 1</b> sees the key and flips one square.</p>
    <p><b>Player 2</b> must find the key using only the final board.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Game"):
        init_game()
        st.session_state.phase = "P1"
    st.stop()

# --- HEADERS ---
if st.session_state.phase == "P1":
    st.header("Player 1's Turn")
    st.write(f"Key is hidden at square: **{st.session_state.key + 1}**")
elif st.session_state.phase == "P2":
    st.header("Player 2's Turn")
elif st.session_state.phase == "RESULT":
    st.header("Result")

# --- BOARD ---
def draw_board(reveal=False):
    for r in range(8):
        cols = st.columns(8)
        for c in range(8):
            i = r*8 + c
            val = "H" if st.session_state.board[i] else "T"

            cls = "sq-dark" if (r+c)%2 else "sq-light"
            if st.session_state.phase == "P1" and i == st.session_state.p1_flip:
                cls = "sq-blue"
            if st.session_state.phase == "P2" and i == st.session_state.p2_guess:
                cls = "sq-blue"
            if reveal and i == st.session_state.key:
                cls = "sq-gold"

            with cols[c]:
                if st.button(val, key=f"s{i}"):
                    if st.session_state.phase == "P1":
                        st.session_state.p1_flip = i
                    elif st.session_state.phase == "P2":
                        st.session_state.p2_guess = i

draw_board(reveal=st.session_state.phase=="RESULT")

# --- ACTION BUTTON ---
if st.session_state.phase == "P1":
    if st.button("Confirm Flip & Call Player 2"):
        if st.session_state.p1_flip is not None:
            i = st.session_state.p1_flip
            st.session_state.board[i] = 1 - st.session_state.board[i]
            st.session_state.phase = "P2"

elif st.session_state.phase == "P2":
    if st.button("Confirm Guess"):
        if st.session_state.p2_guess is not None:
            st.session_state.phase = "RESULT"

elif st.session_state.phase == "RESULT":
    if st.session_state.p2_guess == st.session_state.key:
        st.success("Victory! Player 2 found the key.")
    else:
        st.error(f"Wrong square. Actual was {st.session_state.key + 1}.")
    if st.button("Restart"):
        st.session_state.phase = "INTRO"
