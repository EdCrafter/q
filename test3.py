import pygame
import sys

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
            self.screen.fill(CYAN)
            self.update()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def update(self):
        pass

class RegistrationWindow(Window):
    def __init__(self, parent):
        super().__init__(parent.width, parent.height, "Реєстрація")
        self.parent = parent
        self.input_text = ""
        self.input_rect = pygame.Rect(self.width / 2 - 100, self.height / 2, 200, 30)
        self.active = False
        
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
        font = pygame.font.Font(None, 36)
        while self.active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

            self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, WHITE, self.input_rect, 2)
            text_surface = font.render(self.input_text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.input_rect.center)
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()


    def switch_to_parent(self):
        self.active = False
        self.parent.active = True

def main():
    class MainMenu(Window):
        def __init__(self):
            super().__init__(600, 400, "Головне меню")
            self.login_button = Button(self.width / 2 - 100, self.height / 2 - 50, 200, 50,CYAN , "Ввійти")
            self.registration_button = Button(self.width / 2 - 100, self.height / 2 + 50, 200, 50, CYAN, "Реєстрація")
            self.registration_window = RegistrationWindow(self)

        def update(self):
            self.login_button.draw(self.screen)
            self.registration_button.draw(self.screen)
            if self.registration_window.active:
                self.registration_window.update()

            if self.login_button.is_clicked():
                pass  # Обробка натискання кнопки "Ввійти"
            elif self.registration_button.is_clicked():
                self.registration_window.active = True

    main_menu = MainMenu()
    main_menu.run()

if __name__ == "__main__":
    main()
