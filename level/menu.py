import pygame, sys
from button import Button
from settings import *
from level import Level
from player import Player
import csv
from pathlib import Path


class Menu:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        pygame.display.set_caption('wtg')
        icon = pygame.image.load('graphic/test/r1.png').convert()
        pygame.display.set_icon(icon)
        self.bg = pygame.image.load('assets/Background.png').convert_alpha()
        self.level = Level()
        main_sound = pygame.mixer.Sound('audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops = -1)
        self.font = pygame.font.Font("assets/monogram.ttf",50)
        self.back_10 = pygame.image.load('assets/Background.png').convert_alpha()
        self.back_10 = pygame.transform.scale(self.back_10, (int(self.back_10.get_width() * 3.2), int(self.back_10.get_height() * 3.6)))
        highscore_file = 'highscore.csv'
        self.word=''
        self.leaderBoard = []
        if Path(highscore_file).is_file() == False:
            tmp_list = ['xxx', 0]
            for x in range(5):
                self.leaderBoard.append(tmp_list)

            with open("highscore.csv", 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for x in range(5):
                    writer.writerow(self.leaderBoard[x])
        else:
            with open("highscore.csv", 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x in reader:
                    self.leaderBoard.append(x)
        
    def get_font(self,size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("assets/font.ttf", size)
    
    def get_font2(self,size):
        return pygame.font.Font("assets/SOV_raksil.ttf", size)

    def play(self):
        while True:
            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
            if self.level.gamestatus == False:
                self.get_score()
            

            pygame.display.update()
        
    def get_score(self):
        self.screen.blit(self.back_10, (0, 0))
        self.draw_text(f"Your Score: {self.level.export_score()}", self.font, "white", 50, 280)
        if self.level.endgame_text == "congrat!!":
            self.draw_text(f"{self.level.endgame_text}",self.font, "white", 95, 100)
        else:
            self.draw_text(f"{self.level.endgame_text}", self.font, "white", 80, 100)
        name = []
        text = self.input()
        name.append(text)
        name.append(self.level.export_score())
        self.leaderBoard.append(name)
        for x in range(5):
            if self.level.export_score() > int(self.leaderBoard[x][1]):
                tmp = 1
                self.leaderBoard.remove(self.leaderBoard[4])
                while 4 - tmp >= x:
                    self.leaderBoard[4 - tmp + 1] = self.leaderBoard[4 - tmp]
                    tmp += 1
                self.leaderBoard[x] = name
                break
        with open("highscore.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for x in range(5):
                writer.writerow(self.leaderBoard[x])
        self.main_menu()
    
    def main_menu(self):
        while True:
            self.screen.blit(self.bg, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
            name = self.get_font2(30).render("65010988 วิชญ์วิสิฐ โชติกิจสมบูรณ์", True, "#b68f40")
            name_rect = name.get_rect(center=(640,650))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                                text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                                text_input="LEADERBOARDS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                                text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)
            self.screen.blit(name,name_rect)

            for self.button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                self.button.changeColor(MENU_MOUSE_POS)
                self.button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_m:
                                self.level.toggle_menu()
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.leaderboard()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
    
    def leaderboard(self):
        done=True
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        while done:
            self.screen.blit(self.back_10, (0, 0))
            self.draw_text("LEADERBOARD", self.font, 'white',170, 50)
            with open('highscore.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, x1 in enumerate(reader):
                    for y, y1 in enumerate(x1):
                        self.draw_text(f"{y1}", self.font, 'white', 155 + (y * 420), 150 + (x * 80))
            
            OPTIONS_BACK = Button(image=None, pos=(640, 660), 
                            text_input="PRESS SPACE : MAIN MENU", font=self.get_font(25), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        done = False
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                #         done = False
            pygame.display.update()

    def draw_text(self,text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        self.screen.blit(img, (x, y))
    
    def input(self):
        self.screen.blit(self.back_10, (0, 0))
        self.draw_text("Please enter your name: ",self.font, "white", 50,350)
        pygame.display.flip()
        done = True
        while done:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.word = self.word[:-1]
                    if event.key <= 127 and event.key != pygame.K_BACKSPACE:
                        self.word += chr(event.key)                
                    if event.key == pygame.K_RETURN:
                        done = False
                self.draw_text(self.word , self.font, "white", 500, 350)
                pygame.display.flip()
        pygame.display.update()
        self.word = self.word.strip('\r')
        return self.word
    
Menu().main_menu()