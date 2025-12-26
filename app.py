import streamlit as st
import random

# --- 1. PAGE CONFIGURATION & FORCED GRID CSS ---
st.set_page_config(page_title="Impossible Chessboard", layout="centered")

st.markdown("""
<style>
    /* Force the board into an 8x8 Grid */
    .board-container {
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 2px;
        width: 100%;
        max-width: 450px;
        margin: 0 auto;
    }

    /* Style the buttons inside the grid */
    .board-container button {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        padding: 0px !important;
        margin: 0px !important;
        line-height: 1 !important;
        border-radius: 0px !important;
        font-weight: bold !important;
    }

    /* Target Streamlit's button container to prevent unwanted padding */
    div[data-testid="stHorizontalBlock"] {
        gap: 0px !important;
    }
</style>
""", unsafe_allow_html=True)

# ... (Keep your existing initialization and logic functions here) ...

# --- 3. REPLACING THE BOARD RENDERING SECTION ---
st.title("Impossible Chessboard")

if st.session_state.game_phase == "INTRO":
    # ... (Keep your Intro code) ...
    pass
else:
    # Status Header
    if st.session_state.game_phase == "PLAYER1":
        st.info(f"🔑 Key Location: Square {st.session_state.key_location + 1}")
    
    # WE CREATE A CONTAINER FOR THE GRID
    # Using st.container() with a specific class
    with st.container():
        # This div creates the 8x8 structure
        st.markdown('<div class="board-container">', unsafe_allow_html=True)
        
        # We loop 64 times and place buttons
        # Note: In Streamlit, buttons inside markdown aren't interactive, 
        # so we use columns but with the CSS fix above to stop them from stacking.
        
        for r in range(8):
            cols = st.columns(8)
            for c in range(8):
                i = r * 8 + c
                
                label = "H" if st.session_state.board_state[i] == 1 else "T"
                btn_type = "secondary"
                
                if st.session_state.game_phase == "PLAYER1" and i == st.session_state.p1_selected_flip:
                    btn_type = "primary"
                elif st.session_state.game_phase == "PLAYER2" and i == st.session_state.p2_guess:
                    btn_type = "primary"
                elif st.session_state.game_phase == "RESULT" and i == st.session_state.key_location:
                    btn_type = "primary"
                    label = "🔑"

                if cols[c].button(label, key=f"tile_{i}", type=btn_type):
                    # Your toggle logic
                    if st.session_state.game_phase == "PLAYER1":
                        st.session_state.p1_selected_flip = i
                    elif st.session_state.game_phase == "PLAYER2":
                        st.session_state.p2_guess = i
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ... (Keep your "Confirm" and "Restart" buttons below) ...
