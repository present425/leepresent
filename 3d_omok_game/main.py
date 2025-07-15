#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D 오목 게임 - 메인 실행 파일
"""

import sys
import pygame
from game import OmokGame

def main():
    """메인 함수"""
    print("🎮 3D 오목 게임을 시작합니다!")
    print("게임 규칙:")
    print("- 흑돌(검은색)과 백돌(흰색)을 번갈아가며 놓습니다")
    print("- 가로, 세로, 대각선으로 5개 돌을 연속으로 놓으면 승리합니다")
    print("- ESC 키를 누르면 게임을 종료합니다")
    print("- R 키를 누르면 게임을 재시작합니다")
    print("- 1 키를 누르면 2인용 모드로 전환합니다")
    print("- 2 키를 누르면 AI 대전 모드로 전환합니다")
    print()
    
    # Pygame 초기화
    pygame.init()
    
    # 게임 인스턴스 생성 및 실행
    game = OmokGame()
    game.run()
    
    # Pygame 종료
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 