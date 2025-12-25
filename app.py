import streamlit as st
import random

# --- 2025 GAPLESS CONFIGURATION ---
st.set_page_config(page_title="The Almost Impossible Chess Board Puzzle", layout="centered")

# Force CSS to kill all gaps and fix button colors
st.markdown("""
    <style>
    /* Remove gaps between columns in 2025 versions */
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
    
    /* Make chess buttons square and seamless */
    div.stButton > button {
        width: 45px !important; height: 45px !important;
        border-radius: 0px !important; margin: 0px !important; padding: 0px !important;
        border: 0.1px solid rgba(0,0,0,0.1) !important;
    }
    
    /* Ensure action buttons are wide enough for the text */
    .wide-controls div.stButton > button {
        width: 100% !important; height: 45px !important; border-radius: 5px !important;
    }

    /* Vertical centering for row numbers */
    .row-num { display: flex; align-items: center; justify-content: flex-end; height: 45px; font-weight: bold; padding-right: 10px; }
    .col-num { text-align: center; font-weight: bold; width: 45px; height: 30px; }
    .intro-box { border-left: 5px solid #769656; padding: 15px; background-color: #f9f9f9; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'board' not in st.session_state:
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.p1_sel = None
    st.session_state.p2_sel = None
    st.session_state.phase = "INTRO"

def reset_game():
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key = random.randint(0, 63)
    st.session_state.p1_sel = None
    st.session_state.p2_sel = None
    st.session_state.phase = "PLAYER1"

# --- 1. INTRO STAGE ---
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
    if st.button("Start Game", type="primary", key="start_btn"):
        st.session_state.phase = "PLAYER1"
        st.rerun()

# --- 2. GAMEPLAY ---
else:
    # Instructions
    if st.session_state.phase == "PLAYER1":
        st.subheader("Player 1's Turn")
        st.markdown(f"The key is hidden at: **Square {st.session_state.key + 1}**")
        btn_txt = "Confirm Flip & Call Player 2"
    elif st.session_state.phase == "PLAYER2":
        st.subheader("Player 2's Turn")
        st.write("Warden's info hidden. Identify the square and confirm.")
        btn_txt = "Confirm Guess"
    else:
        st.subheader("Verification Result")
        btn_txt = None

    # Wide Action Buttons
    st.markdown('<div class="wide-controls">', unsafe_allow_html=True)
    c_act, c_res = st.columns(2)
    with c_act:
        if btn_txt and st.button(btn_txt, type="primary", key="main_action"):
            if st.session_state.phase == "PLAYER1" and st.session_state.p1_sel is not None:
                st.session_state.board[st.session_state.p1_sel] = 1 - st.session_state.board[st.session_state.p1_sel]
                st.session_state.phase = "PLAYER2"
                st.rerun()
            elif st.session_state.phase == "PLAYER2" and st.session_state.p2_sel is not None:
                st.session_state.phase = "RESULT"
                st.rerun()
    with c_res:
        if st.button("Restart Game", key="restart"):
            reset_game()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- THE BOARD (Using 2025 gap=None feature) ---
    cols = st.columns([0.7] + [1]*8, gap=None)
    for c in range(8):
        cols[c+1].markdown(f"<div class='col-num'>{c+1}</div>", unsafe_allow_html=True)

    row_starts = ["1", "9", "17", "25", "33", "41", "49", "57"]
    for r in range(8):
        cols = st.columns([0.7] + [1]*8, gap=None)
        cols[0].markdown(f"<div class='row-num'>{row_starts[r]}</div>", unsafe_allow_html=True)
        for c in range(8):
            i = r * 8 + c
            coin = "H" if st.session_state.board[i] == 1 else "T"
            
            # Button Type/Color Logic
            is_blue = (st.session_state.phase == "PLAYER1" and i == st.session_state.p1_sel) or \
                      (st.session_state.phase == "PLAYER2" and i == st.session_state.p2_sel)
            is_gold = (st.session_state.phase == "RESULT" and i == st.session_state.key)
            
            b_type = "primary" if (is_blue or is_gold) else "secondary"
            
            if cols[c+1].button(coin, key=f"sq_{i}", type=b_type):
                if st.session_state.phase == "PLAYER1": st.session_state.p1_sel = i
                elif st.session_state.phase == "PLAYER2": st.session_state.p2_sel = i
                st.rerun()

    if st.session_state.phase == "RESULT":
        if st.session_state.p2_sel == st.session_state.key:
            st.success(f"Victory! Square {st.session_state.key + 1} was correct.")
        else:
            st.error(f"Game Over. The key was at Square {st.session_state.key + 1}.")
