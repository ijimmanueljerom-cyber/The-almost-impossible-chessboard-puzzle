import streamlit as st
import random

# --- 1. PAGE CONFIG & MOBILE-READY CSS ---
st.set_page_config(page_title="The Almost Impossible Chess Board", layout="centered")

st.markdown("""
<style>
    /* Prevent Streamlit standard padding gaps */
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
    div.stButton > button {
        width: 45px !important; height: 45px !important;
        border-radius: 0px !important; margin: 0px !important; padding: 0px !important;
        font-weight: bold !important; font-size: 16px !important; border: none !important;
    }
    
    /* Impenetrable Colors using Box Shadows (Matching your Colab) */
    .sq-dark button { box-shadow: inset 0 0 0 50px #769656 !important; color: white !important; }
    .sq-light button { box-shadow: inset 0 0 0 50px #eeeed2 !important; color: black !important; }
    .sq-blue button { box-shadow: inset 0 0 0 50px #3498db !important; color: white !important; }
    .sq-gold button { box-shadow: inset 0 0 0 50px #f1c40f !important; color: black !important; }

    /* Layout Helpers */
    .row-label { display: flex; align-items: center; justify-content: flex-end; height: 45px; font-weight: bold; padding-right: 10px; color: black; }
    .col-label { text-align: center; font-weight: bold; width: 45px; height: 20px; line-height: 20px; color: black; }
    .intro-box { border-left: 5px solid #769656; padding: 20px; background-color: #f3f3f3; margin-bottom: 20px; color: black; }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE (Replacing Global Variables) ---
if 'game_phase' not in st.session_state:
    st.session_state.game_phase = "INTRO"
    st.session_state.board_state = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key_location = random.randint(0, 63)
    st.session_state.p1_selected_flip = None
    st.session_state.p2_guess = None

def init_game():
    st.session_state.board_state = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key_location = random.randint(0, 63)
    st.session_state.p1_selected_flip = None
    st.session_state.p2_guess = None
    st.session_state.game_phase = "PLAYER1"

# --- 3. PHASE 1: INTRO ---
if st.session_state.game_phase == "INTRO":
    st.markdown("""
    <div class="intro-box">
        <h1>The Almost Impossible Chess Board Puzzle</h1>
        <p><b>The Scenario:</b> Two prisoners can win their freedom if they can locate a hidden key.</p>
        <p><b>1. Player 1:</b> Enters the room and sees a board of coins and the key's location. They <u>must</u> flip exactly one coin.</p>
        <p><b>2. Player 2:</b> Enters the room after. They only see the coins. They must point to the secret square.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Game", use_container_width=True):
        init_game()
        st.rerun()

# --- 4. PHASE 2 & 3: GAMEPLAY ---
else:
    # Header Logic
    if st.session_state.game_phase == "PLAYER1":
        st.subheader("Player 1's Turn")
        st.write(f"The key is hidden at: **Square {st.session_state.key_location + 1}**")
        st.info("Choose one square to flip (blue), then confirm.")
        if st.button("Confirm Flip & Call Player 2", type="primary"):
            if st.session_state.p1_selected_flip is not None:
                idx = st.session_state.p1_selected_flip
                st.session_state.board_state[idx] = 1 - st.session_state.board_state[idx]
                st.session_state.game_phase = "PLAYER2"
                st.rerun()

    elif st.session_state.game_phase == "PLAYER2":
        st.subheader("Player 2's Turn")
        st.write("The key's location is now secret. Identify the square and confirm.")
        if st.button("Confirm Guess", type="primary"):
            if st.session_state.p2_guess is not None:
                st.session_state.game_phase = "RESULT"
                st.rerun()

    elif st.session_state.game_phase == "RESULT":
        if st.session_state.p2_guess == st.session_state.key_location:
            st.success(f"Victory! Player 2 found the key at Square {st.session_state.key_location + 1}.")
        else:
            st.error(f"Game Over. Selection: {st.session_state.p2_guess + 1} | Actual: {st.session_state.key_location + 1}")
        if st.button("Restart Game"):
            init_game()
            st.rerun()

    # --- THE BOARD RENDERING ---
    # Column Headers
    cols = st.columns([0.7] + [1]*8)
    for c in range(8):
        cols[c+1].markdown(f"<div class='col-label'>{c+1}</div>", unsafe_allow_html=True)

    # Grid Rows
    row_starts = [1, 9, 17, 25, 33, 41, 49, 57]
    for r in range(8):
        cols = st.columns([0.7] + [1]*8)
        cols[0].markdown(f"<div class='row-label'>{row_starts[r]}</div>", unsafe_allow_html=True)
        
        for c in range(8):
            i = r * 8 + c
            coin = "H" if st.session_state.board_state[i] == 1 else "T"
            
            # Color Logic (Reveal Gold only in Result Phase)
            reveal_key = (st.session_state.game_phase == "RESULT")
            
            if reveal_key and i == st.session_state.key_location:
                sq_class = "sq-gold"
            elif st.session_state.game_phase == "PLAYER1" and i == st.session_state.p1_selected_flip:
                sq_class = "sq-blue"
            elif st.session_state.game_phase == "PLAYER2" and i == st.session_state.p2_guess:
                sq_class = "sq-blue"
            else:
                sq_class = "sq-dark" if (r + c) % 2 == 1 else "sq-light"

            with cols[c+1]:
                st.markdown(f'<div class="{sq_class}">', unsafe_allow_html=True)
                if st.button(coin, key=f"sq_{i}"):
                    if st.session_state.game_phase == "PLAYER1":
                        st.session_state.p1_selected_flip = i
                    elif st.session_state.game_phase == "PLAYER2":
                        st.session_state.p2_guess = i
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
