import streamlit as st
import random

# --- MOBILE APP STYLING (THE PERFECT CHESSBOARD) ---
st.set_page_config(page_title="The Almost Impossible Chess Board Puzzle", layout="centered")

st.markdown("""
    <style>
    /* Remove gaps between squares */
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
    
    /* Perfect Square Buttons */
    div.stButton > button {
        width: 45px !important; height: 45px !important;
        border-radius: 0px !important; border: 0.1px solid rgba(0,0,0,0.1) !important;
        margin: 0px !important; padding: 0px !important;
        font-weight: bold !important;
    }
    
    /* Selection and Result Colors (Locked for 2025) */
    .st-blue button { background-color: #3498db !important; color: white !important; }
    .st-gold button { background-color: #f1c40f !important; color: black !important; }
    .st-dark button { background-color: #769656 !important; color: white !important; }
    .st-light button { background-color: #eeeed2 !important; color: black !important; }

    /* Centered Numbering */
    .row-label { display: flex; align-items: center; justify-content: flex-end; height: 45px; font-weight: bold; padding-right: 10px; }
    .col-label { text-align: center; font-weight: bold; width: 45px; height: 20px; line-height: 20px; }
    
    /* Intro Box */
    .intro-box { border-left: 5px solid #769656; padding: 15px; background-color: #f9f9f9; margin-bottom: 20px; color: black; }
    </style>
""", unsafe_allow_html=True)

# --- APP STATE ---
if 'board' not in st.session_state:
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.p1_sel = None
    st.session_state.p2_sel = None
    st.session_state.phase = "INTRO"

def restart():
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.p1_sel = None
    st.session_state.p2_sel = None
    st.session_state.phase = "PLAYER1"

# --- STAGE 1: INTRO (EXACT SCRIPT) ---
if st.session_state.phase == "INTRO":
    st.markdown("""
    <div class="intro-box">
        <h1>The Almost Impossible Chess Board Puzzle</h1>
        <p><b>The Scenario:</b> Two prisoners can win their freedom if they can locate a hidden key.</p>
        <p><b>1. Player 1:</b> Enters the room and sees a board of coins and the key's location. They <u>must</u> flip exactly one coin to change its state (Heads to Tails or vice versa).</p>
        <p><b>2. Player 2:</b> Enters the room after Player 1 has left. They only see the coins. Using only the final state of the board, they must point to the secret square.</p>
        <p><i>Freedom depends on the single flip!</i></p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Game", type="primary", use_container_width=True):
        st.session_state.phase = "PLAYER1"
        st.rerun()

# --- STAGE 2: GAMEPLAY ---
else:
    if st.session_state.phase == "PLAYER1":
        st.subheader("Player 1's Turn")
        st.write(f"The key is hidden at: **Square {st.session_state.key + 1}**")
        if st.button("Confirm Flip & Call Player 2", type="primary", use_container_width=True):
            if st.session_state.p1_sel is not None:
                st.session_state.board[st.session_state.p1_sel] = 1 - st.session_state.board[st.session_state.p1_sel]
                st.session_state.phase = "PLAYER2"
                st.rerun()
    elif st.session_state.phase == "PLAYER2":
        st.subheader("Player 2's Turn")
        st.write("Warden's info hidden. Identify the square and confirm.")
        if st.button("Confirm Guess", type="primary", use_container_width=True):
            if st.session_state.p2_sel is not None:
                st.session_state.phase = "RESULT"
                st.rerun()
    elif st.session_state.phase == "RESULT":
        if st.session_state.p2_sel == st.session_state.key:
            st.success(f"Victory! Square {st.session_state.key + 1} was correct.")
        else:
            st.error(f"Game Over. The key was at Square {st.session_state.key + 1}.")
        if st.button("Restart Game", use_container_width=True): restart()

    # --- THE BOARD ---
    cols = st.columns([0.7] + [1]*8)
    for c in range(8): cols[c+1].markdown(f"<div class='col-label'>{c+1}</div>", unsafe_allow_html=True)

    row_labels = ["1", "9", "17", "25", "33", "41", "49", "57"]
    for r in range(8):
        cols = st.columns([0.7] + [1]*8)
        cols[0].markdown(f"<div class='row-label'>{row_labels[r]}</div>", unsafe_allow_html=True)
        for c in range(8):
            i = r * 8 + c
            coin = "H" if st.session_state.board[i] == 1 else "T"
            is_dark = (r + c) % 2 == 1
            
            # Color Logic
            css_class = "st-light"
            if is_dark: css_class = "st-dark"
            if (st.session_state.phase == "PLAYER1" and i == st.session_state.p1_sel) or \
               (st.session_state.phase == "PLAYER2" and i == st.session_state.p2_sel):
                css_class = "st-blue"
            if st.session_state.phase == "RESULT" and i == st.session_state.key:
                css_class = "st-gold"

            with cols[c+1]:
                st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                if st.button(coin, key=f"sq_{i}"):
                    if st.session_state.phase == "PLAYER1": st.session_state.p1_sel = i
                    elif st.session_state.phase == "PLAYER2": st.session_state.p2_sel = i
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
