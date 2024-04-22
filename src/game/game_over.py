import pygame
import os
import AssetCache
from Buttons import Button
from gamestate import Gamestate, Handler
from highscore import Highscores


class GameOverScene:
    def __init__(self, screen, name, score):
        self.screen = screen
        self.id = "game_over"

        self.player_name = name
        self.score = score

        self.background_image = AssetCache.get_image(os.path.join('src/game/background1.jpg'))
        self.background_image = pygame.transform.scale(self.background_image, (screen.get_width(), screen.get_height()))
        self.font = pygame.font.SysFont("Arial", 40)
        
        self.screen_center_x = screen.get_width() // 2
        first_button_y = screen.get_height() // 2 - 100
        button_spacing = 100  # Space between buttons


        # Scale factor for button width
        scale_factor = 1.5

        # Example for PlayButton, apply the same logic to other buttons
        original_button_image = AssetCache.get_image(os.path.join('src/game/Assets/button1.png'))
        # Scale the image to make it wider
        button_width = original_button_image.get_width() * scale_factor
        button_height = original_button_image.get_height()
        scaled_button_image = pygame.transform.scale(original_button_image, (int(button_width), button_height))

        # Now use the scaled image for your buttons
        self.PlayButton = Button(image=scaled_button_image, pos=(self.screen_center_x, first_button_y),
                                text_input="Play Again", font=self.font, base_color=(255, 255, 255), hovering_color=(100, 255, 100),
                                click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        # Repeat the scaling and creation process for MainMenuButton and QuitButton
        self.MainMenuButton = Button(image=scaled_button_image, pos=(self.screen_center_x, first_button_y + button_spacing),
                                    text_input="Main Menu", font=self.font, base_color=(255, 255, 255), hovering_color=(100, 100, 255),
                                    click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.QuitButton = Button(image=scaled_button_image, pos=(self.screen_center_x, first_button_y + 2 * button_spacing),
                                text_input="Quit Game", font=self.font, base_color=(255, 255, 255), hovering_color=(255, 100, 100),
                                click_sound=AssetCache.get_audio("src/game/Assets/button_click.mp3"))

        self.buttons = [self.PlayButton, self.MainMenuButton, self.QuitButton]
        
    def render(self, gamestate):
        self.screen.blit(self.background_image, (0, 0))
        
        # Background for "LEADERBOARD" text
        leaderboard_background = AssetCache.get_image(os.path.join('src/game/Assets/button2.png'))
        leaderboard_background = pygame.transform.scale(leaderboard_background, (400, 150))
        leaderboard_title_x =-10
        leaderboard_title_y = 0
        self.screen.blit(leaderboard_background, (leaderboard_title_x, leaderboard_title_y + 90))

        # Render "Leaderboard" title on top of the background
        leaderboard_title = self.font.render("LEADERBOARD", True, (255, 255, 255))
        self.screen.blit(leaderboard_title, (leaderboard_title_x + 60, leaderboard_title_y + 140))

        # Retrieve and display last recorded score
        
        last_name = self.player_name
        last_score = self.score

        # Set background for "Your Score"
        your_score_background_y = self.screen_center_x - 610
        your_score_background = AssetCache.get_image(os.path.join('src/game/Assets/button1.png'))
        your_score_background = pygame.transform.scale(your_score_background, (self.screen.get_width() // 3, self.screen.get_height() // 4))
        your_score_background_x = (self.screen.get_width() / 2) - (your_score_background.get_width() / 2)
        self.screen.blit(your_score_background, (your_score_background_x, your_score_background_y))

        # Render "Your Score" section
        your_score_text = self.font.render(f"Your Score: {last_score}", True, (255, 255, 255))
        score_x = self.screen.get_width() / 2 - your_score_text.get_width() / 2
        score_y = your_score_background_y + (your_score_background.get_height() / 2) - (your_score_text.get_height() / 2)
        self.screen.blit(your_score_text, (score_x, score_y))

        # Background for leaderboard scores
        scores_background = AssetCache.get_image(os.path.join('src/game/Assets/button2.png'))
        scores_background = pygame.transform.scale(scores_background, (350, 900))  # Adjust size as needed
        scores_x = 50  # Starting x position for high scores
        scores_y = score_y + 100  # Start below the "Your Score" text
        self.screen.blit(scores_background, (scores_x - 60, scores_y - 350))  # Adjust position as needed

        # Render high scores
        score_spacing = 40
        top_scores = gamestate.scores.get()
        for entry in top_scores[:5]:
            score_text = f"{entry.name}: {entry.score}"
            score_surface = self.font.render(score_text, True, (255, 255, 255))
            self.screen.blit(score_surface, (scores_x, scores_y))
            scores_y += score_spacing

        for button in self.buttons:
            button.update(self.screen)
        pygame.display.flip()


    def initHandlers(self, gamestate):
        gamestate.handlers[self.id] = Handler(
            onRender=self.render,
            onUpdate=lambda gs, dt: None,  # Assuming no update needed
            onKeyPress=lambda gs, key, mod, unicode, scancode: None,  # Assuming no key press handling
            onMousePress=self.handle_mouse_clicks
        )

    def handle_mouse_clicks(self, gamestate, pos, button, touch):
        for btn in self.buttons:
            if btn.checkForInput(pos):
                btn.button_sound()
                if btn.text_input == "Play Again":
                    pygame.mixer_music.stop()
                    gamestate.switch_to_game()
                elif btn.text_input == "Main Menu":
                    pygame.mixer_music.stop()
                    # Switch to the main menu scene (assuming it's defined somewhere)
                    gamestate.switch_to_menu()
                elif btn.text_input == "Quit Game":
                    pygame.quit()
                    exit()
