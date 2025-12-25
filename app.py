import streamlit as st
import random

# --- 1. CONFIG & FORCED CSS (FIXES GAPS & OVERFLOW) ---
st.set_page_config(page_title="The Almost Impossible Chess Board", layout="centered")

st.markdown("""
<style>
    /* Remove gaps between Streamlit columns for a perfect grid */
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
    
    /* Force square buttons & fix text overflow */
    div.stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border: 0.1px solid rgba(0,0,0,0.1) !important;
    }

    /* Fixed height for action buttons to prevent text overflow */
    .st-action-btn button {
        aspect-ratio: auto !important;
        height: 50px !important;
        width: 100% !important;
        border-radius: 5px !important;
        white-space: normal !important;
    }

    /* Matching your Colab Shadow-based Colors */
    .sq-dark button { box-shadow: inset 0 0 0 50px #769656 !important; color: white !important; }
    .sq-light button { box-shadow: inset 0 0 0 50px #eeeed2 !important; color: black !important; }
    .sq-blue button { box-shadow: inset 0 0 0 50px #3498db !important; color: white !important; }
    .sq-gold button { box-shadow: inset 0 0 0 50px #f1c40f !important; color: black !important; }

    /* Centered numbering */
    .row-label { display: flex; align-items: center; justify-content: flex-end; height: 45px; font-weight: bold; padding-right: 10px; color: black; }
    .col-label { text-align: center; font-weight: bold; width: 45px; height: 20px; line-height: 20px; color: black; }
    .intro-box { border-left: 5px solid #769656; padding: 20px; background-color: #f3f3f3; margin-bottom: 20px; color: black; }
</style>
""", unsafe_allow_html=True)

# --- 2. SESSION STATE (The Colab 'Global' Variables) ---
if 'board_state' not in st.session_state:
    st.session_state.board_state = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key_location = random.randint(0, 63)
    st.session_state.p1_selected_flip = None
    st.session_state.p2_guess = None
    st.session_state.game_phase = "INTRO"

def init_game():
    st.session_state.board_state = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key_location = random.randint(0, 63)
    st.session_state.p1_selected_flip = None
    st.session_state.p2_guess = None
    st.session_state.game_phase = "PLAYER1"

def on_sq_click(idx):
    if st.session_state.game_phase == "PLAYER1":
        st.session_state.p1_selected_flip = idx
    elif st.session_state.game_phase == "PLAYER2":
        st.session_state.p2_guess = idx

# --- 3. UI ASSEMBLY ---
if st.session_state.game_phase == "INTRO":
    st.markdown("""
    <div class="intro-box">
        <h1>The Almost Impossible Chess Board Puzzle</h1>
        <p><b>The Scenario:</b> Two prisoners can win their freedom if they can locate a hidden key.</p>
        <p><b>1. Player 1:</b> Enters the room and sees a board of coins and the key's location. They <u>must</u> flip exactly one coin.</p>
        <p><b>2. Player 2:</b> Enters the room after. They only see the coins. They must point to the secret square.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Game", type="primary", use_container_width=True):
        init_game()
        st.rerun()

else:
    # Phase Headers
    if st.session_state.game_phase == "PLAYER1":
        st.header("Player 1's Turn")
        st.write(f"The key is hidden at: **Square {st.session_state.key_location + 1}**")
        st.write("Choose one square to flip (it will turn blue), then confirm.")
    elif st.session_state.game_phase == "PLAYER2":
        st.header("Player 2's Turn")
        st.write("The key's location is secret. Identify the square and confirm.")
    elif st.session_state.game_phase == "RESULT":
        if st.session_state.p2_guess == st.session_state.key_location:
            st.markdown("<h2 style='color:green;'>Victory!</h2>", unsafe_allow_html=True)
            st.success(f"Success! Player 2 found the key at Square {st.session_state.key_location + 1}.")
        else:
            st.markdown("<h2 style='color:red;'>Game Over</h2>", unsafe_allow_html=True)
            st.error(f"Selection: {st.session_state.p2_guess + 1} | Actual Location: {st.session_state.key_location + 1}.")

    # --- ACTION BUTTONS (State Control) ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="st-action-btn">', unsafe_allow_html=True)
        if st.session_state.game_phase == "PLAYER1":
            if st.button("Confirm Flip & Call Player 2"):
                if st.session_state.p1_selected_flip is not None:
                    idx = st.session_state.p1_selected_flip
                    st.session_state.board_state[idx] = 1 - st.session_state.board_state[idx]
                    st.session_state.game_phase = "PLAYER2"
                    st.rerun()
        elif st.session_state.game_phase == "PLAYER2":
            if st.button("Confirm Guess"):
                if st.session_state.p2_guess is not None:
                    st.session_state.game_phase = "RESULT"
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="st-action-btn">', unsafe_allow_html=True)
        if st.button("Restart Game"):
            init_game()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- THE CHESS BOARD ---
    # Column labels
    grid_header = st.columns([0.7] + [1]*8)
    for c in range(8):
        grid_header[c+1].markdown(f"<div class='col-label'>{c+1}</div>", unsafe_allow_html=True)

    row_labels = ["1", "9", "17", "25", "33", "41", "49", "57"]
    for r in range(8):
        row_cols = st.columns([0.7] + [1]*8)
        row_cols[0].markdown(f"<div class='row-label'>{row_labels[r]}</div>", unsafe_allow_html=True)
        
        for c in range(8):
            i = r * 8 + c
            coin = "H" if st.session_state.board_state[i] == 1 else "T"
            
            # CSS Selection Logic
            if (st.session_state.game_phase == "RESULT" and i == st.session_state.key_location):
                sq_class = "sq-gold"
            elif (st.session_state.game_phase == "PLAYER1" and i == st.session_state.p1_selected_flip):
                sq_class = "sq-blue"
            elif (st.session_state.game_phase == "PLAYER2" and i == st.session_state.p2_guess):
                sq_class = "sq-blue"
            else:
                sq_class = "sq-dark" if (r + c) % 2 == 1 else "sq-light"

            with row_cols[c+1]:
                st.markdown(f'<div class="{sq_class}">', unsafe_allow_html=True)
                # Using a callback for state changes
                st.button(coin, key=f"sq_{i}", on_click=on_sq_click, args=(i,))
                st.markdown('</div>', unsafe_allow_html=True)
