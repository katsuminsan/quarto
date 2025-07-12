import random
from copy import deepcopy
from items import bord as Bord, poll


class Opponent:
    def __init__(self, level="easy"):
        self.level = level  # "easy", "medium", "hard"
        
    def choose_placement(self, board, piece):
        empty_cells = self._get_empty_cells(board)
    
        if self.level == "hard":
            best_score = -float('inf')
            best_moves = []
            
            for pos in empty_cells:
                new_board = deepcopy(board)
                new_board.puton(piece, pos)
                
                if new_board.check(pos):
                    return pos  # 即勝ちならその手を返す
                
                score = self._minimax_place(new_board, depth=1, maximizing=False)
                
                if score > best_score:
                    best_score = score
                    best_moves = [pos]
                elif score == best_score:
                    best_moves.append(pos)
            
            return random.choice(best_moves) if best_moves else random.choice(empty_cells)
            
        elif self.level == "medium":
            winning_moves = []
            for pos in empty_cells:
                 new_board = deepcopy(board)
                 new_board.puton(piece, pos)
                 if new_board.check(pos):
                     winning_moves.append(pos)
            
        elif self.level == "easy":
            return random.choice(empty_cells)
        
    def choose_next_piece(self, board, remaining_pieces):
        if self.level == "hard":
            best_score = float('inf')
            best_candidates = []
            
            for p in remaining_pieces:
                score = 0
                for pos in self._get_empty_cells(board):
                    new_board = deepcopy(board)
                    new_board.puton(p, pos)
                    if new_board.check(pos):
                        score += 1  # この駒を渡すと相手が勝つ可能性あり
                if score < best_score:
                    best_score = score
                    best_candidates =[p]
                elif score == best_score:
                    best_candidates.append(p)
            return random.choice(best_candidates) # 同点の駒からランダムに選択
            
        elif self.level == "medium":
            safe_pieces = []
            for p in remaining_pieces:
                is_dangerous = False
                for pos in self._get_empty_cells(board):
                    new_board = deepcopy(board)
                    new_board.puton(p, pos)
                    if new_board.check(pos):
                        is_dangerous = True
                        break
                if not is_dangerous:
                    safe_pieces.append(p)
            return random.choice(safe_pieces) if safe_pieces else random.choice(remaining_pieces)
            
        elif self.level == "easy":
            # easy mode
            return random.choice(remaining_pieces)
        
    def decide_best_move(self, board, depth=2):
        _, best = self._minimax(board, depth, maximizing=True)
        return best  # (座標, 駒ID)

    def _minimax_place(self, board, depth, maximizing):
        """
        駒を置いた後の評価(再帰的)
        maximizing: TrueならCOMの手番、Falseなら相手
        """
        win, _ = board.all_check()
        if win:
            return 10 if maximizing else -10
        if depth == 0:
            return self._evaluate(board)

        empty_cells = self._get_empty_cells(board)
        if maximizing:
            max_eval = -float('inf')
            for pos in empty_cells:
                new_board = deepcopy(board)
                new_board.puton(poll(0), pos)  # 仮の駒(ビット無視)
                eval = self._minimax_place(new_board, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for pos in empty_cells:
                new_board = deepcopy(board)
                new_board.puton(poll(0), pos)
                eval = self._minimax_place(new_board, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def show(self, board):
        coord, piece_id = self.decide_best_move(board)
        print(f"AIは {coord} に駒 {piece_id} を置きます")

    def _get_empty_cells(self, board):
        return [(r, c) for r in range(4) for c in range(4) if board.exist((r, c)) == 16]

    def _get_remaining_pieces(self, board: Bord):
        placed = set()
        for r in range(4):
            for c in range(4):
                val = board.exist((r, c))
                if val != 16:
                    placed.add(val)
        return [poll(i) for i in range(16) if i not in placed]
    
    def _evaluate(self, board):
        is_end, _ = board.all_check()
        if is_end:
            return 100  # 勝ち
        # 評価関数の改良:三つ揃いなどで勝ちに近い状態を評価
        # ここでは暫定的に 0 としておき、必要に応じて詳細化可能
        return 0

    def _minimax(self, board, depth, maximizing):
        is_end, _ = board.all_check()
        if depth == 0 or is_end:
            return self._evaluate(board), None

        empty_cells = self._get_empty_cells(board)
        remaining_pieces = self._get_remaining_pieces(board)

        if maximizing:
            max_eval = float('-inf')
            best_move = None
            for coord in empty_cells:
                for p_id in remaining_pieces:
                    new_board = deepcopy(board)
                    new_board.puton(poll(p_id), coord)
                    score, _ = self._minimax(new_board, depth - 1, False)
                    if score > max_eval:
                        max_eval = score
                        best_move = (coord, p_id)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for coord in empty_cells:
                for p_id in remaining_pieces:
                    new_board = deepcopy(board)
                    new_board.puton(poll(p_id), coord)
                    score, _ = self._minimax(new_board, depth - 1, True)
                    if score < min_eval:
                        min_eval = score
                        best_move = (coord, p_id)
            return min_eval, best_move
