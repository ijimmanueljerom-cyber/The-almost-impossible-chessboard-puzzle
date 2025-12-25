import streamlit as st
import random

# --- PUZZLE LOGIC (The Hamming Code/XOR Solution) ---
def get_board_xor(board):
    """Calculates the XOR sum of all indices where the coin is 'Heads' (1)."""
    xor_sum = 0
    for i, val in enumerate(board):
        if val == 1:
            xor_sum ^= i
    return xor_sum

# --- INITIALIZATION ---
if 'board' not in st.session_state:
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key_pos = random.randint(0, 63)
    st.session_state.phase = "PLAYER1"

# --- STYLING (The Gapless Chessboard) ---
st.markdown("""
<style>
    .board-grid {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        width: 100%;
        max-width: 480px;
        aspect-ratio: 1/1;
        margin: auto;
        border: 5px solid #333;
    }
    .tile {
        aspect-ratio: 1/1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
        cursor: pointer;
        border: none;
    }
    .light { background-color: #eeeed2; color: #769656; }
    .dark { background-color: #769656; color: #eeeed2; }
    .highlight-key { box-shadow: inset 0 0 15px 5px gold !important; border: 3px solid gold !important; }
    .highlight-flip { box-shadow: inset 0 0 15px 5px #3498db !important; }
</style>
""", unsafe_allow_html=True)

# --- GAME PHASES ---
st.title("The Almost Impossible Chessboard")

if st.session_state.phase == "PLAYER1":
    current_xor = get_board_xor(st.session_state.board)
    # The Magic Formula: target_key XOR current_board_parity = the coin index to flip
    flip_index = st.session_state.key_pos ^ current_xor
    
    st.subheader("Step 1: Prisoner 1 (The Messenger)")
    st.write(f"Warden hid the key at: **Square {st.session_state.key_pos}**")
    st.write(f"Current Board Parity (XOR): **{current_xor}**")
    st.info(f"💡 MATHEMATICAL SOLUTION: Flip **Square {flip_index}** to make the parity match the key.")
    
    if st.button(f"Flip Square {flip_index} & Call Prisoner 2", use_container_width=True):
        st.session_state.board[flip_index] = 1 - st.session_state.board[flip_index]
        st.session_state.phase = "PLAYER2"
        st.rerun()

elif st.session_state.phase == "PLAYER2":
    st.subheader("Step 2: Prisoner 2 (The Decoder)")
    inferred_key = get_board_xor(st.session_state.board)
    st.write("Prisoner 2 enters. They see only the coins.")
    
    if st.button("Calculate Key Location", type="primary", use_container_width=True):
        st.session_state.p2_guess = inferred_key
        st.session_state.phase = "RESULT"
        st.rerun()

elif st.session_state.phase == "RESULT":
    final_xor = get_board_xor(st.session_state.board)
    st.subheader("Result")
    if final_xor == st.session_state.key_pos:
        st.success(f"VICTORY! Prisoner 2 calculated the XOR sum was {final_xor} and found the key!")
    else:
        st.error("FAILED! The math did not match.")
    
    if st.button("New Game"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- BOARD RENDERING ---
board_html = '<div class="board-grid">'
for i in range(64):
    row, col = divmod(i, 8)
    tile_type = "light" if (row + col) % 2 == 0 else "dark"
    coin = "H" if st.session_state.board[i] == 1 else "T"
    
    # Highlight logic
    extra_class = ""
    if st.session_state.phase == "PLAYER1" and i == st.session_state.key_pos:
        extra_class = "highlight-key"
    
    board_html += f'<div class="tile {tile_type} {extra_class}">{coin}<br><small style="font-size:10px">{i}</small></div>'
board_html += '</div>'

st.markdown(board_html, unsafe_allow_html=True)
