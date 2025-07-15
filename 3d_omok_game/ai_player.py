#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D 오목 게임 - AI 플레이어
"""

import random
import numpy as np

class AIPlayer:
    """AI 플레이어 클래스"""
    
    def __init__(self):
        """AI 플레이어 초기화"""
        self.difficulty = "medium"  # easy, medium, hard
    
    def get_best_move(self, board, player):
        """최선의 수를 찾는 함수"""
        valid_moves = board.get_valid_moves()
        
        if not valid_moves:
            return None
        
        # 난이도에 따른 AI 로직
        if self.difficulty == "easy":
            return self.get_random_move(valid_moves)
        elif self.difficulty == "medium":
            return self.get_medium_move(board, valid_moves, player)
        else:  # hard
            return self.get_hard_move(board, valid_moves, player)
    
    def get_random_move(self, valid_moves):
        """랜덤 수 선택 (쉬운 난이도)"""
        return random.choice(valid_moves)
    
    def get_medium_move(self, board, valid_moves, player):
        """중간 난이도 AI - 기본적인 전략 사용"""
        # 즉시 승리할 수 있는 수가 있는지 확인
        for x, y in valid_moves:
            test_board = board.copy()
            test_board.place_stone(x, y, player)
            if test_board.check_win(x, y, player):
                return (x, y)
        
        # 상대방이 즉시 승리할 수 있는 수를 막기
        opponent = 3 - player
        for x, y in valid_moves:
            test_board = board.copy()
            test_board.place_stone(x, y, opponent)
            if test_board.check_win(x, y, opponent):
                return (x, y)
        
        # 중앙 근처의 수 우선 선택
        center_x, center_y = board.cols // 2, board.rows // 2
        center_moves = []
        other_moves = []
        
        for x, y in valid_moves:
            distance = abs(x - center_x) + abs(y - center_y)
            if distance <= 3:
                center_moves.append((x, y))
            else:
                other_moves.append((x, y))
        
        if center_moves:
            return random.choice(center_moves)
        else:
            return random.choice(other_moves)
    
    def get_hard_move(self, board, valid_moves, player):
        """어려운 난이도 AI - 미니맥스 알고리즘 사용"""
        best_score = float('-inf')
        best_move = None
        
        for x, y in valid_moves:
            test_board = board.copy()
            test_board.place_stone(x, y, player)
            
            # 미니맥스 알고리즘으로 점수 계산
            score = self.minimax(test_board, 3, False, player, float('-inf'), float('inf'))
            
            if score > best_score:
                best_score = score
                best_move = (x, y)
        
        return best_move
    
    def minimax(self, board, depth, is_maximizing, player, alpha, beta):
        """미니맥스 알고리즘 (알파-베타 가지치기 포함)"""
        opponent = 3 - player
        
        # 종료 조건
        if depth == 0 or board.is_full():
            return self.evaluate_board(board, player)
        
        # 승리 조건 확인
        for y in range(board.rows):
            for x in range(board.cols):
                if board.board[y][x] != 0:
                    if board.check_win(x, y, board.board[y][x]):
                        if board.board[y][x] == player:
                            return 1000
                        else:
                            return -1000
        
        valid_moves = board.get_valid_moves()
        
        if is_maximizing:
            max_eval = float('-inf')
            for x, y in valid_moves:
                test_board = board.copy()
                test_board.place_stone(x, y, player)
                eval_score = self.minimax(test_board, depth - 1, False, player, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for x, y in valid_moves:
                test_board = board.copy()
                test_board.place_stone(x, y, opponent)
                eval_score = self.minimax(test_board, depth - 1, True, player, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def evaluate_board(self, board, player):
        """보드 상태 평가"""
        opponent = 3 - player
        score = 0
        
        # 각 위치에서 연속된 돌 개수 확인
        for y in range(board.rows):
            for x in range(board.cols):
                if board.board[y][x] != 0:
                    current_player = board.board[y][x]
                    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
                    
                    for dx, dy in directions:
                        count = 1
                        blocked = 0
                        
                        # 정방향 확인
                        temp_x, temp_y = x + dx, y + dy
                        while (0 <= temp_x < board.cols and 
                               0 <= temp_y < board.rows and 
                               board.board[temp_y][temp_x] == current_player):
                            count += 1
                            temp_x += dx
                            temp_y += dy
                        
                        # 정방향 막힘 확인
                        if not (0 <= temp_x < board.cols and 
                               0 <= temp_y < board.rows and 
                               board.board[temp_y][temp_x] == 0):
                            blocked += 1
                        
                        # 역방향 확인
                        temp_x, temp_y = x - dx, y - dy
                        while (0 <= temp_x < board.cols and 
                               0 <= temp_y < board.rows and 
                               board.board[temp_y][temp_x] == current_player):
                            count += 1
                            temp_x -= dx
                            temp_y -= dy
                        
                        # 역방향 막힘 확인
                        if not (0 <= temp_x < board.cols and 
                               0 <= temp_y < board.rows and 
                               board.board[temp_y][temp_x] == 0):
                            blocked += 1
                        
                        # 점수 계산
                        if current_player == player:
                            score += self.get_line_score(count, blocked)
                        else:
                            score -= self.get_line_score(count, blocked)
        
        return score
    
    def get_line_score(self, count, blocked):
        """연속된 돌 개수에 따른 점수 계산"""
        if count >= 5:
            return 10000
        elif count == 4:
            if blocked == 0:
                return 1000
            elif blocked == 1:
                return 100
        elif count == 3:
            if blocked == 0:
                return 100
            elif blocked == 1:
                return 10
        elif count == 2:
            if blocked == 0:
                return 10
            elif blocked == 1:
                return 1
        
        return 0
    
    def set_difficulty(self, difficulty):
        """AI 난이도 설정"""
        if difficulty in ["easy", "medium", "hard"]:
            self.difficulty = difficulty 