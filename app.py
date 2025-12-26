import streamlit as st
import random

# --- 1. PAGE CONFIGURATION & CSS ---
st.set_page_config(page_title="Impossible Chessboard", layout="centered")

# Custom CSS to mimic the tight grid and specific styling of your original notebook
st.markdown("""
<style>
    /* Center the main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 700px;
    }
    
    /* Styling for the Intro Box */
    .intro-box {
        border-left: 5px solid #769656;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin-bottom: 20px;
        color: black;
    }
    
    /* Tweaking buttons to look more like tiles */
    div.stButton > button {
        width: 100%;
        border-radius: 0px;
        height: 50px;
        font-weight: bold;
        border: 1px solid #ccc;
    }
    
    /* Helper classes for text colors */
    .victory-text { color: green; font-weight: bold; font-size: 24px; }
    .failure-text { color: red; font-weight: bold; font-size: 24px; }
</style>
""", unsafe_allow_html=True)

# --- 2. INITIALIZATION & STATE MANAGEMENT ---
if 'board_state' not in st.session_state:
    st.session_state.board_state = [0] * 64
if 'key_location' not in st.session_state:
    st.session_state.key_location = 0
if 'game_phase' not in st.session_state:
    st.session_state.game_phase = "INTRO"  # Phases: INTRO, PLAYER1, PLAYER2, RESULT
if 'p1_selected_flip' not in st.session_state:
    st.session_state.p1_selected_flip = None
if 'p2_guess' not in st.session_state:
    st.session_state.p2_guess = None

def init_game():
    st.session_state.board_state = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key_location = random.randint(0, 63)
    st.session_state.p1_selected_flip = None
    st.session_state.p2_guess = None
    st.session_state.game_phase = "PLAYER1"

def toggle_coin(index):
    # Logic for Player 1 Selection
    if st.session_state.game_phase == "PLAYER1":
        # If clicking the same one, deselect it, otherwise select new
        if st.session_state.p1_selected_flip == index:
            st.session_state.p1_selected_flip = None
        else:
            st.session_state.p1_selected_flip = index

    # Logic for Player 2 Guess
    elif st.session_state.game_phase == "PLAYER2":
        if st.session_state.p2_guess == index:
            st.session_state.p2_guess = None
        else:
            st.session_state.p2_guess = index

def confirm_action():
    if st.session_state.game_phase == "PLAYER1":
        if st.session_state.p1_selected_flip is not None:
            # Apply the flip
            idx = st.session_state.p1_selected_flip
            st.session_state.board_state[idx] = 1 - st.session_state.board_state[idx]
            st.session_state.game_phase = "PLAYER2"
    
    elif st.session_state.game_phase == "PLAYER2":
        if st.session_state.p2_guess is not None:
            st.session_state.game_phase = "RESULT"

# --- 3. UI RENDERING ---

# >>> PHASE: INTRO <<<
if st.session_state.game_phase == "INTRO":
    st.markdown("""
    <div class="intro-box">
        <h1>The Almost Impossible Chess Board Puzzle</h1>
        <p><b>The Scenario:</b> Two prisoners can win their freedom if they can locate a hidden key.</p>
        <p><b>1. Player 1:</b> Enters the room, sees coins and the key location. They <u>must</u> flip exactly one coin.</p>
        <p><b>2. Player 2:</b> Enters later. Using only the board state, they must find the secret square.</p>
        <p><i>Freedom depends on the single flip!</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start Game", type="primary", use_container_width=True):
        init_game()
        st.rerun()

# >>> PHASE: GAMEPLAY (P1, P2, RESULT) <<<
else:
    # -- HEADER INFO --
    if st.session_state.game_phase == "PLAYER1":
        st.subheader("Player 1's Turn")
        st.info(f"The key is hidden at: **Square {st.session_state.key_location + 1}**")
        st.write("Choose one square to flip (it will turn red), then confirm to call Player 2.")
    
    elif st.session_state.game_phase == "PLAYER2":
        st.subheader("Player 2's Turn")
        st.info("The key's location is secret. Identify the correct square and confirm your guess.")
    
    elif st.session_state.game_phase == "RESULT":
        is_win = st.session_state.p2_guess == st.session_state.key_location
        if is_win:
            st.markdown(f'<p class="victory-text">Victory! Found the key at Square {st.session_state.key_location + 1}.</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="failure-text">Game Over. You guessed {st.session_state.p2_guess + 1}, but Key was at {st.session_state.key_location + 1}.</p>', unsafe_allow_html=True)

    # -- THE CHESS BOARD --
    # We use columns to create the grid. 
    # To reduce code density, we iterate 0-63 and break into rows of 8.
    
    # Visual cues constants
    KEY_LOC = st.session_state.key_location
    P1_SEL = st.session_state.p1_selected_flip
    P2_GUESS = st.session_state.p2_guess
    PHASE = st.session_state.game_phase
    BOARD = st.session_state.board_state

    # Loop to render 8 rows
    for r in range(8):
        cols = st.columns(8, gap="small") # gap="small" mimics the tight board
        for c in range(8):
            i = r * 8 + c
            
            # Determine Label (Heads/Tails)
            label = "H" if BOARD[i] == 1 else "T"
            
            # Determine Color/Style
            # Default is secondary (grey/white). We use 'primary' (red/theme) for selection.
            btn_type = "secondary"
            
            # Logic for highlighting buttons
            if PHASE == "PLAYER1" and i == P1_SEL:
                btn_type = "primary" # Highlight selection
            elif PHASE == "PLAYER2" and i == P2_GUESS:
                btn_type = "primary" # Highlight guess
            elif PHASE == "RESULT" and i == KEY_LOC:
                label += " 🔑" # Show key in result
                btn_type = "primary" # Highlight key location
            
            # Create the button
            if cols[c].button(label, key=f"btn_{i}", type=btn_type):
                toggle_coin(i)
                st.rerun()

    st.markdown("---")

    # -- ACTION BUTTONS --
    if st.session_state.game_phase != "RESULT":
        # Disable confirm if no selection made
        disable_confirm = True
        if st.session_state.game_phase == "PLAYER1" and st.session_state.p1_selected_flip is not None:
            disable_confirm = False
        if st.session_state.game_phase == "PLAYER2" and st.session_state.p2_guess is not None:
            disable_confirm = False
            
        if st.button("Confirm Action", type="primary", disabled=disable_confirm, use_container_width=True):
            confirm_action()
            st.rerun()

    if st.button("Restart / New Game", type="secondary", use_container_width=True):
        init_game()
        st.rerun()
