import streamlit as st
import random

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Impossible Chessboard", layout="centered")

# --- 2. LOGIC & STATE ---
if 'board' not in st.session_state:
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.phase = "PLAYER1" # PLAYER1, PLAYER2, RESULT
    st.session_state.selected = None

def restart():
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.phase = "PLAYER1"
    st.session_state.selected = None

# --- 3. THE CSS (FORCING THE GRID) ---
st.markdown("""
<style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 2px;
        background-color: #444;
        padding: 5px;
        border-radius: 4px;
        width: 100%;
        max-width: 400px;
        margin: auto;
    }
    .tile {
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        cursor: pointer;
        border: none;
        color: black;
    }
    /* Square Colors */
    .dark { background-color: #769656; }
    .light { background-color: #eeeed2; }
    .selected { background-color: #3498db !important; color: white; }
    .key-gold { background-color: #f1c40f !important; }
</style>
""", unsafe_allow_html=True)

# --- 4. GAME HEADER ---
st.title("The Impossible Chessboard")

if st.session_state.phase == "PLAYER1":
    st.info(f"**Player 1:** The key is at **Square {st.session_state.key + 1}**. Choose 1 coin to flip.")
elif st.session_state.phase == "PLAYER2":
    st.warning("**Player 2:** Look at the board. Find the key!")
else:
    if st.session_state.selected == st.session_state.key:
        st.success("✨ VICTORY! Player 2 found the key!")
    else:
        st.error(f"❌ FAILED! Key was at {st.session_state.key + 1}")

# --- 5. THE INTERACTIVE GRID ---
# We use st.columns as a fallback that we style heavily
with st.container():
    for r in range(8):
        cols = st.columns(8)
        for c in range(8):
            i = r * 8 + c
            
            # Logic for visuals
            label = "H" if st.session_state.board[i] == 1 else "T"
            
            # Determine button type
            is_key = (st.session_state.phase == "RESULT" and i == st.session_state.key)
            is_selected = (i == st.session_state.selected)
            
            btn_type = "primary" if (is_selected or is_key) else "secondary"
            
            if is_key: label = "🔑"

            if cols[c].button(label, key=f"sq_{i}", type=btn_type, use_container_width=True):
                st.session_state.selected = i
                st.rerun()

# --- 6. ACTION AREA ---
st.markdown("---")
if st.session_state.phase == "PLAYER1":
    if st.button("Confirm Flip & Call Player 2", use_container_width=True, type="primary", disabled=st.session_state.selected is None):
        idx = st.session_state.selected
        st.session_state.board[idx] = 1 - st.session_state.board[idx]
        st.session_state.selected = None
        st.session_state.phase = "PLAYER2"
        st.rerun()

elif st.session_state.phase == "PLAYER2":
    if st.button("Identify Key Location", use_container_width=True, type="primary", disabled=st.session_state.selected is None):
        st.session_state.phase = "RESULT"
        st.rerun()

if st.button("Start New Game", use_container_width=True):
    restart()
    st.rerun()
