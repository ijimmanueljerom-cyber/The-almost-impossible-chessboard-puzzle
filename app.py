import streamlit as st
import random

# --- 1. GLOBAL SETTINGS & CSS ---
st.set_page_config(page_title="Impossible Chessboard", layout="centered")

# This CSS forces the grid to stay 8x8 regardless of screen size
st.markdown("""
<style>
    .chess-grid {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 4px;
        max-width: 400px;
        margin: auto;
    }
    .stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0 !important;
        font-weight: bold !important;
        border-radius: 0px !important;
    }
    .status-box {
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. STATE MANAGEMENT ---
if 'board' not in st.session_state:
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.phase = "INTRO"
    st.session_state.selection = None

def reset():
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.selection = None
    st.session_state.phase = "PLAYER1"

# --- 3. UI RENDERING ---
st.title("♟️ The Impossible Puzzle")

if st.session_state.phase == "INTRO":
    st.info("Two prisoners. 64 coins. One flip. Can Player 2 find the key?")
    if st.button("Start Game", use_container_width=True, type="primary"):
        reset()
        st.rerun()

else:
    # Status Updates
    if st.session_state.phase == "PLAYER1":
        st.success(f"PLAYER 1: Key is at **Square {st.session_state.key + 1}**")
        st.write("Select one coin to flip, then confirm.")
    elif st.session_state.phase == "PLAYER2":
        st.warning("PLAYER 2: Look at the board. Where is the key?")
    elif st.session_state.phase == "RESULT":
        if st.session_state.selection == st.session_state.key:
            st.balloons()
            st.success("VICTORY! Player 2 found the key!")
        else:
            st.error(f"GAME OVER. Key was at {st.session_state.key + 1}")

    # --- THE BOARD ---
    # We use a container and manual columns to simulate the grid
    # This is the most stable way to do it in Streamlit
    container = st.container()
    for r in range(8):
        cols = st.columns(8)
        for c in range(8):
            idx = r * 8 + c
            label = "H" if st.session_state.board[idx] == 1 else "T"
            
            # Color logic
            b_type = "secondary"
            if st.session_state.phase == "RESULT" and idx == st.session_state.key:
                label = "🔑"
                b_type = "primary"
            elif idx == st.session_state.selection:
                b_type = "primary"

            if cols[c].button(label, key=f"btn_{idx}", type=b_type):
                st.session_state.selection = idx
                st.rerun()

    # --- ACTION BUTTONS ---
    st.divider()
    if st.session_state.phase == "PLAYER1":
        if st.button("Confirm Flip & Call Player 2", use_container_width=True, disabled=st.session_state.selection is None):
            # Flip logic
            s = st.session_state.selection
            st.session_state.board[s] = 1 - st.session_state.board[s]
            st.session_state.selection = None
            st.session_state.phase = "PLAYER2"
            st.rerun()
    
    elif st.session_state.phase == "PLAYER2":
        if st.button("Confirm Guess", use_container_width=True, disabled=st.session_state.selection is None):
            st.session_state.phase = "RESULT"
            st.rerun()

    if st.button("Restart", use_container_width=True):
        reset()
        st.rerun()
