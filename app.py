import streamlit as st
import random

# --- CONFIG & STYLING ---
st.set_page_config(page_title="The Impossible Chessboard", layout="centered")

st.markdown("""
    <style>
    /* Force the board to look like a solid unit */
    [data-testid="stHorizontalBlock"] { gap: 0px !important; margin: 0px !important; padding: 0px !important; }
    div.stButton > button {
        width: 100% !important; aspect-ratio: 1 / 1 !important;
        border: none !important; border-radius: 0px !important;
        margin: 0px !important; padding: 0px !important;
        font-size: 1.2rem !important; font-weight: bold !important;
    }
    /* Real Chessboard Colors */
    .light-sq button { background-color: #eeeed2 !important; color: #769656 !important; }
    .dark-sq button { background-color: #769656 !important; color: #eeeed2 !important; }
    
    /* Selection States */
    .selected button { background-color: #3498db !important; color: white !important; box-shadow: inset 0 0 10px rgba(0,0,0,0.5) !important; }
    .key-sq button { background-color: #f1c40f !important; color: black !important; animation: pulse 1.5s infinite; }
    
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.6; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'board' not in st.session_state:
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.p1_flip = None
    st.session_state.p2_guess = None
    st.session_state.phase = "PLAYER1"

def restart():
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.p1_flip = None
    st.session_state.p2_guess = None
    st.session_state.phase = "PLAYER1"

# --- GAMEPLAY UI ---
if st.session_state.phase == "PLAYER1":
    st.title("♟️ Player 1: The Messenger")
    st.info(f"The hidden key is at **Square {st.session_state.key}**. Select one coin to flip.")
    if st.button("Confirm Flip & Hand to Player 2", type="primary", use_container_width=True):
        if st.session_state.p1_flip is not None:
            st.session_state.board[st.session_state.p1_flip] = 1 - st.session_state.board[st.session_state.p1_flip]
            st.session_state.phase = "PLAYER2"
            st.rerun()

elif st.session_state.phase == "PLAYER2":
    st.title("🕵️ Player 2: The Decoder")
    st.warning("Player 1 has flipped a coin. Can you find the hidden key?")
    if st.button("Submit Guess", type="primary", use_container_width=True):
        if st.session_state.p2_guess is not None:
            st.session_state.phase = "RESULT"
            st.rerun()

elif st.session_state.phase == "RESULT":
    if st.session_state.p2_guess == st.session_state.key:
        st.success(f"VICTORY! You found the key at Square {st.session_state.key}!")
    else:
        st.error(f"FAILURE! The key was at Square {st.session_state.key}.")
    if st.button("Restart Game", use_container_width=True): restart()

# --- THE CHESSBOARD GRID ---
# Using 8 columns for the 8x8 grid
board_container = st.container()
with board_container:
    for r in range(8):
        cols = st.columns(8)
        for c in range(8):
            idx = r * 8 + c
            coin_val = "●" if st.session_state.board[idx] == 1 else "○"
            
            # Logic for Square Coloring
            is_dark = (r + c) % 2 == 1
            sq_class = "dark-sq" if is_dark else "light-sq"
            
            if (st.session_state.phase == "PLAYER1" and idx == st.session_state.p1_flip) or \
               (st.session_state.phase == "PLAYER2" and idx == st.session_state.p2_guess):
                sq_class = "selected"
            
            if st.session_state.phase == "RESULT" and idx == st.session_state.key:
                sq_class = "key-sq"

            with cols[c]:
                st.markdown(f'<div class="{sq_class}">', unsafe_allow_html=True)
                if st.button(f"{coin_val}", key=f"btn_{idx}"):
                    if st.session_state.phase == "PLAYER1": st.session_state.p1_flip = idx
                    elif st.session_state.phase == "PLAYER2": st.session_state.p2_guess = idx
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
