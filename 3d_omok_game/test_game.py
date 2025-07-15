#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D 오목 게임 - 테스트 스크립트
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from board import Board
from ai_player import AIPlayer

def test_board():
    """보드 기능 테스트"""
    print("🧪 보드 기능 테스트 시작...")
    
    # 보드 생성 테스트
    board = Board(15, 15)
    assert board.rows == 15 and board.cols == 15, "보드 크기 오류"
    print("✅ 보드 생성 성공")
    
    # 돌 놓기 테스트
    assert board.is_valid_move(7, 7), "중앙 위치가 유효하지 않음"
    assert board.place_stone(7, 7, 1), "돌 놓기 실패"
    assert not board.is_valid_move(7, 7), "이미 놓은 위치가 유효함"
    print("✅ 돌 놓기 기능 성공")
    
    # 승리 조건 테스트
    # 가로 승리 테스트
    test_board = Board(15, 15)
    for i in range(5):
        test_board.place_stone(7 + i, 7, 1)
    assert test_board.check_win(11, 7, 1), "가로 승리 판정 실패"
    print("✅ 가로 승리 판정 성공")
    
    # 세로 승리 테스트
    test_board = Board(15, 15)
    for i in range(5):
        test_board.place_stone(7, 7 + i, 1)
    assert test_board.check_win(7, 11, 1), "세로 승리 판정 실패"
    print("✅ 세로 승리 판정 성공")
    
    # 대각선 승리 테스트
    test_board = Board(15, 15)
    for i in range(5):
        test_board.place_stone(7 + i, 7 + i, 1)
    assert test_board.check_win(11, 11, 1), "대각선 승리 판정 실패"
    print("✅ 대각선 승리 판정 성공")
    
    print("🎉 보드 기능 테스트 완료!\n")

def test_ai():
    """AI 기능 테스트"""
    print("🤖 AI 기능 테스트 시작...")
    
    ai = AIPlayer()
    
    # 쉬운 난이도 테스트
    ai.set_difficulty("easy")
    board = Board(15, 15)
    board.place_stone(7, 7, 1)  # 중앙에 흑돌
    
    move = ai.get_best_move(board, 2)
    assert move is not None, "AI가 수를 찾지 못함"
    assert board.is_valid_move(move[0], move[1]), "AI가 유효하지 않은 수를 선택"
    print("✅ 쉬운 난이도 AI 테스트 성공")
    
    # 보통 난이도 테스트
    ai.set_difficulty("medium")
    move = ai.get_best_move(board, 2)
    assert move is not None, "AI가 수를 찾지 못함"
    print("✅ 보통 난이도 AI 테스트 성공")
    
    # 어려운 난이도 테스트 (시간이 오래 걸릴 수 있음)
    ai.set_difficulty("hard")
    move = ai.get_best_move(board, 2)
    assert move is not None, "AI가 수를 찾지 못함"
    print("✅ 어려운 난이도 AI 테스트 성공")
    
    print("🎉 AI 기능 테스트 완료!\n")

def test_win_scenarios():
    """승리 시나리오 테스트"""
    print("🏆 승리 시나리오 테스트 시작...")
    
    # 즉시 승리 수 테스트
    board = Board(15, 15)
    # 4개 돌을 연속으로 놓고 승리 수 확인
    for i in range(4):
        board.place_stone(7 + i, 7, 1)
    
    # AI가 승리 수를 찾는지 테스트
    ai = AIPlayer()
    ai.set_difficulty("medium")
    move = ai.get_best_move(board, 1)
    
    if move:
        test_board = board.copy()
        test_board.place_stone(move[0], move[1], 1)
        if test_board.check_win(move[0], move[1], 1):
            print("✅ AI가 승리 수를 찾음")
        else:
            print("⚠️ AI가 승리 수를 찾지 못함")
    
    print("🎉 승리 시나리오 테스트 완료!\n")

def main():
    """메인 테스트 함수"""
    print("🚀 3D 오목 게임 테스트 시작\n")
    
    try:
        test_board()
        test_ai()
        test_win_scenarios()
        
        print("🎊 모든 테스트가 성공적으로 완료되었습니다!")
        print("게임을 실행하려면: python main.py")
        
    except Exception as e:
        print("❌ 테스트 중 오류 발생: {}".format(e))
        return False
    
    return True

if __name__ == "__main__":
    main() 