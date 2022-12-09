import pygame
import os
import datetime


class Button:
    def __init__(self, size, position, color=None, sprite=None):
        self.positioning = position
        self.size = size
        self.position = position
        self.color = color
        self.sprite = sprite
        if sprite:
            self.image = pygame.image.load(os.path.join(sprite))
            self.image = pygame.transform.scale(self.image, size)
            self.rect = self.image.get_rect(center=self.position)
            self.image_copy = self.image
        else:
            self.rect = None
        self.surface = None
        self.update_size()

    def update(self, app_state=None, input_state=None):
        if not self.sprite:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.surface.fill('#009adf')
            else:
                self.surface.fill(self.color)
        else:
            pass

    def update_size(self):
        window_width, window_height = pygame.display.get_window_size()
        if self.positioning == 'full_center':
            self.size = window_width, 100
            self.position = 0, 100
        elif self.positioning == 'half_center':
            self.size = window_width // 2, 100
            self.position = window_width // 2 - self.size[0] // 2, 300
        elif self.positioning == 'center':
            self.position = window_width // 2, window_height // 2

        self.surface = pygame.Surface(self.size)
        self.rect = self.surface.get_rect(center=self.position)
        self.surface.fill(self.color)

    def draw(self, screen):
        if self.sprite:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.surface, self.rect)


class StartButton(Button):
    def __init__(self, font_path, size, position, color):
        super().__init__(size, position, color)
        self.font_path = font_path
        self.to_draw = 'START'

    def update(self, app_state=None, input_state=None):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surface.fill('#009adf')
            color = 'white'
            if input_state.get_mouse_released():
                print(app_state.get_state())
                app_state.set_state('tickets_1')
                print(app_state.get_state())
        else:
            self.surface.fill(self.color)
            color = 'white'
        now = datetime.datetime.now()
        scale = now.second % 5 + 2
        self.font = pygame.font.Font(self.font_path, int(70 + scale**2))
        if app_state.get_language() == 'PL':
            self.to_draw = 'KUP BILETY'
        elif app_state.get_language() == 'GB':
            self.to_draw = 'BUY TICKETS'
        elif app_state.get_language() == 'DE':
            self.to_draw = 'TICKETS KAUFEN'
        elif app_state.get_language() == 'UA':
            self.to_draw = 'ПРИДБАТИ КВИТКИ'
        self.text = self.font.render(self.to_draw, 1, color)
        window_width, window_height = pygame.display.get_window_size()
        self.text_pos = self.text.get_rect(center=(window_width/2,
                                                   window_height/2))

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        screen.blit(self.text, self.text_pos)


class TopBar:
    def __init__(self, size, position, color):
        self.positioning = position
        self.size = size
        self.position = position
        self.color = color
        self.surface = None
        self.rect = None
        self.update_size()

    def update(self, app_state=None, input_state=None):
        pass

    def update_size(self):
        window_width, window_height = pygame.display.get_window_size()
        if self.positioning == 'full_top':
            self.size = window_width, 100
            self.position = 0, 0
        elif self.positioning == 'half_center':
            self.size = window_width // 2, 100
            self.position = window_width // 2 - self.size[0] // 2, 250

        self.surface = pygame.Surface(self.size)
        self.rect = self.surface.get_rect(topleft=self.position)
        self.surface.fill(self.color)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class Clock(Button):
    def __init__(self, font, size, position):
        self.position = position
        self.font = pygame.font.Font(font, size)
        self.text = None

    def update(self, app_state=None, input_state=None):
        now = datetime.datetime.now()
        hour = now.strftime("%H:%M")
        date = str(now.day) + '/' + str(now.month) + '/' + str(now.year)[2:]
        self.text = self.font.render(hour + ' '*4 + date,
                                     1, 'white')

    def draw(self, screen):
        screen.blit(self.text, self.position)


class ProgressBar(Button):

    def __init__(self, size, position, font, color=None, sprite=None):
        super().__init__(size, position, color, sprite)
        self.font = font
        self.font_size = 14
        self.state = 1
        self.spacing = 15
        # Rect(left, top, width, height)
        rect1 = (position[0], position[1],
                 size[0], size[1])
        rect2 = (position[0] + (size[0] + self.spacing), position[1],
                 size[0], size[1])
        rect3 = (position[0] + (size[0] + self.spacing) * 2, position[1],
                 size[0], size[1])
        rect4 = (position[0] + (size[0] + self.spacing) * 3, position[1],
                 size[0], size[1])
        self.rects = [rect1, rect2, rect3, rect4]
        self.state = 1
        self.font = pygame.font.Font(self.font, self.font_size)
        self.text = {}
        self.text['PL'] = ['TYP', 'BILETU',
                           'LICZBA', 'I ZNIŻKA',
                           'PODSUMOWANIE', 'ZAMÓWIENIA',
                           'METODA', 'PŁATNOŚCI']
        self.text['GB'] = ['TICKET', 'TYPE',
                           'COUNT AND', 'DISCOUNT',
                           'ORDER', 'SUMMARY',
                           'PAYMENT', 'METHOD']
        self.text['DE'] = ['ART DES', 'TICKETS',
                           'ANZAHL UND', 'RABATT',
                           'BESTELL-', 'ÜBERSICHT',
                           'METOZAHLUNGS-', 'METHODEDA']
        self.text['UA'] = ['ТИП', 'КВИТКА',
                           'КІЛЬКІСТЬ', 'ТА ЗНИЖКА',
                           'ПІДСУМОК', 'ЗАМОВЛЕННЯ',
                           'СПОСІБ', 'ОПЛАТИ']

    def update(self, app_state=None, input_state=None):
        if app_state.get_state() in ['start']:
            self.state = 0
        elif app_state.get_state() in ['tickets_1',
                                       'tickets_2',
                                       'tickets_3',
                                       'tickets_4']:
            self.state = 1
        elif app_state.get_state() in ['counts_discounts']:
            self.state = 2
        elif app_state.get_state() in ['summary']:
            self.state = 3
        elif app_state.get_state() in ['payment_method']:
            self.state = 4
        lang = app_state.get_language()
        self.to_draw = [self.font.render(line, 1,
                                         'white') for line in self.text[lang]]

    def draw(self, screen):
        if self.state != 0:
            for bar in range(4):
                if bar < self.state:
                    self.surface.set_alpha(255)
                else:
                    self.surface.set_alpha(60)
                screen.blit(self.to_draw[bar*2],
                            (self.position[0] + bar * (self.spacing +
                                                       self.size[0]),
                            self.position[1] - 1.9 * self.size[1]))
                screen.blit(self.to_draw[2*bar+1],
                            (self.position[0] + bar * (self.spacing +
                                                       self.size[0]),
                            self.position[1] - self.size[1]))
                screen.blit(self.surface, self.rects[bar])


class Flag(Button):

    def __init__(self, size, position, lang, color=None, sprite=None):
        super().__init__(size, position, color, sprite)
        self.lang = lang

    def update(self, app_state=None, input_state=None):
        if app_state.get_language() != self.lang:
            self.image.set_alpha(125)
        else:
            self.image.set_alpha(255)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if input_state.get_mouse_released():
                print(app_state.get_language(), end='->')
                app_state.set_language(self.lang)
                print(app_state.get_language())


class Ticket(Button):
    def __init__(self, font, size, position, color=None, sprite=None):
        super().__init__(size, position, color, sprite)
        self.position = position
        self.font = pygame.font.Font(font, 20)
        self.text = None

    def update(self, app_state=None, input_state=None):
        text = ['Zwykłe, pospieszne i nocne',
                'w strefie taryfowej: Sopotu albo Rumi',
                'albo gm. Kosakowo albo gm. Żukowo',
                'albo gm. Szemud albo gm. Wejherowo']

        self.text = [self.font.render(line, 1, 'white') for line in text]

    def draw(self, screen):
        for line in range(len(self.text)):
            screen.blit(self.text[line], (self.position[0],
                                          self.position[1] + line * 20))


class SwitchTickets(Button):
    def __init__(self, font_path, size, to_switch, position, color):
        super().__init__(size, position, color)
        self.font_path = font_path
        self.to_switch = to_switch

    def update(self, app_state=None, input_state=None):
        # Rect(left, top, width, height)
        if app_state.get_state() == self.to_switch:
            self.surface = pygame.Surface((self.size[0] * 1.1, self.size[1]))
            color = 'green'
        else:
            self.surface = pygame.Surface(self.size)
            color = 'white'
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surface.fill('#009adf')
            if input_state.get_mouse_released():
                print(app_state.get_state(), end='->')
                app_state.set_state(self.to_switch)
                print(app_state.get_state())
        else:
            self.surface.fill(self.color)
        self.font = pygame.font.Font(self.font_path, 40)
        self.text = self.font.render(self.to_switch, 1, color)
        self.text_pos = self.text.get_rect(center=self.position)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        screen.blit(self.text, self.text_pos)


class SwitchStep(Button):
    def __init__(self, font_path, size, forward_or_backward,
                 position, color):
        super().__init__(size, position, color)
        self.font_path = font_path
        self.forward_or_backward = forward_or_backward
        self.button_text = {}
        if self.forward_or_backward == 'forward':
            self.button_text['PL'] = 'DALEJ'
            self.button_text['GB'] = 'NEXT'
            self.button_text['DE'] = 'NÄCHSTE'
            self.button_text['UA'] = 'ДАЛІ'
        elif self.forward_or_backward == 'backward':
            self.button_text['PL'] = 'WSTECZ'
            self.button_text['GB'] = 'PREVIOUS'
            self.button_text['DE'] = 'ZURÜCK'
            self.button_text['UA'] = 'НАЗАД'

    def update(self, app_state=None, input_state=None):
        # Rect(left, top, width, height)
        color = 'white'
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surface.fill('#009adf')
            if input_state.get_mouse_released():
                print(app_state.get_state(), end='->')
                if self.forward_or_backward == 'forward':
                    if app_state.get_state() in ['tickets_1',
                                                 'tickets_2',
                                                 'tickets_3',
                                                 'tickets_4']:
                        to_switch = 'counts_discounts'
                    if app_state.get_state() in ['counts_discounts']:
                        to_switch = 'summary'
                    if app_state.get_state() in ['summary']:
                        to_switch = 'payment_method'
                elif self.forward_or_backward == 'backward':
                    if app_state.get_state() in ['tickets_1',
                                                 'tickets_2',
                                                 'tickets_3',
                                                 'tickets_4']:
                        to_switch = 'start'
                    if app_state.get_state() in ['counts_discounts']:
                        to_switch = 'tickets_1'
                    if app_state.get_state() in ['summary']:
                        to_switch = 'counts_discounts'
                    if app_state.get_state() in ['payment_method']:
                        to_switch = 'summary'
                app_state.set_state(to_switch)
                print(app_state.get_state())
        else:
            self.surface.fill(self.color)
        self.font = pygame.font.Font(self.font_path, 40)
        self.text = self.font.render(
            self.button_text[app_state.get_language()], 1, color)
        self.text_pos = self.text.get_rect(center=self.position)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        screen.blit(self.text, self.text_pos)
