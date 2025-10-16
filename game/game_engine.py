import pygame
from .paddle import Paddle
from .ball import Ball

# Game Constants
WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Load sound effects
        try:
            self.paddle_hit_sound = pygame.mixer.Sound("assets/paddle_hit.wav")
            self.wall_bounce_sound = pygame.mixer.Sound("assets/wall_bounce.wav")
            self.score_sound = pygame.mixer.Sound("assets/score.wav")
        except pygame.error as e:
            print(f"Error loading sound files: {e}")
            print("Please ensure you have an 'assets' folder with the required .wav files.")
            # Handle error gracefully, e.g., by creating dummy sound objects
            self.paddle_hit_sound = pygame.mixer.Sound(buffer=b'')
            self.wall_bounce_sound = pygame.mixer.Sound(buffer=b'')
            self.score_sound = pygame.mixer.Sound(buffer=b'')


        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        # Pass the sounds to the Ball object
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height, self.paddle_hit_sound, self.wall_bounce_sound)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        
        self.winning_score = 5
        self.game_over = False

    def handle_input(self):
        # Don't handle paddle movement if the game is over
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
            self.score_sound.play() # Play score sound
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.score_sound.play() # Play score sound
            self.ball.reset()

        # Check for a winner against the current winning score
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            self.game_over = True

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw game elements
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # If game is over, display the replay menu
        if self.game_over:
            self.draw_game_over_menu(screen)

    def draw_game_over_menu(self, screen):
        """Draws the winner and the replay options on the screen."""
        # Display Winner
        winner_font = pygame.font.SysFont("Arial", 50)
        winner_text_str = "Player Wins!" if self.player_score >= self.winning_score else "AI Wins!"
        text_surface = winner_font.render(winner_text_str, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2 - 100))
        screen.blit(text_surface, text_rect)

        # Display Replay Options
        option_font = pygame.font.SysFont("Arial", 30)
        options = [
            "Press [3] for Best of 3",
            "Press [5] for Best of 5",
            "Press [7] for Best of 7",
            "Press [ESC] to Exit"
        ]
        
        for i, option in enumerate(options):
            option_surface = option_font.render(option, True, WHITE)
            option_rect = option_surface.get_rect(center=(self.width / 2, self.height / 2 + i * 40))
            screen.blit(option_surface, option_rect)
            
    def reset_game(self, new_winning_score):
        """Resets the game state for a new match."""
        self.winning_score = new_winning_score
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.ball.reset()


