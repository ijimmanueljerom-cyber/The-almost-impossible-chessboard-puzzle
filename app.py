import streamlit as st
import random

# --- 1. PAGE SETUP & CSS ---
st.set_page_config(page_title="Impossible Chessboard", layout="centered")

st.markdown("""
<style>
    /* Force 8x8 Grid even on small screens */
    div[data-testid="column"] {
        width: 12.5% !important;
        flex: 1 1 calc(12.5% - 5px) !important;
        min-width: 10px !important;
    }

    /* Make buttons square and tight */
    div.stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0px !important;
        margin: 0px !important;
        border-radius: 0px !important;
        font-size: 14px !important;
    }

    /* Intro box styling */
    .intro-box {
        border-left: 5px solid #769656;
        padding: 15px;
        background-color: #f0f2f6;
        color: black;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. STATE INITIALIZATION ---
if 'board_state' not in st.session_state:
    st.session_state.board_state = [0] * 64
    st.session_state.key_location = 0
    st.session_state.game_phase = "INTRO"
    st.session_state.p1_selected_flip = None
    st.session_state.p2_guess = None

def init_game():
    st.session_state.board_state = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key_location = random.randint(0, 63)
    st.session_state.p1_selected_flip = None
    st.session_state.p2_guess = None
    st.session_state.game_phase = "PLAYER1"

# --- 3. UI LOGIC ---
st.title("♟️ Impossible Chessboard")

if st.session_state.game_phase == "INTRO":
    st.markdown("""
    <div class="intro-box">
        <h3>The Rules</h3>
        <p><b>Player 1:</b> Sees the board and the hidden key. You must flip <b>exactly one</b> coin.</p>
        <p><b>Player 2:</b> Enters the room and sees only the coins. You must find the key.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Game", type="primary", use_container_width=True):
        init_game()
        st.rerun()

else:
    # Top Information
    if st.session_state.game_phase == "PLAYER1":
        st.info(f"📍 Key is at Square: **{st.session_state.key_location + 1}**")
        st.write("Click a square to select which coin to flip.")
    elif st.session_state.game_phase == "PLAYER2":
        st.warning("🕵️ Player 2: Find the key! Which square was indicated?")
    elif st.session_state.game_phase == "RESULT":
        if st.session_state.p2_guess == st.session_state.key_location:
            st.success(f"✅ Victory! Found at {st.session_state.key_location + 1}")
        else:
            st.error(f"❌ Failed! Key was at {st.session_state.key_location + 1}")

    # --- THE BOARD ---
    # We use a container to keep everything grouped
    board_container = st.container()
    
    for r in range(8):
        cols = st.columns(8)
        for c in range(8):
            i = r * 8 + c
            
            # Labeling
            label = "H" if st.session_state.board_state[i] == 1 else "T"
            
            # Styling
            btn_type = "secondary"
            if st.session_state.game_phase == "PLAYER1" and i == st.session_state.p1_selected_flip:
                btn_type = "primary"
            elif st.session_state.game_phase == "PLAYER2" and i == st.session_state.p2_guess:
                btn_type = "primary"
            elif st.session_state.game_phase == "RESULT" and i == st.session_state.key_location:
                label = "🔑"
                btn_type = "primary"

            # Button Interaction
            if cols[c].button(label, key=f"sq_{i}", type=btn_type):
                if st.session_state.game_phase == "PLAYER1":
                    st.session_state.p1_selected_flip = i
                    st.rerun()
                elif st.session_state.game_phase == "PLAYER2":
                    st.session_state.p2_guess = i
                    st.rerun()

    st.write("---")

    # --- FOOTER ACTIONS ---
    if st.session_state.game_phase == "PLAYER1":
        if st.button("Confirm Flip & Call Player 2", type="primary", use_container_width=True, disabled=(st.session_state.p1_selected_flip is None)):
            # Apply the flip logic
            idx = st.session_state.p1_selected_flip
            st.session_state.board_state[idx] = 1 - st.session_state.board_state[idx]
            st.session_state.game_phase = "PLAYER2"
            st.rerun()

    elif st.session_state.game_phase == "PLAYER2":
        if st.button("Confirm Guess", type="primary", use_container_width=True, disabled=(st.session_state.p2_guess is None)):
            st.session_state.game_phase = "RESULT"
            st.rerun()

    if st.button("Restart Game", use_container_width=True):
        init_game()
        st.rerun()
