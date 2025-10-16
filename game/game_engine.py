import pygame
from .paddle import Paddle
from .ball import Ball

# Game Constants
WHITE = (255, 255, 255)
WINNING_SCORE = 5

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        
        # Add a game over state
        self.game_over = False

    def handle_input(self):
        # Don't handle input if the game is over
        if self.game_over:
            return
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # If the game is over, stop updating game objects
        if self.game_over:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # Check for a winner
        if self.player_score >= WINNING_SCORE or self.ai_score >= WINNING_SCORE:
            self.game_over = True

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # If game is over, display the winner
        if self.game_over:
            self.draw_winner(screen)
            
    def draw_winner(self, screen):
        """Draws the winner text on the screen."""
        end_font = pygame.font.SysFont("Arial", 60)
        winner_text = "Player Wins!" if self.player_score >= WINNING_SCORE else "AI Wins!"
        
        text_surface = end_font.render(winner_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2))
        screen.blit(text_surface, text_rect)
