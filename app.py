import streamlit as st
import random

# --- SEAMLESS DESIGN CSS ---
st.set_page_config(page_title="The Almost Impossible Chessboard", layout="centered")

st.markdown("""
    <style>
    /* Remove gaps between columns and rows */
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
    div.stButton > button {
        width: 45px !important; height: 45px !important;
        border-radius: 0px !important; border: 0.1px solid rgba(0,0,0,0.1) !important;
        margin: 0px !important; padding: 0px !important;
    }
    .row-label { display: flex; align-items: center; justify-content: flex-end; height: 45px; font-weight: bold; padding-right: 10px; }
    .col-label { text-align: center; font-weight: bold; width: 45px; height: 25px; }
    .intro-box { border-left: 5px solid #769656; padding: 15px; background-color: #f9f9f9; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- STATE PERSISTENCE ---
if 'board' not in st.session_state:
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.p1_selection = None
    st.session_state.p2_selection = None
    st.session_state.phase = "INTRO"

def restart():
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.p1_selection = None
    st.session_state.p2_selection = None
    st.session_state.phase = "PLAYER1"

# --- 1. INTRO STAGE ---
if st.session_state.phase == "INTRO":
    st.markdown("""
    <div class="intro-box">
        <h1>The Almost Impossible Chess Board Puzzle</h1>
        <p><b>The Scenario:</b> Two prisoners can win their freedom if they can locate a hidden key.</p>
        <p><b>1. Player 1:</b> Sees the secret key location. They <u>must</u> flip exactly one coin to change its state.</p>
        <p><b>2. Player 2:</b> Enters later. Using only the final state of the board, they must identify the secret square.</p>
        <p><i>Freedom depends on the single flip!</i></p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Game", type="primary"):
        st.session_state.phase = "PLAYER1"
        st.rerun()

# --- 2. GAMEPLAY ---
else:
    # Header Information
    if st.session_state.phase == "PLAYER1":
        st.subheader("Player 1's Turn")
        st.markdown(f"The key is hidden at: **Square {st.session_state.key + 1}**")
        st.write("Select a square to flip (Blue), then confirm.")
    elif st.session_state.phase == "PLAYER2":
        st.subheader("Player 2's Turn")
        st.write("The location is now secret. Find the square with the key and confirm.")
    
    # Action Buttons
    c_act, c_res = st.columns([2, 1])
    with c_act:
        if st.session_state.phase == "PLAYER1":
            if st.button("Confirm Flip & Call Player 2", type="success", use_container_width=True):
                if st.session_state.p1_selection is not None:
                    idx = st.session_state.p1_selection
                    st.session_state.board[idx] = 1 - st.session_state.board[idx]
                    st.session_state.phase = "PLAYER2"
                    st.rerun()
        elif st.session_state.phase == "PLAYER2":
            if st.button("Confirm Guess", type="success", use_container_width=True):
                if st.session_state.p2_selection is not None:
                    st.session_state.phase = "RESULT"
                    st.rerun()
    with c_res:
        if st.button("Restart Game", type="info", use_container_width=True):
            restart()
            st.rerun()

    # The Board Rendering
    # Column Labels
    cols = st.columns([0.5] + [1]*8)
    for c in range(8):
        cols[c+1].markdown(f"<div class='col-label'>{c+1}</div>", unsafe_allow_html=True)

    row_labels = ["1", "9", "17", "25", "33", "41", "49", "57"]
    for r in range(8):
        cols = st.columns([0.5] + [1]*8)
        cols[0].markdown(f"<div class='row-label'>{row_labels[r]}</div>", unsafe_allow_html=True)
        for c in range(8):
            i = r * 8 + c
            coin = "H" if st.session_state.board[i] == 1 else "T"
            is_dark = (r + c) % 2 == 1
            
            # Button Colors (Identical to our Perfect version)
            if st.session_state.phase == "PLAYER1" and i == st.session_state.p1_selection:
                b_type = "primary" # Blue
            elif st.session_state.phase == "PLAYER2" and i == st.session_state.p2_selection:
                b_type = "primary" # Blue
            elif st.session_state.phase == "RESULT" and i == st.session_state.key:
                b_type = "primary" # Gold (re-colored via primary in Results)
            else:
                b_type = "secondary" # Standard Green/Cream via CSS

            if cols[c+1].button(coin, key=f"sq_{i}", type=b_type):
                if st.session_state.phase == "PLAYER1":
                    st.session_state.p1_selection = i
                    st.rerun()
                elif st.session_state.phase == "PLAYER2":
                    st.session_state.p2_selection = i
                    st.rerun()

    # Result Messages
    if st.session_state.phase == "RESULT":
        if st.session_state.p2_selection == st.session_state.key:
            st.success(f"Victory! Player 2 found the key at Square {st.session_state.key + 1}")
        else:
            st.error(f"Game Over. Player 2 chose {st.session_state.p2_selection + 1}, but the key was at {st.session_state.key + 1}")
