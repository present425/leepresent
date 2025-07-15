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
    print("🎮 3D Omok Game Starting!")
    print("Game Rules:")
    print("- Place black and white stones alternately")
    print("- Win by placing 5 stones in a row (horizontal, vertical, or diagonal)")
    print("- Press ESC to exit the game")
    print("- Press R to restart the game")
    print("- Press 1 to switch to 2-Player mode")
    print("- Press 2 to switch to AI mode")
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