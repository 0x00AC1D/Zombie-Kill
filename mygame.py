import pygame
import random
from pygame.locals import USEREVENT

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1000
        self.HEIGHT = 500
        self.BLACK = (0, 0, 0)
        self.GRAY = (50, 50, 50)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.VIOLET = (255, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.STAT_FONT = pygame.font.SysFont(None, 40)
        self.MENU_FONT = pygame.font.SysFont(None, 100)
        zombie_img_files = ["zombie_1.gif", "zombie_2.png", "zombie_3.png"]
        self.ZOMBIE_IMGS = [pygame.image.load("assets/images/" + file) for file in zombie_img_files]
        self.BG_IMG = pygame.image.load("assets/images/background.png")
        self.AIM_IMG = pygame.image.load("assets/images/aim_pointer.png")
        self.GUN_IMG = pygame.image.load("assets/images/gun_1.png")
        self.BLOOD_IMG = pygame.image.load("assets/images/zombie_blood.png")
        self.SHOT_SOUND = pygame.mixer.Sound("assets/sounds/shot_sound.wav")
        self.BG_SOUND = pygame.mixer.Sound("assets/sounds/background.wav")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.play_button = pygame.Rect(self.WIDTH / 2 - 100, 250, 200, 50)
        self.quit_button = pygame.Rect(self.WIDTH / 2 - 100, 310, 200, 50)
        self.buttons = [self.play_button, self.quit_button]
        self.restart_game()
        self.show_menu(True)
        
    def restart_game(self):
        self.blood_coords = []
        self.time_left = 8
        self.score = 0

    def refresh_text(self, text, x, y, color, font=None):
            if font is None:
                font = self.STAT_FONT
            text = font.render(text, True, color)
            self.screen.blit(text, (x, y))

    def show_menu(self, is_first_game):
        while True:
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and self.quit_button.collidepoint(mx, my)):
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.play_button.collidepoint(mx, my):
                    self.restart_game()
                    self.game_loop()

            self.screen.fill(self.BLACK)

            if is_first_game:
                self.refresh_text("WELCOME TO ZOMBIE-KILL", self.WIDTH / 2 - 470, 100, self.RED, self.MENU_FONT)
            else:
                self.refresh_text("TIME IS UP!", self.WIDTH / 2 - 200, 100, self.BLUE, self.MENU_FONT)
                self.refresh_text(f"SCORE {self.score}", self.WIDTH / 2 - 150, 170, self.RED, self.MENU_FONT)

            for button in self.buttons:
                pygame.draw.rect(self.screen, self.GRAY, button)

            self.refresh_text("PLAY", self.WIDTH / 2 - 40, 265, self.BLACK)
            self.refresh_text("QUIT", self.WIDTH / 2 - 40, 325, self.BLACK)
            pygame.display.update()

    def random_zombie(self):
        zombie_img = random.choice(self.ZOMBIE_IMGS)
        zx = random.randint(0, self.WIDTH - 200)
        zy = random.randint(0, self.HEIGHT - 300)
        return zombie_img, zx, zy

    def append_blood_coords(self, bx, by):
        """ reduce blood to last 5 kills """
        self.blood_coords.append((bx, by))
        if len(self.blood_coords) > 5:
            self.blood_coords = self.blood_coords[-5:]

    def game_loop(self):
        self.BG_SOUND.play()
        zombie_img, zx, zy = self.random_zombie()
        pygame.time.set_timer(USEREVENT + 1, 1000)

        while True:
            mx, my = pygame.mouse.get_pos()
            zombie_box = pygame.Rect(zx, zy, zombie_img.get_width(), zombie_img.get_height())
            shot_box = pygame.Rect(mx, my, self.AIM_IMG.get_width(), self.AIM_IMG.get_height())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
                elif event.type == USEREVENT + 1:
                    self.time_left -= 1
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.SHOT_SOUND.play()

                    if zombie_box.colliderect(shot_box):
                        self.score += 1
                        self.append_blood_coords(mx, my)
                        zombie_img, zx, zy = self.random_zombie()

            if self.time_left == 0:
                break

            self.screen.blit(self.BG_IMG, (0,0))

            for bx, by in self.blood_coords:
                self.screen.blit(self.BLOOD_IMG, (bx, by))

            self.refresh_text(f"TIME LEFT : {self.time_left}", self.WIDTH - 200, 0, self.VIOLET)
            self.refresh_text(f"SCORE : {self.score}", 8, 0, self.RED)
            self.screen.blit(zombie_img, (zx, zy))
            self.screen.blit(self.AIM_IMG, (mx - 48, my - 48))
            self.screen.blit(self.GUN_IMG, (mx, self.HEIGHT - 250))
            pygame.display.update()

        self.show_menu(False)

if __name__ == "__main__":
    game = Game()
    game.game_loop()