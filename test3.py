import pygame
import sys
import re

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
SILVER = (192, 192, 192)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
LIME = (0, 128, 0)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
PURPLE = (128, 0, 128)



class Button:
    def __init__(self, x, y, width, height, color, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        return self.rect.collidepoint(mouse) and click[0] == 1


class Window:
    def __init__(self, width, height, caption):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill(BLUE )
            self.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def update(self):
        pass

    def drawLines(self):
        pygame.draw.lines(self.screen, GREEN, False, [(50, 50), (50, self.height - 50)], 5)
        pygame.draw.lines(self.screen, GREEN, False, [(48, 50), (self.width - 48,50)], 5)
        pygame.draw.lines(self.screen, GREEN, False, [(self.width - 50, 50), (self.width - 50, self.height - 50)], 5)
        pygame.draw.lines(self.screen, GREEN, False, [(self.width - 48, self.height - 50), (48, self.height - 50)], 5)
class CustomerWindow(Window):
    def __init__(self, parent,name=""):
        super().__init__(parent.width, parent.height, "Гра")
        self.parent = parent
        self.active = False
        self.current_encoding = 'utf-8'
        self.scoreText = ""
        self.customer_score=0
        self.customer_name=name
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def update(self):
        
        exit_button = Button(self.width / 2 - 150, self.height / 2 + 200, 300, 50,LIME, "Повернутися в меню")
        play_button = Button(self.width / 2 - 150, self.height / 2 -40, 300, 50,GREEN, "Грати")
        info_button = Button(self.width / 2 - 150, self.height / 2 +120, 300, 50,LIME, "Інформація")
        setting_button = Button(self.width / 2 - 150, self.height / 2 +40, 300, 50,LIME, "Налаштування")
        font = pygame.font.Font(None, 52)
        self.find_record()
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            self.screen.fill(BLUE)
            self.drawLines()
            font = pygame.font.Font(None, 80)
            prompt_text = font.render("Вікторина", True, MAGENTA)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 200))
            self.screen.blit(prompt_text, prompt_rect)
            font = pygame.font.Font(None, 36)
            prompt_text = font.render(f"Вітаю {self.customer_name} !!!", True, YELLOW)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 120))
            self.screen.blit(prompt_text, prompt_rect)
            prompt_text = font.render(f"Ваш виграш : {self.customer_score} coins", True, YELLOW)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 80))
            self.screen.blit(prompt_text, prompt_rect)
        
            exit_button.draw(self.screen)
            play_button.draw(self.screen)
            setting_button.draw(self.screen)
            info_button.draw(self.screen)
            pygame.display.flip()

    def find_record(self):
        nameFind = False
        with open("records.txt", "r", encoding=self.current_encoding) as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith("Name:"):
                    if((line.replace("Name:", "").strip().lower()) == self.customer_name.lower()):
                        nameFind = True
                if line.startswith("Score:") and nameFind:
                    self.customer_score = line.replace("Score:", "").strip().lower()
                    break

class InfoWindow(Window):
    def __init__(self, parent,name=""):
        super().__init__(parent.width, parent.height, "Гра")
        self.parent = parent
        self.active = False
        self.current_encoding = 'utf-8'
        self.scoreText = ""
        self.customer_score=0
        self.customer_name=name
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def update(self):
        
        exit_button = Button(self.width / 2 - 150, self.height / 2 + 200, 300, 50,LIME, "Повернутися в меню")
        play_button = Button(self.width / 2 - 150, self.height / 2 -40, 300, 50,GREEN, "Грати")
        info_button = Button(self.width / 2 - 150, self.height / 2 +120, 300, 50,LIME, "Інформація")
        setting_button = Button(self.width / 2 - 150, self.height / 2 +40, 300, 50,LIME, "Налаштування")
        font = pygame.font.Font(None, 52)
        self.find_record()
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            self.screen.fill(BLUE)
            self.drawLines()
            font = pygame.font.Font(None, 80)
            prompt_text = font.render("Вікторина", True, MAGENTA)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 200))
            self.screen.blit(prompt_text, prompt_rect)
            font = pygame.font.Font(None, 36)
            prompt_text = font.render(f"Вітаю {self.customer_name} !!!", True, YELLOW)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 120))
            self.screen.blit(prompt_text, prompt_rect)
            prompt_text = font.render(f"Ваш виграш : {self.customer_score} coins", True, YELLOW)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 80))
            self.screen.blit(prompt_text, prompt_rect)
        
            exit_button.draw(self.screen)
            play_button.draw(self.screen)
            setting_button.draw(self.screen)
            info_button.draw(self.screen)
            pygame.display.flip()

    def find_record(self):
        nameFind = False
        with open("records.txt", "r", encoding=self.current_encoding) as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith("Name:"):
                    if((line.replace("Name:", "").strip().lower()) == self.customer_name.lower()):
                        nameFind = True
                if line.startswith("Score:") and nameFind:
                    self.customer_score = line.replace("Score:", "").strip().lower()
                    break

class SettingWindow(Window):
    def __init__(self, parent,name=""):
        super().__init__(parent.width, parent.height, "Гра")
        self.parent = parent
        self.active = False
        self.current_encoding = 'utf-8'
        self.scoreText = ""
        self.customer_score=0
        self.customer_name=name
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def update(self):
        
        exit_button = Button(self.width / 2 - 150, self.height / 2 + 200, 300, 50,LIME, "Повернутися в меню")
        play_button = Button(self.width / 2 - 150, self.height / 2 -40, 300, 50,GREEN, "Грати")
        info_button = Button(self.width / 2 - 150, self.height / 2 +120, 300, 50,LIME, "Інформація")
        setting_button = Button(self.width / 2 - 150, self.height / 2 +40, 300, 50,LIME, "Налаштування")
        font = pygame.font.Font(None, 52)
        self.find_record()
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            self.screen.fill(BLUE)
            self.drawLines()
            font = pygame.font.Font(None, 80)
            prompt_text = font.render("Вікторина", True, MAGENTA)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 200))
            self.screen.blit(prompt_text, prompt_rect)
            font = pygame.font.Font(None, 36)
            prompt_text = font.render(f"Вітаю {self.customer_name} !!!", True, YELLOW)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 120))
            self.screen.blit(prompt_text, prompt_rect)
            prompt_text = font.render(f"Ваш виграш : {self.customer_score} coins", True, YELLOW)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 80))
            self.screen.blit(prompt_text, prompt_rect)
        
            exit_button.draw(self.screen)
            play_button.draw(self.screen)
            setting_button.draw(self.screen)
            info_button.draw(self.screen)
            pygame.display.flip()

    def find_record(self):
        nameFind = False
        with open("records.txt", "r", encoding=self.current_encoding) as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith("Name:"):
                    if((line.replace("Name:", "").strip().lower()) == self.customer_name.lower()):
                        nameFind = True
                if line.startswith("Score:") and nameFind:
                    self.customer_score = line.replace("Score:", "").strip().lower()
                    break

class PlayWindow(Window):
    def __init__(self, parent,name=""):
        super().__init__(parent.width, parent.height, "Гра")
        self.parent = parent
        self.active = False
        self.current_encoding = 'utf-8'
        self.scoreText = ""
        self.customer_score=0
        self.customer_name=name
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def update(self):
        
        exit_button = Button(self.width / 2 - 150, self.height / 2 + 200, 300, 50,LIME, "Повернутися в меню")
        play_button = Button(self.width / 2 - 150, self.height / 2 -40, 300, 50,GREEN, "Грати")
        info_button = Button(self.width / 2 - 150, self.height / 2 +120, 300, 50,LIME, "Інформація")
        setting_button = Button(self.width / 2 - 150, self.height / 2 +40, 300, 50,LIME, "Налаштування")
        font = pygame.font.Font(None, 52)
        self.find_record()
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            self.screen.fill(BLUE)
            self.drawLines()
            font = pygame.font.Font(None, 80)
            prompt_text = font.render("Вікторина", True, MAGENTA)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 200))
            self.screen.blit(prompt_text, prompt_rect)
            font = pygame.font.Font(None, 36)
            prompt_text = font.render(f"Вітаю {self.customer_name} !!!", True, YELLOW)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 120))
            self.screen.blit(prompt_text, prompt_rect)
            prompt_text = font.render(f"Ваш виграш : {self.customer_score} coins", True, YELLOW)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 80))
            self.screen.blit(prompt_text, prompt_rect)
        
            exit_button.draw(self.screen)
            play_button.draw(self.screen)
            setting_button.draw(self.screen)
            info_button.draw(self.screen)
            pygame.display.flip()

    def find_record(self):
        nameFind = False
        with open("records.txt", "r", encoding=self.current_encoding) as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith("Name:"):
                    if((line.replace("Name:", "").strip().lower()) == self.customer_name.lower()):
                        nameFind = True
                if line.startswith("Score:") and nameFind:
                    self.customer_score = line.replace("Score:", "").strip().lower()
                    break


class RegistrationWindow(Window):
    def __init__(self, parent):
        super().__init__(parent.width, parent.height, "Реєстрація")
        self.parent = parent
        self.input_text = ""
        self.input_rect = pygame.Rect(self.width / 2 - 200, self.height / 2, 400, 30)
        self.active = False
        self.current_encoding = 'utf-8'
        self.errorText = ""
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    self.handle_event(event)

            self.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

    def update(self):
        exit_button = Button(self.width / 2 - 150, self.height / 2 + 100, 300, 50,GREEN, "Повернутися в меню")
        font = pygame.font.Font(None, 36)
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.errorText = ""
                    if event.key == pygame.K_RETURN:
                        if (self.check_name()):
                            self.save_record()
                            self.active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 12:
                            self.input_text += event.unicode
                        elif len(self.input_text) == 12:
                            self.errorText = "Довжина імені не більше 12 символів"
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            self.screen.fill(BLUE)
            prompt_text = font.render("Введіть ім'я :", True, YELLOW)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 50))
            self.screen.blit(prompt_text, prompt_rect)
            pygame.draw.rect(self.screen, CYAN, self.input_rect, 2)
            text_surface = font.render(self.input_text, True,MAGENTA)
            text_rect = text_surface.get_rect(center=self.input_rect.center)
            self.screen.blit(text_surface, text_rect)
            if self.errorText != "":
                error_text = font.render(self.errorText, True, RED)
                error_rect = error_text.get_rect(center=(self.width / 2, self.height / 2 + 50))
                self.screen.blit(error_text, error_rect)
            exit_button.draw(self.screen)
            pygame.display.flip()
        self.input_text=""
        self.errorText = ""

    def save_record(self):
        with open("records.txt", "a", encoding=self.current_encoding) as file:
            record = f"Name: {self.input_text}\nScore: 0\n"  # Замените "ваш_рекорд" на реальное значение рекорда
            file.write(record)
    def is_valid_name(self,name):
        return re.match(r'^[a-zA-Zа-яА-Я]+$', name) is not None
    def check_name(self):
        if (len(self.input_text)==0 or not self.is_valid_name(self.input_text)):
            self.errorText = "Недопустиме ім'я"
            return False
        with open("records.txt", 'r', encoding=self.current_encoding) as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    if line.startswith("Name:"):
                        nameA = line.replace("Name:", "").strip().lower()
                        if (nameA == self.input_text.lower()):
                            self.errorText = "Дане ім'я вже використовується"
                            return False
            return True
class LoginWindow(Window):
    def __init__(self, parent):
        super().__init__(parent.width, parent.height, "Вхід")
        self.parent = parent
        self.input_text = ""
        self.input_rect = pygame.Rect(self.width / 2 - 200, self.height / 2, 400, 30)
        self.active = False
        self.current_encoding = 'utf-8'
        self.errorText = ""
        self.customer_window = CustomerWindow(parent,self.input_text)
        
    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    self.handle_event(event)

            self.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

    def update(self):
        font = pygame.font.Font(None, 36)
        exit_button = Button(self.width / 2 - 150, self.height / 2 + 100, 300, 50,GREEN, "Повернутися в меню")

        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.errorText = ""
                    if event.key == pygame.K_RETURN:
                        if self.check_name():
                            self.customer_window.active = True
                            self.customer_window.customer_name = self.input_text
                            self.customer_window.update()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if len(self.input_text) < 12:
                            self.input_text += event.unicode
                        elif len(self.input_text) == 12:
                            self.errorText = "Довжина імені не більше 12 символів"
            if exit_button.is_clicked():
                self.running = False
                self.active = False
                break
            self.screen.fill(BLUE)
            prompt_text = font.render("Введіть ім'я :", True, YELLOW)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 50))
            self.screen.blit(prompt_text, prompt_rect)
            pygame.draw.rect(self.screen, CYAN, self.input_rect, 2)
            text_surface = font.render(self.input_text, True, MAGENTA)
            text_rect = text_surface.get_rect(center=self.input_rect.center)
            self.screen.blit(text_surface, text_rect)
            if self.errorText != "":
                error_text = font.render(self.errorText, True, RED)
                error_rect = error_text.get_rect(center=(self.width / 2, self.height / 2 + 50))
                self.screen.blit(error_text, error_rect)
            exit_button.draw(self.screen)
            
            pygame.display.flip()

        self.input_text = ""
        self.errorText = ""


    def check_name(self):
        
        with open("records.txt", 'r', encoding=self.current_encoding) as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    if line.startswith("Name:"):
                        nameA = line.replace("Name:", "").strip().lower()
                        if (nameA == self.input_text.lower()):
                            return True
            self.errorText = "Дане ім'я не використовується (Зареєструйтеся)"
            return False
class MainMenu(Window):
        def __init__(self):
            super().__init__(1200, 700, "Головне меню")
            self.login_button = Button(self.width / 2 - 100, self.height / 2 - 50, 200, 50,BLUE , "Ввійти")
            self.registration_button = Button(self.width / 2 - 100, self.height / 2 + 50, 200, 50, BLUE , "Реєстрація")
            self.registration_window = RegistrationWindow(self)
            self.login_window = LoginWindow(self)

        def update(self):
            font = pygame.font.Font(None, 90)
            self.drawLines()
            prompt_text = font.render("Вікторина", True,MAGENTA )
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 200))
            self.screen.blit(prompt_text, prompt_rect)
            self.login_button.draw(self.screen)
            self.registration_button.draw(self.screen)
            if self.registration_window.active:
                self.registration_window.update()
            if self.login_window.active:
                self.login_window.update()

            if self.login_button.is_clicked():
                self.login_window.active = True
            elif self.registration_button.is_clicked():
                self.registration_window.active = True

def main():
    main_menu = MainMenu()
    main_menu.run()

if __name__ == "__main__":
    main()
