#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D 오목 게임 - 보드 관리 및 승리 판정
"""

import numpy as np

class Board:
    """오목판 클래스"""
    
    def __init__(self, rows=15, cols=15):
        """보드 초기화"""
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.move_count = 0
    
    def is_valid_move(self, x, y):
        """유효한 수인지 확인"""
        return (0 <= x < self.cols and 
                0 <= y < self.rows and 
                self.board[y][x] == 0)
    
    def place_stone(self, x, y, player):
        """돌을 놓는 함수"""
        if self.is_valid_move(x, y):
            self.board[y][x] = player
            self.move_count += 1
            return True
        return False
    
    def check_win(self, x, y, player):
        """승리 조건 확인"""
        # 8방향 검사 (가로, 세로, 대각선)
        directions = [
            (1, 0),   # 가로
            (0, 1),   # 세로
            (1, 1),   # 우하 대각선
            (1, -1)   # 우상 대각선
        ]
        
        for dx, dy in directions:
            count = 1  # 현재 위치 포함
            
            # 양방향으로 연속된 돌 개수 확인
            # 정방향
            temp_x, temp_y = x + dx, y + dy
            while (0 <= temp_x < self.cols and 
                   0 <= temp_y < self.rows and 
                   self.board[temp_y][temp_x] == player):
                count += 1
                temp_x += dx
                temp_y += dy
            
            # 역방향
            temp_x, temp_y = x - dx, y - dy
            while (0 <= temp_x < self.cols and 
                   0 <= temp_y < self.rows and 
                   self.board[temp_y][temp_x] == player):
                count += 1
                temp_x -= dx
                temp_y -= dy
            
            # 5개 이상이면 승리
            if count >= 5:
                return True
        
        return False
    
    def is_full(self):
        """보드가 가득 찼는지 확인"""
        return self.move_count >= self.rows * self.cols
    
    def get_valid_moves(self):
        """유효한 수들의 리스트 반환"""
        valid_moves = []
        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x] == 0:
                    valid_moves.append((x, y))
        return valid_moves
    
    def copy(self):
        """보드 복사"""
        new_board = Board(self.rows, self.cols)
        new_board.board = self.board.copy()
        new_board.move_count = self.move_count
        return new_board
    
    def print_board(self):
        """보드 출력 (디버깅용)"""
        for row in self.board:
            print(' '.join(['.' if cell == 0 else '●' if cell == 1 else '○' for cell in row]))
        print() 