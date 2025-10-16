import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
    
    # In game/ball.py

    def check_collision(self, player, ai):
        # Check collision with player paddle (left side)
        if self.velocity_x < 0: # Ball is moving left
            if self.rect().colliderect(player.rect()):
                self.velocity_x *= -1
            
                # Optional: Add variety to the bounce based on where it hits the paddle
                middle_y = player.y + player.height / 2
                difference_in_y = middle_y - self.y
                reduction_factor = (player.height / 2) / 3
                self.velocity_y = -1 * (difference_in_y / reduction_factor)


        # Check collision with AI paddle (right side)
        if self.velocity_x > 0: # Ball is moving right
            if self.rect().colliderect(ai.rect()):
                self.velocity_x *= -1

                # Optional: Add variety to the bounce
                middle_y = ai.y + ai.height / 2
                difference_in_y = middle_y - self.y
                reduction_factor = (ai.height / 2) / 3
                self.velocity_y = -1 * (difference_in_y / reduction_factor)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
