import streamlit as st
import random

# --- 1. CONFIG & REPAIRING CSS ---
st.set_page_config(page_title="The Almost Impossible Chess Board", layout="centered")

# CSS to fix gaps, force squares, and prevent text overflow
st.markdown("""
<style>
    /* GAPLESS GRID SYSTEM */
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
    
    /* SQUARE BUTTONS & TEXT OVERFLOW FIX */
    div.stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 2px !important;
        font-weight: bold !important;
        font-size: clamp(10px, 2vw, 16px) !important;
        border: 0.1px solid rgba(0,0,0,0.1) !important;
        overflow: hidden !important; /* Prevents text overflow */
        white-space: nowrap !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* FIXING OVERFLOW FOR ACTION BUTTONS */
    div.stButton > button[p-id="action-btn"] {
        aspect-ratio: auto !important;
        height: 50px !important;
        width: 100% !important;
        border-radius: 8px !important;
        white-space: normal !important; /* Allow wrapping for long labels */
        padding: 10px !important;
    }

    /* AUTHENTIC CHESS COLORS (Matching your Colab Shadows) */
    .sq-dark button { background-color: #769656 !important; color: white !important; }
    .sq-light button { background-color: #eeeed2 !important; color: black !important; }
    .sq-blue button { background-color: #3498db !important; color: white !important; box-shadow: inset 0 0 10px #000 !important; }
    .sq-gold button { background-color: #f1c40f !important; color: black !important; border: 2px solid orange !important; }

    /* LABEL STYLING */
    .label { font-weight: bold; text-align: center; color: #333; }
</style>
""", unsafe_allow_html=True)

# --- 2. GAME LOGIC & STATE ---
if 'board' not in st.session_state:
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.phase = "PLAYER1"
    st.session_state.selection = None

def reset_game():
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.phase = "PLAYER1"
    st.session_state.selection = None

# --- 3. UI LAYOUT ---
if st.session_state.phase == "PLAYER1":
    st.title("Prisoner 1: The Flip")
    st.write(f"The hidden key is at **Square {st.session_state.key + 1}**")
    if st.button("Confirm Flip & Call Player 2", key="confirm_p1", help="Select a square first"):
        if st.session_state.selection is not None:
            idx = st.session_state.selection
            st.session_state.board[idx] = 1 - st.session_state.board[idx]
            st.session_state.phase = "PLAYER2"
            st.session_state.selection = None
            st.rerun()

elif st.session_state.phase == "PLAYER2":
    st.title("Prisoner 2: The Guess")
    if st.button("Confirm Guess", key="confirm_p2"):
        if st.session_state.selection is not None:
            st.session_state.phase = "RESULT"
            st.rerun()

elif st.session_state.phase == "RESULT":
    if st.session_state.selection == st.session_state.key:
        st.success(f"VICTORY! You found the key at Square {st.session_state.key + 1}!")
    else:
        st.error(f"FAILURE! Key was at {st.session_state.key + 1}, you guessed {st.session_state.selection + 1}")
    if st.button("Restart Game"):
        reset_game()
        st.rerun()

# --- 4. THE CHESSBOARD GRID ---
# Create 8 columns with a small leading column for row numbers
grid_cols = st.columns([0.5] + [1] * 8)

# Header Row (Column numbers)
for i in range(8):
    grid_cols[i+1].markdown(f"<p class='label'>{i+1}</p>", unsafe_allow_html=True)

# 8x8 Grid
for r in range(8):
    row_cols = st.columns([0.5] + [1] * 8)
    row_cols[0].markdown(f"<p class='label' style='line-height:45px;'>{r*8+1}</p>", unsafe_allow_html=True)
    
    for c in range(8):
        idx = r * 8 + c
        coin = "H" if st.session_state.board[idx] == 1 else "T"
        
        # Determine CSS Class for current tile
        is_dark = (r + c) % 2 == 1
        tile_style = "sq-dark" if is_dark else "sq-light"
        
        if st.session_state.selection == idx:
            tile_style = "sq-blue"
        if st.session_state.phase == "RESULT" and idx == st.session_state.key:
            tile_style = "sq-gold"

        with row_cols[c+1]:
            st.markdown(f'<div class="{tile_style}">', unsafe_allow_html=True)
            if st.button(coin, key=f"btn_{idx}"):
                st.session_state.selection = idx
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
