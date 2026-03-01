import streamlit as st
import math

# ---------------- CONSTANTS ----------------
HUMAN = "X"
AI = "O"

WIN_COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

# ---------------- GAME LOGIC ----------------
def check_winner(board, player):
    return any(all(board[i] == player for i in combo) for combo in WIN_COMBOS)

def is_draw(board):
    return "" not in board

def minimax(board, depth, is_max, alpha, beta):
    if check_winner(board, AI):
        return 10 - depth
    if check_winner(board, HUMAN):
        return depth - 10
    if is_draw(board):
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = AI
                score = minimax(board, depth + 1, False, alpha, beta)
                board[i] = ""
                best = max(best, score)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = HUMAN
                score = minimax(board, depth + 1, True, alpha, beta)
                board[i] = ""
                best = min(best, score)
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best

def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = AI
            score = minimax(board, 0, False, -math.inf, math.inf)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Unbeatable Tic Tac Toe AI")

st.title("🤖 Tic Tac Toe – AI Never Loses")

if "board" not in st.session_state:
    st.session_state.board = [""] * 9

cols = st.columns(3)

for i in range(9):
    with cols[i % 3]:
        if st.button(st.session_state.board[i] or " ", key=i):
            if st.session_state.board[i] == "":
                st.session_state.board[i] = HUMAN

                if not check_winner(st.session_state.board, HUMAN):
                    ai_index = best_move(st.session_state.board)
                    if ai_index is not None:
                        st.session_state.board[ai_index] = AI

# ---------------- RESULT ----------------
if check_winner(st.session_state.board, AI):
    st.error("AI Wins 😈 (Unbeatable)")
elif check_winner(st.session_state.board, HUMAN):
    st.success("You Win 🎉 (Impossible!)")
elif is_draw(st.session_state.board):
    st.warning("It's a Draw 🤝")

if st.button("🔄 Restart Game"):
    st.session_state.board = [""] * 9