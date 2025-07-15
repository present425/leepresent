#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D 오목 게임 - 핵심 게임 로직
"""

import pygame
import numpy as np
import sys
import math
from board import Board
from ai_player import AIPlayer

class OmokGame:
    """3D 오목 게임 클래스"""
    
    def __init__(self):
        """게임 초기화"""
        # 화면 설정
        self.WIDTH = 1400
        self.HEIGHT = 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("3D 오목 게임 - Enhanced 3D Effects")
        
        # 색상 정의 (3D 효과를 위한 그라데이션 색상들)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        self.LIGHT_GRAY = (192, 192, 192)
        
        # 나무 보드 색상 (3D 효과용)
        self.WOOD_DARK = (101, 67, 33)
        self.WOOD_MEDIUM = (139, 69, 19)
        self.WOOD_LIGHT = (160, 82, 45)
        self.WOOD_HIGHLIGHT = (205, 133, 63)
        
        # 돌 색상 (3D 효과용)
        self.STONE_BLACK_DARK = (20, 20, 20)
        self.STONE_BLACK_MEDIUM = (40, 40, 40)
        self.STONE_BLACK_LIGHT = (60, 60, 60)
        self.STONE_BLACK_HIGHLIGHT = (100, 100, 100)
        
        self.STONE_WHITE_DARK = (200, 200, 200)
        self.STONE_WHITE_MEDIUM = (220, 220, 220)
        self.STONE_WHITE_LIGHT = (240, 240, 240)
        self.STONE_WHITE_HIGHLIGHT = (255, 255, 255)
        
        # 기타 색상
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.YELLOW = (255, 255, 0)
        self.GOLD = (255, 215, 0)
        self.SILVER = (192, 192, 192)
        
        # 폰트 설정 (한글 지원)
        try:
            # macOS 기본 한글 폰트들 시도
            font_names = [
                'AppleGothic',
                'Arial Unicode MS', 
                'Helvetica',
                'Arial',
                'DejaVu Sans'
            ]
            
            font_found = False
            for font_name in font_names:
                try:
                    self.font = pygame.font.SysFont(font_name, 36)
                    self.small_font = pygame.font.SysFont(font_name, 24)
                    self.large_font = pygame.font.SysFont(font_name, 48)
                    font_found = True
                    break
                except:
                    continue
            
            if not font_found:
                # 기본 폰트 사용
                self.font = pygame.font.Font(None, 36)
                self.small_font = pygame.font.Font(None, 24)
                self.large_font = pygame.font.Font(None, 48)
                
        except:
            # 폰트 로드 실패시 기본 폰트 사용
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
            self.large_font = pygame.font.Font(None, 48)
        
        # 게임 상태
        self.board = Board(15, 15)  # 15x15 오목판
        self.current_player = 1  # 1: 흑돌, 2: 백돌
        self.game_mode = "2p"  # "2p": 2인용, "ai": AI 대전
        self.game_over = False
        self.winner = None
        self.last_move = None
        
        # AI 플레이어
        self.ai_player = AIPlayer()
        self.ai_difficulty = "medium"  # easy, medium, hard
        
        # 3D 효과를 위한 설정
        self.board_offset_x = 150
        self.board_offset_y = 150
        self.cell_size = 40
        self.stone_radius = 18
        self.board_depth = 15  # 보드 두께
        
        # 클릭 감지 영역
        self.board_rect = pygame.Rect(
            self.board_offset_x, 
            self.board_offset_y, 
            self.board.cols * self.cell_size, 
            self.board.rows * self.cell_size
        )
        
        # 애니메이션 효과
        self.animation_timer = 0
        self.show_win_line = False
        self.win_line_points = []
        
        # 3D 조명 효과
        self.light_source = (self.WIDTH // 2, 100)  # 조명 위치
        self.ambient_light = 0.3  # 환경광
        self.diffuse_light = 0.7  # 확산광
        
        # 마우스 호버 효과
        self.mouse_pos = (0, 0)
        self.hover_cell = None
        
        # 돌 놓기 애니메이션
        self.stone_animations = []  # [(x, y, player, progress), ...]
        
        # 보드 테두리 3D 효과
        self.board_border_width = 20
        self.board_border_depth = 10
    
    def run(self):
        """게임 메인 루프"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                    self.update_hover_cell(event.pos)
            
            # AI 턴 처리
            if (self.game_mode == "ai" and 
                self.current_player == 2 and 
                not self.game_over):
                self.ai_turn()
            
            # 애니메이션 업데이트
            self.animation_timer += 1
            self.update_animations()
            
            # 화면 그리기
            self.draw()
            pygame.display.flip()
            clock.tick(60)
    
    def update_hover_cell(self, pos):
        """마우스 호버 셀 업데이트"""
        if self.board_rect.collidepoint(pos):
            board_x = (pos[0] - self.board_offset_x) // self.cell_size
            board_y = (pos[1] - self.board_offset_y) // self.cell_size
            
            if (0 <= board_x < self.board.cols and 
                0 <= board_y < self.board.rows and
                self.board.board[board_y][board_x] == 0):
                self.hover_cell = (board_x, board_y)
            else:
                self.hover_cell = None
        else:
            self.hover_cell = None
    
    def update_animations(self):
        """애니메이션 업데이트"""
        # 돌 놓기 애니메이션 업데이트
        for i in range(len(self.stone_animations) - 1, -1, -1):
            x, y, player, progress = self.stone_animations[i]
            progress += 0.1
            if progress >= 1.0:
                self.stone_animations.pop(i)
            else:
                self.stone_animations[i] = (x, y, player, progress)
    
    def handle_keydown(self, key):
        """키보드 입력 처리"""
        if key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif key == pygame.K_r:
            self.restart_game()
        elif key == pygame.K_1:
            self.game_mode = "2p"
            self.restart_game()
        elif key == pygame.K_2:
            self.game_mode = "ai"
            self.restart_game()
        elif key == pygame.K_e:
            self.ai_difficulty = "easy"
            self.ai_player.set_difficulty("easy")
        elif key == pygame.K_m:
            self.ai_difficulty = "medium"
            self.ai_player.set_difficulty("medium")
        elif key == pygame.K_h:
            self.ai_difficulty = "hard"
            self.ai_player.set_difficulty("hard")
    
    def handle_mouse_click(self, pos):
        """마우스 클릭 처리"""
        if self.game_over:
            return
        
        # AI 모드에서 AI 턴일 때는 클릭 무시
        if self.game_mode == "ai" and self.current_player == 2:
            return
        
        # 보드 영역 클릭 확인
        if self.board_rect.collidepoint(pos):
            # 클릭 위치를 보드 좌표로 변환
            board_x = (pos[0] - self.board_offset_x) // self.cell_size
            board_y = (pos[1] - self.board_offset_y) // self.cell_size
            
            # 유효한 좌표인지 확인
            if (0 <= board_x < self.board.cols and 
                0 <= board_y < self.board.rows):
                self.make_move(board_x, board_y)
    
    def make_move(self, x, y):
        """돌을 놓는 함수"""
        if self.board.is_valid_move(x, y):
            self.board.place_stone(x, y, self.current_player)
            self.last_move = (x, y)
            
            # 돌 놓기 애니메이션 추가
            self.stone_animations.append((x, y, self.current_player, 0.0))
            
            # 승리 확인
            if self.board.check_win(x, y, self.current_player):
                self.game_over = True
                self.winner = self.current_player
                self.show_win_line = True
                self.win_line_points = self.get_win_line_points(x, y, self.current_player)
            else:
                # 플레이어 전환
                self.current_player = 3 - self.current_player  # 1 -> 2, 2 -> 1
    
    def get_win_line_points(self, x, y, player):
        """승리 라인의 점들을 찾는 함수"""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = 1
            points = [(x, y)]
            
            # 정방향 확인
            temp_x, temp_y = x + dx, y + dy
            while (0 <= temp_x < self.board.cols and 
                   0 <= temp_y < self.board.rows and 
                   self.board.board[temp_y][temp_x] == player):
                count += 1
                points.append((temp_x, temp_y))
                temp_x += dx
                temp_y += dy
            
            # 역방향 확인
            temp_x, temp_y = x - dx, y - dy
            while (0 <= temp_x < self.board.cols and 
                   0 <= temp_y < self.board.rows and 
                   self.board.board[temp_y][temp_x] == player):
                count += 1
                points.append((temp_x, temp_y))
                temp_x -= dx
                temp_y -= dy
            
            if count >= 5:
                return points
        
        return []
    
    def ai_turn(self):
        """AI 턴 처리"""
        # AI가 최선의 수를 계산
        best_move = self.ai_player.get_best_move(self.board, 2)
        if best_move:
            x, y = best_move
            self.make_move(x, y)
    
    def restart_game(self):
        """게임 재시작"""
        self.board = Board(15, 15)
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.show_win_line = False
        self.win_line_points = []
        self.stone_animations = []
        self.hover_cell = None
    
    def draw(self):
        """화면 그리기"""
        # 배경 그라데이션 그리기
        self.draw_background_gradient()
        
        # 3D 보드 그리기
        self.draw_3d_board()
        
        # 돌 그리기
        self.draw_stones()
        
        # 호버 효과 그리기
        self.draw_hover_effect()
        
        # 승리 라인 그리기
        if self.show_win_line and self.win_line_points:
            self.draw_win_line()
        
        # UI 그리기
        self.draw_ui()
        
        # 게임 상태 메시지 그리기
        self.draw_status()
    
    def draw_background_gradient(self):
        """배경 그라데이션 그리기"""
        for y in range(self.HEIGHT):
            # 위에서 아래로 갈수록 어두워지는 그라데이션
            ratio = y / self.HEIGHT
            r = int(205 * (1 - ratio * 0.3))
            g = int(133 * (1 - ratio * 0.3))
            b = int(63 * (1 - ratio * 0.3))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.WIDTH, y))
    
    def draw_3d_board(self):
        """3D 효과가 있는 보드 그리기"""
        # 보드 테두리 3D 효과 (입체감)
        self.draw_board_border_3d()
        
        # 보드 배경 (나무 질감)
        self.draw_board_texture()
        
        # 격자 그리기 (3D 효과)
        self.draw_grid_3d()
        
        # 중앙점 표시
        center_x = self.board_offset_x + (self.board.cols // 2) * self.cell_size
        center_y = self.board_offset_y + (self.board.rows // 2) * self.cell_size
        pygame.draw.circle(self.screen, self.BLACK, (center_x, center_y), 4)
    
    def draw_board_border_3d(self):
        """보드 테두리 3D 효과"""
        board_width = self.board.cols * self.cell_size
        board_height = self.board.rows * self.cell_size
        
        # 왼쪽 테두리 (그림자)
        for i in range(self.board_border_depth):
            color_intensity = max(0, min(255, 255 - (i * 20)))
            color = (color_intensity, color_intensity, color_intensity)
            pygame.draw.rect(self.screen, color, (
                self.board_offset_x - self.board_border_width + i,
                self.board_offset_y - self.board_border_width + i,
                self.board_border_width - i,
                board_height + self.board_border_width * 2 - i * 2
            ))
        
        # 위쪽 테두리 (그림자)
        for i in range(self.board_border_depth):
            color_intensity = max(0, min(255, 255 - (i * 20)))
            color = (color_intensity, color_intensity, color_intensity)
            pygame.draw.rect(self.screen, color, (
                self.board_offset_x - self.board_border_width + i,
                self.board_offset_y - self.board_border_width + i,
                board_width + self.board_border_width * 2 - i * 2,
                self.board_border_width - i
            ))
        
        # 오른쪽 테두리 (하이라이트)
        for i in range(self.board_border_depth):
            color_intensity = max(0, min(255, 200 + (i * 10)))
            color = (color_intensity, color_intensity, color_intensity)
            pygame.draw.rect(self.screen, color, (
                self.board_offset_x + board_width + i,
                self.board_offset_y - self.board_border_width + i,
                self.board_border_width - i,
                board_height + self.board_border_width * 2 - i * 2
            ))
        
        # 아래쪽 테두리 (하이라이트)
        for i in range(self.board_border_depth):
            color_intensity = max(0, min(255, 200 + (i * 10)))
            color = (color_intensity, color_intensity, color_intensity)
            pygame.draw.rect(self.screen, color, (
                self.board_offset_x - self.board_border_width + i,
                self.board_offset_y + board_height + i,
                board_width + self.board_border_width * 2 - i * 2,
                self.board_border_width - i
            ))
    
    def draw_board_texture(self):
        """보드 나무 질감 그리기"""
        board_rect = pygame.Rect(
            self.board_offset_x,
            self.board_offset_y,
            self.board.cols * self.cell_size,
            self.board.rows * self.cell_size
        )
        
        # 기본 나무 색상
        pygame.draw.rect(self.screen, self.WOOD_MEDIUM, board_rect)
        
        # 나무 질감 효과 (작은 사각형들)
        for y in range(0, self.board.rows * self.cell_size, 8):
            for x in range(0, self.board.cols * self.cell_size, 8):
                if (x + y) % 16 == 0:
                    pygame.draw.rect(self.screen, self.WOOD_DARK, (
                        self.board_offset_x + x,
                        self.board_offset_y + y,
                        4, 4
                    ))
                elif (x + y) % 16 == 8:
                    pygame.draw.rect(self.screen, self.WOOD_HIGHLIGHT, (
                        self.board_offset_x + x,
                        self.board_offset_y + y,
                        4, 4
                    ))
    
    def draw_grid_3d(self):
        """3D 격자 그리기"""
        for i in range(self.board.rows + 1):
            # 가로선 (그림자 효과)
            shadow_offset = 2
            start_pos_shadow = (self.board_offset_x + shadow_offset, 
                              self.board_offset_y + i * self.cell_size + shadow_offset)
            end_pos_shadow = (self.board_offset_x + self.board.cols * self.cell_size + shadow_offset, 
                            self.board_offset_y + i * self.cell_size + shadow_offset)
            pygame.draw.line(self.screen, self.DARK_GRAY, start_pos_shadow, end_pos_shadow, 3)
            
            # 가로선 (메인)
            start_pos = (self.board_offset_x, self.board_offset_y + i * self.cell_size)
            end_pos = (self.board_offset_x + self.board.cols * self.cell_size, 
                      self.board_offset_y + i * self.cell_size)
            pygame.draw.line(self.screen, self.BLACK, start_pos, end_pos, 2)
            
            # 세로선 (그림자 효과)
            start_pos_shadow = (self.board_offset_x + i * self.cell_size + shadow_offset, 
                              self.board_offset_y + shadow_offset)
            end_pos_shadow = (self.board_offset_x + i * self.cell_size + shadow_offset, 
                            self.board_offset_y + self.board.rows * self.cell_size + shadow_offset)
            pygame.draw.line(self.screen, self.DARK_GRAY, start_pos_shadow, end_pos_shadow, 3)
            
            # 세로선 (메인)
            start_pos = (self.board_offset_x + i * self.cell_size, self.board_offset_y)
            end_pos = (self.board_offset_x + i * self.cell_size, 
                      self.board_offset_y + self.board.rows * self.cell_size)
            pygame.draw.line(self.screen, self.BLACK, start_pos, end_pos, 2)
    
    def draw_stones(self):
        """돌 그리기 (3D 효과)"""
        for y in range(self.board.rows):
            for x in range(self.board.cols):
                if self.board.board[y][x] != 0:
                    self.draw_stone_3d(x, y, self.board.board[y][x])
        
        # 애니메이션 중인 돌들 그리기
        for x, y, player, progress in self.stone_animations:
            self.draw_stone_3d_animated(x, y, player, progress)
    
    def draw_stone_3d(self, x, y, player):
        """3D 돌 그리기"""
        stone_x = self.board_offset_x + x * self.cell_size + self.cell_size // 2
        stone_y = self.board_offset_y + y * self.cell_size + self.cell_size // 2
        
        # 조명 효과 계산
        light_intensity = self.calculate_light_intensity(stone_x, stone_y)
        
        if player == 1:  # 흑돌
            # 그림자
            shadow_offset = 3
            pygame.draw.circle(self.screen, self.STONE_BLACK_DARK, 
                             (stone_x + shadow_offset, stone_y + shadow_offset), 
                             self.stone_radius)
            
            # 메인 돌
            pygame.draw.circle(self.screen, self.STONE_BLACK_MEDIUM, 
                             (stone_x, stone_y), self.stone_radius)
            
            # 하이라이트 (조명 효과)
            highlight_radius = int(self.stone_radius * 0.6)
            highlight_x = stone_x - 4
            highlight_y = stone_y - 4
            pygame.draw.circle(self.screen, self.STONE_BLACK_HIGHLIGHT, 
                             (highlight_x, highlight_y), highlight_radius)
            
            # 반사광
            reflection_radius = int(self.stone_radius * 0.3)
            reflection_x = stone_x - 2
            reflection_y = stone_y - 2
            pygame.draw.circle(self.screen, self.STONE_BLACK_LIGHT, 
                             (reflection_x, reflection_y), reflection_radius)
            
        else:  # 백돌
            # 그림자
            shadow_offset = 3
            pygame.draw.circle(self.screen, self.STONE_WHITE_DARK, 
                             (stone_x + shadow_offset, stone_y + shadow_offset), 
                             self.stone_radius)
            
            # 메인 돌
            pygame.draw.circle(self.screen, self.STONE_WHITE_MEDIUM, 
                             (stone_x, stone_y), self.stone_radius)
            
            # 하이라이트 (조명 효과)
            highlight_radius = int(self.stone_radius * 0.7)
            highlight_x = stone_x - 3
            highlight_y = stone_y - 3
            pygame.draw.circle(self.screen, self.STONE_WHITE_HIGHLIGHT, 
                             (highlight_x, highlight_y), highlight_radius)
            
            # 반사광
            reflection_radius = int(self.stone_radius * 0.4)
            reflection_x = stone_x - 1
            reflection_y = stone_y - 1
            pygame.draw.circle(self.screen, self.STONE_WHITE_LIGHT, 
                             (reflection_x, reflection_y), reflection_radius)
        
        # 마지막 돌 표시 (빨간 테두리)
        if self.last_move == (x, y):
            pygame.draw.circle(self.screen, self.RED, (stone_x, stone_y), 
                             self.stone_radius + 2, 3)
    
    def draw_stone_3d_animated(self, x, y, player, progress):
        """애니메이션 중인 3D 돌 그리기"""
        stone_x = self.board_offset_x + x * self.cell_size + self.cell_size // 2
        stone_y = self.board_offset_y + y * self.cell_size + self.cell_size // 2
        
        # 애니메이션 효과 (위에서 떨어지는 효과)
        bounce_height = int(20 * (1 - progress))
        animated_y = stone_y - bounce_height
        
        # 그림자 (떨어지는 동안 그림자도 작아짐)
        shadow_scale = 1.0 - (bounce_height / 20.0) * 0.3
        shadow_radius = int(self.stone_radius * shadow_scale)
        shadow_offset = int(3 * shadow_scale)
        
        if player == 1:  # 흑돌
            pygame.draw.circle(self.screen, self.STONE_BLACK_DARK, 
                             (stone_x + shadow_offset, stone_y + shadow_offset), 
                             shadow_radius)
            pygame.draw.circle(self.screen, self.STONE_BLACK_MEDIUM, 
                             (stone_x, animated_y), self.stone_radius)
        else:  # 백돌
            pygame.draw.circle(self.screen, self.STONE_WHITE_DARK, 
                             (stone_x + shadow_offset, stone_y + shadow_offset), 
                             shadow_radius)
            pygame.draw.circle(self.screen, self.STONE_WHITE_MEDIUM, 
                             (stone_x, animated_y), self.stone_radius)
    
    def draw_hover_effect(self):
        """호버 효과 그리기"""
        if self.hover_cell and not self.game_over:
            x, y = self.hover_cell
            hover_x = self.board_offset_x + x * self.cell_size + self.cell_size // 2
            hover_y = self.board_offset_y + y * self.cell_size + self.cell_size // 2
            
            # 호버 링 (깜빡이는 효과)
            alpha = abs(int(255 * (self.animation_timer % 30) / 30))
            hover_color = (100, 100, 255, alpha)
            
            # 외부 링
            pygame.draw.circle(self.screen, hover_color, (hover_x, hover_y), 
                             self.stone_radius + 5, 2)
            
            # 내부 링
            pygame.draw.circle(self.screen, hover_color, (hover_x, hover_y), 
                             self.stone_radius + 2, 1)
    
    def calculate_light_intensity(self, x, y):
        """조명 강도 계산"""
        # 조명원으로부터의 거리 계산
        distance = math.sqrt((x - self.light_source[0])**2 + (y - self.light_source[1])**2)
        max_distance = math.sqrt(self.WIDTH**2 + self.HEIGHT**2)
        
        # 거리에 따른 조명 강도 (가까울수록 밝음)
        intensity = 1.0 - (distance / max_distance) * 0.5
        return max(0.3, min(1.0, intensity))
    
    def draw_win_line(self):
        """승리 라인 그리기 (3D 효과)"""
        if not self.win_line_points:
            return
        
        # 애니메이션 효과
        alpha = abs(int(255 * (self.animation_timer % 60) / 60))
        
        # 승리 라인 그리기 (3D 효과)
        points = []
        for x, y in self.win_line_points:
            screen_x = self.board_offset_x + x * self.cell_size + self.cell_size // 2
            screen_y = self.board_offset_y + y * self.cell_size + self.cell_size // 2
            points.append((screen_x, screen_y))
        
        if len(points) >= 2:
            # 그림자 효과
            shadow_points = [(x + 3, y + 3) for x, y in points]
            pygame.draw.lines(self.screen, self.DARK_GRAY, False, shadow_points, 7)
            
            # 메인 라인
            pygame.draw.lines(self.screen, self.GOLD, False, points, 5)
            
            # 하이라이트 효과
            highlight_points = [(x - 1, y - 1) for x, y in points]
            pygame.draw.lines(self.screen, self.YELLOW, False, highlight_points, 2)
    
    def draw_ui(self):
        """UI 그리기 (3D 효과)"""
        # UI 배경 (반투명)
        ui_surface = pygame.Surface((300, 200))
        ui_surface.set_alpha(200)
        ui_surface.fill(self.WOOD_DARK)
        self.screen.blit(ui_surface, (20, 20))
        
        # 게임 모드 표시
        mode_text = "2-Player Mode" if self.game_mode == "2p" else f"AI Mode ({self.ai_difficulty})"
        mode_surface = self.font.render(mode_text, True, self.WHITE)
        self.screen.blit(mode_surface, (30, 30))
        
        # 현재 플레이어 표시
        player_text = "Black Turn" if self.current_player == 1 else "White Turn"
        player_color = self.STONE_BLACK_HIGHLIGHT if self.current_player == 1 else self.STONE_WHITE_HIGHLIGHT
        player_surface = self.font.render(player_text, True, player_color)
        self.screen.blit(player_surface, (30, 70))
        
        # 조작법 안내
        controls = [
            "ESC: Exit",
            "R: Restart", 
            "1: 2-Player Mode",
            "2: AI Mode",
            "E: AI Easy",
            "M: AI Medium",
            "H: AI Hard"
        ]
        
        for i, control in enumerate(controls):
            control_surface = self.small_font.render(control, True, self.WHITE)
            self.screen.blit(control_surface, (30, 120 + i * 25))
    
    def draw_status(self):
        """게임 상태 메시지 그리기 (3D 효과)"""
        if self.game_over:
            # 배경 (그림자 효과)
            if self.winner:
                winner_text = "Black Wins!" if self.winner == 1 else "White Wins!"
                status_surface = self.large_font.render(winner_text, True, self.RED)
            else:
                status_surface = self.large_font.render("Draw!", True, self.BLUE)
            
            # 그림자
            shadow_surface = self.large_font.render(winner_text if self.winner else "Draw!", True, self.DARK_GRAY)
            shadow_rect = shadow_surface.get_rect()
            shadow_rect.center = (self.WIDTH // 2 + 3, 53)
            self.screen.blit(shadow_surface, shadow_rect)
            
            # 메시지 중앙 배치
            text_rect = status_surface.get_rect()
            text_rect.center = (self.WIDTH // 2, 50)
            self.screen.blit(status_surface, text_rect)
            
            # 재시작 안내
            restart_surface = self.small_font.render("Press R to restart", True, self.WHITE)
            restart_rect = restart_surface.get_rect()
            restart_rect.center = (self.WIDTH // 2, 90)
            self.screen.blit(restart_surface, restart_rect) 