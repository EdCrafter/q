import pygame
import sys
import re
import math
import random

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
        self.background_image_main = pygame.image.load("img/mainBg.jpg").convert()

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
        self.play_window = PlayWindow(self)
        #self.settings_window = CustomerWindow(self,self.input_text)
        self.info_window =InfoWindow(self)
        self.last_click_time =0

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
        exit_button = Button(self.width / 2 - 150, self.height / 2 + 200, 300, 50,LIME, "Вихід")
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
            if pygame.time.get_ticks() - self.last_click_time > 1000: 
                if play_button.is_clicked():
                    self.play_window.active = True
                    self.play_window.update()
                if info_button.is_clicked():
                    infoText = ["","",
                    "Правила гри:","1.Потрібно правильно відповідати на питання",
                    "2.Виберіть варіант відповіді з 4 запропонованих",
                    "  Якщо відповідь правильна то ви заробляєте гроші й переходите далі",
                    "  Інакше покидаєте квіз із грошима",
                    "  Бажаю удачі!!!",
                    "Гра розроблена на pygame Жердєвом Е.С."]
                    self.info_window.act = True
                    self.info_window.text = infoText
                    self.info_window.update()
                if exit_button.is_clicked():
                    self.running = False
                    self.active = False
                    self.parent.running = False
                    self.parent.active = False
                    break
            self.screen.blit(self.background_image_main, (0, 0))
            self.drawLines()
            self.drawTitle()
            font = pygame.font.Font(None, 36)
            prompt_text = font.render(f"Вітаю {self.customer_name} !!!", True, PURPLE)
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
    def drawTitle(self):
        x = 525
        y=180
        pygame.draw.lines(self.screen, MAGENTA, False, [(x, y), (x, y-70)], 5)
        pygame.draw.lines(self.screen, MAGENTA, False, [(x,y-35), (x+30,y-70)], 6)
        pygame.draw.lines(self.screen, MAGENTA, False, [(x,y-35), (x+30,y)], 6)
        x+=50
        pygame.draw.lines(self.screen,YELLOW, False, [(x, y), (x, y-50)], 5)
        pygame.draw.arc(self.screen, YELLOW, (x-17,y-30,40,30),math.pi/2*3,math.pi/2, 5)  # Верхняя полукруглая часть
        pygame.draw.arc(self.screen, YELLOW, (x-12,y-50, 30, 20), math.pi/2*3,math.pi/2, 5)  # Нижняя полукруглая часть
        x+=50
        pygame.draw.lines(self.screen,  CYAN, False, [(x, y), (x, y-65)], 5)
        pygame.draw.circle(self.screen, CYAN, (x, y-80), 5)  
        x+=30
        pygame.draw.arc(self.screen, RED, (x-17,y-30,40,30),math.pi/2*3-0.3,math.pi/2, 5)  # Верхняя полукруглая часть
        pygame.draw.arc(self.screen, RED, (x-12,y-50, 30, 20), math.pi/2*3,math.pi/2, 5) 
       

class InfoWindow(Window):
    def __init__(self, parent,text=[""],color="PURPLE"):
        super().__init__(parent.width, parent.height, "Гра")
        self.parent = parent
        self.act = False
        self.text=text
        self.color = color
        
    def update(self):
        font = pygame.font.Font(None, 45)
        while self.act:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.act = False
            self.screen.fill(SILVER)
            y=200
            for strT in self.text:
                prompt_text = font.render(strT, True, self.color)
                prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - y))
                y-=50
                self.screen.blit(prompt_text, prompt_rect)
            self.drawLines()
            pygame.display.flip()

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
            self.screen.blit(self.background_image_main, (0, 0))
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
    def __init__(self,parent,language="ukrainian"):
        super().__init__(parent.width, parent.height, "Гра")
        self.parent = parent
        self.active = False
        self.current_encoding = 'utf-8'
        self.scoreText = ""
        self.customer_score=0
        self.language=language
        self.num_q=0
        self.last_click_time =0
        self.background_image = pygame.image.load("img/bg1.jpg").convert()
        self.money = [
            "500","1000","2000","3000","5000","7500","10000","12500",
            "15000","25000","50000","100000","250000","500000","1000000",
            ]
        self.info_window1 =InfoWindow(self)
        
    def update(self):
        pygame.time.delay(1000)
        easy_file = "questionsBasa/Ukrainian/easy_questions.txt"
        medium_file = "questionsBasa/Ukrainian/medium_questions.txt"
        hard_file = "questionsBasa/Ukrainian/hard_questions.txt"

        easy_questions = self.read_questions_from_file(easy_file)
        medium_questions = self.read_questions_from_file(medium_file)
        hard_questions = self.read_questions_from_file(hard_file)

        self.selected_questions = random.sample(easy_questions,5) + random.sample(medium_questions, 5) + random.sample(hard_questions, 5)
        score = self.ask_questions(self.selected_questions,self.language)
        while self.active:
            a_button = Button(self.width / 2 - 450, self.height / 2 -80, 400, 50,OLIVE, self.a_text)
            b_button = Button(self.width / 2 - 450, self.height / 2, 400, 50,PURPLE, self.b_text)
            c_button = Button(self.width / 2+50 , self.height / 2 -80, 400, 50,SILVER, self.c_text)
            d_button = Button(self.width / 2+50 , self.height / 2 , 400, 50,CYAN, self.d_text)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Проверка нажатия кнопок
            if pygame.time.get_ticks() - self.last_click_time > 1000: 
                if a_button.is_clicked():
                    self.user_answer = "a"
                    if self.check_ans() :
                        for i in range(3):
                            a_button = Button(self.width / 2 - 450, self.height / 2 -80, 400, 50,GREEN, self.a_text)
                            a_button.draw(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(100)
                            a_button = Button(self.width / 2 - 450, self.height / 2 -80, 400, 50,OLIVE, self.a_text)
                            a_button.draw(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(100)
                        self.customer_score = self.money[self.num_q]
                        self.num_q += 1
                        if self.check_win():
                            break
                        self.ask_questions(self.selected_questions,self.language)
                        self.last_click_time = pygame.time.get_ticks()
                    else : 
                        for i in range(3):
                            a_button = Button(self.width / 2 - 450, self.height / 2 -80, 400, 50,RED, self.a_text)
                            a_button.draw(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(100)
                            a_button = Button(self.width / 2 - 450, self.height / 2 -80, 400, 50,OLIVE, self.a_text)
                            a_button.draw(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(100)
                        self.lose()
                       
                elif b_button.is_clicked():
                    self.user_answer = "b"
                    if self.check_ans() :
                        for i in range(3):
                            b_button = Button(self.width / 2 - 450, self.height / 2, 400, 50,GREEN, self.b_text)
                            b_button.draw(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(100)
                            b_button = Button(self.width / 2 - 450, self.height / 2, 400, 50,PURPLE, self.b_text)
                            b_button.draw(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(100)
                        self.customer_score = self.money[self.num_q]
                        self.num_q += 1
                        if self.check_win():
                            break
                        self.ask_questions(self.selected_questions,self.language)
                        self.last_click_time = pygame.time.get_ticks()        
                elif c_button.is_clicked():
                    self.user_answer = "c"
                    if self.check_ans() :
                        for i in range(3):
                            c_button = Button(self.width / 2+50 , self.height / 2 -80, 400, 50,GREEN, self.c_text)
                            c_button.draw(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(100)
                            c_button = Button(self.width / 2+50 , self.height / 2 -80, 400, 50,GRAY, self.c_text)
                            c_button.draw(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(100)
                        self.customer_score = self.money[self.num_q]
                        self.num_q += 1
                        if self.check_win():
                            break
                        self.ask_questions(self.selected_questions,self.language)
                        self.last_click_time = pygame.time.get_ticks()
                elif d_button.is_clicked():
                    self.user_answer = "d"
                    if self.check_ans() :
                        for i in range(3):
                            d_button = Button(self.width / 2+50 , self.height / 2, 400, 50,GREEN, self.d_text)
                            d_button.draw(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(100)
                            d_button = Button(self.width / 2+50 , self.height / 2, 400, 50,CYAN, self.d_text)
                            d_button.draw(self.screen)
                            pygame.display.flip()
                            pygame.time.delay(100)
                        self.customer_score = self.money[self.num_q]
                        self.num_q += 1
                        if self.check_win():
                            break
                        self.ask_questions(self.selected_questions,self.language)
                        self.last_click_time = pygame.time.get_ticks()   

            self.screen.blit(self.background_image, (0, 0))
            self.drawLines()
            font = pygame.font.Font(None, 40)
            prompt_text = font.render(self.q_text, True, WHITE)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 200))
            self.screen.blit(prompt_text, prompt_rect)
            p_text = font.render(f"Ваш виграш : {self.customer_score} coins", True, YELLOW)
            p_rect = p_text.get_rect(center=(self.width / 2, self.height / 2 - 140))
            self.screen.blit(p_text, p_rect)
            self.drowMoney()
            a_button.draw(self.screen)
            b_button.draw(self.screen)
            c_button.draw(self.screen)
            d_button.draw(self.screen)
            pygame.display.flip()

    def lose(self):
        infoText = ["","",
            "Неправильна відповідь !!!","",
            f"Ваш виграш {self.customer_score}",
            "",
            "Приходьте ще !!!",]
        self.info_window1.act = True
        self.info_window1.text = infoText
        self.info_window1.color = RED
        self.info_window1.update()
        self.active=False
        self.num_q=0
        slef.writeScore()
        self.customer_score=0
        
    def writeScore(self):
        pass

    def check_ans(self):
        return self.user_answer == self.correct_answer
        
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
    def read_questions_from_file(self,file_name):
        current_encoding = 'utf-8'
        with open(file_name, 'r', encoding=current_encoding) as file:
            lines = file.readlines()
        questions = []
        current_question = None
        current_options = []
        for line in lines:
            line = line.strip()
            if line:
                if current_question is None:
                    current_question = line
                elif line.startswith("A.") or line.startswith("B.") or line.startswith("C.") or line.startswith("D."):
                    current_options.append(line)
                elif line.startswith("Answer:"):
                    correct_answer = line.replace("Answer:", "").strip().lower()
                    questions.append((current_question, current_options, correct_answer))
                    current_question = None
                    current_options = []
                elif line.startswith("Відповідь:"):
                    correct_answer = line.replace("Відповідь:", "").strip().lower()
                    questions.append((current_question, current_options, correct_answer))
                    current_question = None
                    current_options = []

        return questions

    def check_win(self):
        if self.num_q == 15:
            self.active = False
            self.parent.active = True
            self.parent.update()
            return True
        return False

    def ask_questions(self,questions,language):
        score = 0
        if self.language=="english":
            for i, (question, options, correct_answer) in enumerate(questions, 1):
                print(f"Question {i}: {question}")
                for option in options:
                    print(option)
                user_answer = input("Select your answer (A, B, C, or D): ").strip().lower()
                if user_answer == correct_answer:
                    print("Correct!\n")
                    score += 1
                else:
                    print(f"Wrong. The correct answer is: {correct_answer}\n")
        elif self.language=="ukrainian":
            j=self.num_q
            question=questions[j]
            self.q_text = question[0]
            i=1
            for option in question[1]:
                if (i==1):
                    self.a_text = option
                if (i==2):
                    self.b_text = option
                if (i==3):
                    self.c_text = option
                if (i==4):
                    self.d_text = option
                i+=1
            self.correct_answer = question[2]
                

        return score
    def drowMoney(self):
        x=270
        y=self.height-130
        for n in range (15):
            if n==self.num_q:
                font = pygame.font.Font(None, 40)
                color = YELLOW
            else:
                font = pygame.font.Font(None, 30)
                color = WHITE
            prompt_text = font.render(self.money[n], True, color)
            prompt_rect = prompt_text.get_rect(center=(x,y))
            rotated_text = pygame.transform.rotate(prompt_text, 90)
            rotated_rect = rotated_text.get_rect(center=prompt_rect.center)
            self.screen.blit(rotated_text, rotated_rect)
            x+=50

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
            self.screen.blit(self.background_image_main, (0, 0))
            font = pygame.font.Font(None, 70)
            prompt_text = font.render("Реєстрація", True, MAGENTA)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 200))
            self.screen.blit(prompt_text, prompt_rect)
            font = pygame.font.Font(None, 36)
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
        self.customer_window = CustomerWindow(self,self.input_text)
        
        
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
            self.screen.blit(self.background_image_main, (0, 0))
            font = pygame.font.Font(None, 70)
            prompt_text = font.render("Вхід", True, MAGENTA)
            prompt_rect = prompt_text.get_rect(center=(self.width / 2, self.height / 2 - 200))
            self.screen.blit(prompt_text, prompt_rect)
            font = pygame.font.Font(None, 36)
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
            self.screen.blit(self.background_image_main, (0, 0))
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
