import streamlit as st
import random
import streamlit.components.v1 as components

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Impossible Chessboard", layout="centered")

# --- 2. GAME LOGIC & STATE ---
if 'board' not in st.session_state:
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key_loc = random.randint(0, 63)
    st.session_state.phase = "PLAYER1" # PLAYER1, PLAYER2, RESULT
    st.session_state.last_clicked = -1

# Handle clicks from the HTML Grid
query_params = st.query_params
if "clicked" in query_params:
    clicked_idx = int(query_params["clicked"])
    st.session_state.last_clicked = clicked_idx
    # Clear the param so it doesn't trigger again
    st.query_params.clear()
    st.rerun()

# --- 3. CONSTRUCT THE HTML BOARD ---
def render_html_board():
    # Dynamic CSS for colors
    grid_html = """
    <div style="display: grid; grid-template-columns: repeat(8, 1fr); gap: 2px; width: 100%; max-width: 400px; margin: auto; border: 4px solid #333;">
    """
    
    for i in range(64):
        # Determine Color
        row, col = i // 8, i % 8
        is_dark = (row + col) % 2 == 1
        bg_color = "#769656" if is_dark else "#eeeed2" # Chess green/cream
        
        # Override for selection/key
        if st.session_state.phase == "RESULT" and i == st.session_state.key_loc:
            bg_color = "#f1c40f" # Gold for Key
        elif i == st.session_state.last_clicked:
            bg_color = "#3498db" # Blue for Selection
            
        label = "H" if st.session_state.board[i] == 1 else "T"
        if st.session_state.phase == "RESULT" and i == st.session_state.key_loc:
            label = "🔑"

        # This JavaScript tells Streamlit which square was clicked via URL parameters
        click_js = f"window.parent.location.href = window.parent.location.href.split('?')[0] + '?clicked={i}'"
        
        grid_html += f"""
        <div onclick="{click_js}" style="aspect-ratio: 1; background-color: {bg_color}; display: flex; align-items: center; justify-content: center; font-family: sans-serif; font-weight: bold; cursor: pointer; user-select: none; border: 1px solid rgba(0,0,0,0.1);">
            {label}
        </div>
        """
    grid_html += "</div>"
    return grid_html

# --- 4. DISPLAY UI ---
st.title("♟️ Impossible Chessboard")

# Instructions
if st.session_state.phase == "PLAYER1":
    st.info(f"**Player 1:** The key is at **Square {st.session_state.key_loc + 1}**. Click one coin to flip.")
elif st.session_state.phase == "PLAYER2":
    st.warning("**Player 2:** Find the key! Which square was indicated?")
else:
    if st.session_state.last_clicked == st.session_state.key_loc:
        st.success("✨ VICTORY! Found the key!")
    else:
        st.error(f"❌ FAILED! Key was at {st.session_state.key_loc + 1}")

# Render the Board
st.markdown(render_html_board(), unsafe_allow_html=True)

# --- 5. ACTION BUTTONS ---
st.write("---")
if st.session_state.phase == "PLAYER1":
    if st.button("Confirm Flip & Call Player 2", use_container_width=True, type="primary"):
        if st.session_state.last_clicked != -1:
            idx = st.session_state.last_clicked
            st.session_state.board[idx] = 1 - st.session_state.board[idx]
            st.session_state.last_clicked = -1
            st.session_state.phase = "PLAYER2"
            st.rerun()

elif st.session_state.phase == "PLAYER2":
    if st.button("Confirm Guess", use_container_width=True, type="primary"):
        if st.session_state.last_clicked != -1:
            st.session_state.phase = "RESULT"
            st.rerun()

if st.button("Restart New Game", use_container_width=True):
    st.session_state.board = [random.randint(0, 1) for _ in range(64)]
    st.session_state.key_loc = random.randint(0, 63)
    st.session_state.phase = "PLAYER1"
    st.session_state.last_clicked = -1
    st.rerun()
