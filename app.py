import streamlit as st
import random

# --- CHESSBOARD ENGINE (The logic remains the same, the UI changes) ---
if 'board' not in st.session_state:
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.p1_flip = None
    st.session_state.p2_guess = None
    st.session_state.phase = "PLAYER1"

def handle_click(idx):
    if st.session_state.phase == "PLAYER1":
        st.session_state.p1_flip = idx
    elif st.session_state.phase == "PLAYER2":
        st.session_state.p2_guess = idx

# --- ADVANCED CSS FOR A REAL BOARD ---
st.markdown("""
<style>
    /* 1. Create the square grid container */
    .chess-board {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        width: 100%;
        max-width: 500px;
        margin: 0 auto;
        aspect-ratio: 1 / 1;
        border: 4px solid #3d3d3d;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* 2. Style the individual squares */
    .square {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        cursor: pointer;
        user-select: none;
        transition: transform 0.1s;
    }
    .square:active { transform: scale(0.95); }

    /* 3. Authentic Colors */
    .light { background-color: #eeeed2; color: #769656; }
    .dark { background-color: #769656; color: #eeeed2; }
    
    /* 4. State Overlays */
    .selected { outline: 4px solid #3498db !important; outline-offset: -4px; z-index: 2; }
    .is-key { background-color: #f1c40f !important; color: black !important; }
    
    /* Hide default Streamlit button styling for these specific buttons */
    div.stButton > button {
        background: transparent !important;
        border: none !important;
        width: 100% !important;
        height: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

# --- UI CONTROL PANEL ---
if st.session_state.phase == "PLAYER1":
    st.title("♟️ Player 1: Flip One Coin")
    st.write(f"The Secret Key is at Square **{st.session_state.key}**")
    if st.button("Finish Flip", type="primary", use_container_width=True):
        if st.session_state.p1_flip is not None:
            st.session_state.board[st.session_state.p1_flip] = 1 - st.session_state.board[st.session_state.p1_flip]
            st.session_state.phase = "PLAYER2"
            st.rerun()

elif st.session_state.phase == "PLAYER2":
    st.title("🕵️ Player 2: Guess the Key")
    if st.button("Confirm Guess", type="primary", use_container_width=True):
        if st.session_state.p2_guess is not None:
            st.session_state.phase = "RESULT"
            st.rerun()

elif st.session_state.phase == "RESULT":
    if st.session_state.p2_guess == st.session_state.key:
        st.success("Correct! You found the key.")
    else:
        st.error(f"Failed! The key was at Square {st.session_state.key}")
    if st.button("Restart"): 
        del st.session_state.board
        st.rerun()

# --- THE RENDERED BOARD ---
# We wrap buttons in a CSS Grid container
st.markdown('<div class="chess-board">', unsafe_allow_html=True)
cols = st.columns(8) # We use this dummy structure to capture events but override layout with CSS
for i in range(64):
    row = i // 8
    col = i % 8
    
    # Determine visual class
    is_dark = (row + col) % 2 == 1
    tile_class = "dark" if is_dark else "light"
    
    if (st.session_state.phase == "PLAYER1" and i == st.session_state.p1_flip) or \
       (st.session_state.phase == "PLAYER2" and i == st.session_state.p2_guess):
        tile_class += " selected"
    
    if st.session_state.phase == "RESULT" and i == st.session_state.key:
        tile_class += " is-key"
    
    coin = "●" if st.session_state.board[i] == 1 else "○"
    
    # Render Square
    with st.container():
        # This custom div structure inside the column ensures the CSS Grid handles the sizing
        st.markdown(f'<div class="square {tile_class}" id="sq-{i}">', unsafe_allow_html=True)
        if st.button(coin, key=f"btn-{i}"):
            handle_click(i)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
