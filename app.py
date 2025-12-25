import streamlit as st
import random

# --- FORCED CSS FOR SEAMLESS CHESSBOARD ---
st.set_page_config(page_title="The Almost Impossible Chess Board Puzzle", layout="centered")

st.markdown("""
    <style>
    /* Remove all gaps between Streamlit columns */
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
    
    /* Force buttons to be exactly 45x45 and remove margins */
    div.stButton > button {
        width: 45px !important;
        height: 45px !important;
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
        border: 0.1px solid rgba(0,0,0,0.1) !important;
        display: block;
    }
    
    /* Style for the wide Confirm/Restart buttons at the top */
    .wide-btn div.stButton > button {
        width: 100% !important;
        height: 40px !important;
        border-radius: 4px !important;
    }

    /* Centering labels */
    .row-label { display: flex; align-items: center; justify-content: flex-end; height: 45px; font-weight: bold; padding-right: 10px; }
    .col-label { text-align: center; font-weight: bold; width: 45px; height: 30px; line-height: 30px; }
    .intro-box { border-left: 5px solid #769656; padding: 15px; background-color: #f9f9f9; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'board' not in st.session_state:
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.p1_selection = None
    st.session_state.p2_selection = None
    st.session_state.phase = "INTRO"

def restart_logic():
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.p1_selection = None
    st.session_state.p2_selection = None
    st.session_state.phase = "PLAYER1"

# --- 1. INTRO STAGE ---
if st.session_state.phase == "INTRO":
    st.markdown(f"""
    <div class="intro-box">
        <h1>The Almost Impossible Chess Board Puzzle</h1>
        <p><b>The Scenario:</b> Two prisoners can win their freedom if they can locate a hidden key.</p>
        <p><b>1. Player 1:</b> Enters the room and sees a board of coins and the key's location. They <u>must</u> flip exactly one coin to change its state (Heads to Tails or vice versa).</p>
        <p><b>2. Player 2:</b> Enters the room after Player 1 has left. They only see the coins. Using only the final state of the board, they must point to the secret square.</p>
        <p><i>Freedom depends on the single flip!</i></p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start Game", type="primary"):
        st.session_state.phase = "PLAYER1"
        st.rerun()

# --- 2. GAMEPLAY ---
else:
    # Text Instructions
    if st.session_state.phase == "PLAYER1":
        st.subheader("Player 1's Turn")
        st.markdown(f"The key is hidden at: **Square {st.session_state.key + 1}**")
        st.write("Select a square to flip (Blue), then confirm.")
    elif st.session_state.phase == "PLAYER2":
        st.subheader("Player 2's Turn")
        st.write("The location is now secret. Identify the correct square and confirm.")

    # TOP CONTROL BUTTONS (Wide area)
    st.markdown('<div class="wide-btn">', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        if st.session_state.phase == "PLAYER1":
            if st.button("Confirm Flip & Call Player 2", type="primary"):
                if st.session_state.p1_selection is not None:
                    idx = st.session_state.p1_selection
                    st.session_state.board[idx] = 1 - st.session_state.board[idx]
                    st.session_state.phase = "PLAYER2"
                    st.rerun()
        elif st.session_state.phase == "PLAYER2":
            if st.button("Confirm Guess", type="primary"):
                if st.session_state.p2_selection is not None:
                    st.session_state.phase = "RESULT"
                    st.rerun()
    with c2:
        if st.button("Restart Game"):
            restart_logic()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- THE CHESSBOARD ---
    # Column Labels
    cols = st.columns([0.6, 1, 1, 1, 1, 1, 1, 1, 1])
    for c in range(8):
        cols[c+1].markdown(f"<div class='col-label'>{c+1}</div>", unsafe_allow_html=True)

    row_labels = ["1", "9", "17", "25", "33", "41", "49", "57"]
    for r in range(8):
        cols = st.columns([0.6, 1, 1, 1, 1, 1, 1, 1, 1])
        cols[0].markdown(f"<div class='row-label'>{row_labels[r]}</div>", unsafe_allow_html=True)
        for c in range(8):
            i = r * 8 + c
            coin = "H" if st.session_state.board[i] == 1 else "T"
            is_dark = (r + c) % 2 == 1
            
            # Coloring logic to mimic the "Perfect" version
            if (st.session_state.phase == "PLAYER1" and i == st.session_state.p1_selection) or \
               (st.session_state.phase == "PLAYER2" and i == st.session_state.p2_selection) or \
               (st.session_state.phase == "RESULT" and i == st.session_state.key):
                # We use a custom trick: Streamlit "primary" buttons are blue.
                # In Result phase, we highlight the key square.
                if cols[c+1].button(coin, key=f"sq_{i}", type="primary"):
                    if st.session_state.phase == "PLAYER1": st.session_state.p1_selection = i
                    elif st.session_state.phase == "PLAYER2": st.session_state.p2_selection = i
                    st.rerun()
            else:
                # Secondary buttons get the Green/Cream via the CSS color logic
                # Note: Streamlit doesn't allow custom hex per button easily, 
                # so we rely on the checkerboard pattern.
                if cols[c+1].button(coin, key=f"sq_{i}", type="secondary"):
                    if st.session_state.phase == "PLAYER1": st.session_state.p1_selection = i
                    elif st.session_state.phase == "PLAYER2": st.session_state.p2_selection = i
                    st.rerun()

    # Results Message
    if st.session_state.phase == "RESULT":
        if st.session_state.p2_selection == st.session_state.key:
            st.success(f"Victory! Player 2 found the key at Square {st.session_state.key + 1}")
        else:
            st.error(f"Game Over. The key was at Square {st.session_state.key + 1}")
