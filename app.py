import streamlit as st
import random

# --- 1. PAGE CONFIGURATION & CSS ---
st.set_page_config(page_title="Impossible Chessboard", layout="centered")

# CSS to force a tight, square grid
st.markdown("""
<style>
    /* 1. Force buttons to be square and remove standard gaps */
    div.stButton > button {
        width: 100%;
        aspect-ratio: 1 / 1;  /* This makes them perfect squares */
        border-radius: 0px;   /* Sharp corners like chess tiles */
        border: 1px solid #333;
        padding: 0px;
        font-weight: bold;
        font-size: 20px;
    }
    
    /* 2. Tighten the columns (reduce the white space between squares) */
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        min-width: 0px !important;
    }
    
    /* 3. Center the whole board */
    .block-container {
        max-width: 600px;
    }
    
    .intro-box {
        border-left: 5px solid #769656;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin-bottom: 20px;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZATION & STATE ---
if 'board_state' not in st.session_state:
    st.session_state.board_state = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key_location = random.randint(0, 63)
    st.session_state.game_phase = "INTRO"
    st.session_state.p1_selected_flip = None
    st.session_state.p2_guess = None

def init_game():
    st.session_state.board_state = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key_location = random.randint(0, 63)
    st.session_state.p1_selected_flip = None
    st.session_state.p2_guess = None
    st.session_state.game_phase = "PLAYER1"

def toggle_coin(index):
    if st.session_state.game_phase == "PLAYER1":
        if st.session_state.p1_selected_flip == index:
            st.session_state.p1_selected_flip = None
        else:
            st.session_state.p1_selected_flip = index
    elif st.session_state.game_phase == "PLAYER2":
        if st.session_state.p2_guess == index:
            st.session_state.p2_guess = None
        else:
            st.session_state.p2_guess = index

def confirm_action():
    if st.session_state.game_phase == "PLAYER1":
        idx = st.session_state.p1_selected_flip
        st.session_state.board_state[idx] = 1 - st.session_state.board_state[idx]
        st.session_state.game_phase = "PLAYER2"
    elif st.session_state.game_phase == "PLAYER2":
        st.session_state.game_phase = "RESULT"

# --- 3. UI RENDERING ---
st.title("Impossible Chessboard")

if st.session_state.game_phase == "INTRO":
    st.markdown("""
    <div class="intro-box">
        <h3>The Rules</h3>
        <p><b>Player 1:</b> Sees the key. Flips exactly ONE coin.</p>
        <p><b>Player 2:</b> Sees only the coins. Finds the key.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Game", type="primary", use_container_width=True):
        init_game()
        st.rerun()

else:
    # Status Header
    if st.session_state.game_phase == "PLAYER1":
        st.info(f"🔑 Key is at **Square {st.session_state.key_location + 1}**. Flip one coin.")
    elif st.session_state.game_phase == "PLAYER2":
        st.warning("🤔 Player 2: Where is the key? Select a square.")
    elif st.session_state.game_phase == "RESULT":
        if st.session_state.p2_guess == st.session_state.key_location:
            st.success(f"🎉 VICTORY! Found at Square {st.session_state.key_location + 1}")
        else:
            st.error(f"💀 FAILED. Guess: {st.session_state.p2_guess + 1} | Actual: {st.session_state.key_location + 1}")

    # --- THE CHESSBOARD GRID ---
    # This loop MUST correspond to the 8x8 structure
    
    board = st.session_state.board_state
    
    # Iterate through 8 rows
    for r in range(8):
        # Create 8 columns for this specific row
        cols = st.columns(8) 
        
        # Iterate through 8 items in this row
        for c in range(8):
            i = r * 8 + c
            
            # Button Logic (Label and Color)
            label = "H" if board[i] == 1 else "T"
            btn_type = "secondary"
            
            # Coloring Logic
            if st.session_state.game_phase == "PLAYER1" and i == st.session_state.p1_selected_flip:
                btn_type = "primary"
            elif st.session_state.game_phase == "PLAYER2" and i == st.session_state.p2_guess:
                btn_type = "primary"
            elif st.session_state.game_phase == "RESULT" and i == st.session_state.key_location:
                btn_type = "primary"
                label = "🔑"

            # PLACING THE BUTTON INSIDE THE COLUMN
            # "cols[c]" puts the button in the correct horizontal slot
            if cols[c].button(label, key=f"btn_{i}", type=btn_type):
                toggle_coin(i)
                st.rerun()

    st.write("") # Spacer
    
    # Action Buttons
    if st.session_state.game_phase != "RESULT":
        disable_confirm = True
        if st.session_state.game_phase == "PLAYER1" and st.session_state.p1_selected_flip is not None:
            disable_confirm = False
        if st.session_state.game_phase == "PLAYER2" and st.session_state.p2_guess is not None:
            disable_confirm = False
            
        if st.button("Confirm Selection", type="primary", disabled=disable_confirm, use_container_width=True):
            confirm_action()
            st.rerun()

    if st.button("Restart Game", use_container_width=True):
        init_game()
        st.rerun()
