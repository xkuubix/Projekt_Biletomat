import pygame
from gui_utils import Button, StartButton, TopBar, Clock, Flag, ProgressBar
from gui_utils import Ticket, SwitchTickets, SwitchStep
from states import ApplicationState, InputState

GAME_WIDTH, GAME_HEIGHT = 1280, 720
TITLE = "ZKM GDYNIA"

APP_STATES = ['start',
              'tickets_1', 'tickets_2',
              'ticket_3', 'tickets_4']


# -------------------------- DEBUG SIDE
DEBUG = False


def drawGrid(screen, grid_step):
    blockSize = grid_step   # Set the size of the grid block
    for x in range(0, GAME_WIDTH, blockSize):
        for y in range(0, GAME_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, 'white', rect, 1)

# -------------------------- <


APP_STATE = ApplicationState()
IN_STATE = InputState()


def init():
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT),
                                     flags=pygame.RESIZABLE)
    pygame.display.set_caption(TITLE)
    screen.fill("black")
    ui_objects = {}
    size = 80

    start_button = StartButton('Roboto-BoldCondensed.ttf',
                               size=(GAME_WIDTH//1.45, GAME_HEIGHT//4),
                               position=(GAME_WIDTH//2, GAME_HEIGHT//2),
                               color='#002ADF')
    ui_objects['start'] = [start_button]

    ticket_1 = Ticket('Roboto-BoldCondensed.ttf',
                      (size, size), (40, 120), color='white', sprite=None)
    asdf_button1 = Button((size, size), (400, 160), '#002ADF')
    asdf_button3 = Button((size, size), (400, 260), '#002ADF')
    asdf_button2 = Button((size, size), (400, 360), '#002ADF')
    asdf_button4 = Button((size, size), (400, 460), '#002ADF')
    asdf_button5 = Button((size, size), (400, 560), '#002ADF')
    ui_objects['tickets_1'] = [ticket_1, asdf_button1, asdf_button2,
                               asdf_button3, asdf_button4,
                               asdf_button5]
    sw_button_height = 100
    sw_button_width = 200
    sw_button_x = 1120

    to_tickets_1 = SwitchTickets('Roboto-BoldCondensed.ttf',
                                 size=(sw_button_width, sw_button_height),
                                 to_switch='tickets_1',
                                 position=(sw_button_x, 170),
                                 color='#002ADF')
    to_tickets_2 = SwitchTickets('Roboto-BoldCondensed.ttf',
                                 size=(sw_button_width, sw_button_height),
                                 to_switch='tickets_2',
                                 position=(sw_button_x, 290),
                                 color='#002ADF')
    to_tickets_3 = SwitchTickets('Roboto-BoldCondensed.ttf',
                                 size=(sw_button_width, sw_button_height),
                                 to_switch='tickets_3',
                                 position=(sw_button_x, 410),
                                 color='#002ADF')
    to_tickets_4 = SwitchTickets('Roboto-BoldCondensed.ttf',
                                 size=(sw_button_width, sw_button_height),
                                 to_switch='tickets_4',
                                 position=(sw_button_x, 530),
                                 color='#002ADF')
    ui_objects['tickets'] = [to_tickets_1,
                             to_tickets_2,
                             to_tickets_3,
                             to_tickets_4]

    forward_backward_butto_size = (200, 80)
    forward_button = SwitchStep('Roboto-BoldCondensed.ttf',
                                size=forward_backward_butto_size,
                                forward_or_backward='forward',
                                position=(1120, 640),
                                color='#002ADF')
    backward_button = SwitchStep('Roboto-BoldCondensed.ttf',
                                 size=forward_backward_butto_size,
                                 forward_or_backward='backward',
                                 position=(900, 640),
                                 color='#002ADF')
    ui_objects['steps'] = [forward_button, backward_button]

    logo = Button((100, 100), (50, 50), '#009adf', 'zkm.png')
    top_bar = TopBar((100, 100), 'full_top', '#009adf')
    top_bar_under_flags = TopBar((450, 100), (850, 0), '#002adf')
    clock = Clock('Roboto-BoldCondensed.ttf', 40, (130, 25))
    progress_bar = ProgressBar((90, 20), (430, 70),
                               'Roboto-BoldCondensed.ttf', 'green')
    pl_flag = Flag((100, 100), (920, 50), 'PL',
                   'black', 'poland-circular.png')
    gb_flag = Flag((100, 100), (1020, 50), 'GB',
                   'black', 'great-britain-circular.png')
    de_flag = Flag((100, 100), (1120, 50), 'DE',
                   'black', 'germany-circular.png')
    ua_flag = Flag((100, 100), (1220, 50), 'UA',
                   'black', 'ukraine-circular.png')
    ui_objects['top_bar'] = [top_bar, top_bar_under_flags,
                             logo, clock, progress_bar,
                             pl_flag, gb_flag, de_flag, ua_flag]
    return screen, ui_objects


def handle_events():
    IN_STATE.reset_mouse_released()
    IN_STATE.reset_mouse_pressed()
    for event in pygame.event.get():
        if event.type in [
            pygame.QUIT] or event.type in [
                pygame.KEYDOWN] and event.key in [
                    pygame.K_ESCAPE]:
            print('quit')
            pygame.display.quit()
            pygame.quit()
            raise SystemExit

        if event.type == pygame.MOUSEBUTTONDOWN:
            IN_STATE.set_mouse_pressed()
        elif event.type == pygame.MOUSEBUTTONUP:
            IN_STATE.set_mouse_released()


def run(screen, ui_objects):
    clock = pygame.time.Clock()
    while True:
        state = APP_STATE.get_state()
        if DEBUG:
            pygame.display.set_caption(state)
        else:
            pygame.display.set_caption('ZKM GDYNIA')

        handle_events()
        clock.tick(600)

        screen.fill('#00DFB5')
        [(ui_object.update(APP_STATE, IN_STATE),
          ui_object.draw(screen)) for ui_object in ui_objects['top_bar']]

        if state == 'start':
            [(ui_object.update(APP_STATE, IN_STATE),
             ui_object.draw(screen)) for ui_object in ui_objects[
                 APP_STATE.get_state()]]

        if state == 'tickets_1':
            [(ui_object.update(APP_STATE, IN_STATE),
             ui_object.draw(screen)) for ui_object in ui_objects[
                 APP_STATE.get_state()]]

        if state in ['tickets_1', 'tickets_2',
                     'tickets_3', 'tickets_4']:
            [(ui_object.update(APP_STATE, IN_STATE),
             ui_object.draw(screen)) for ui_object in ui_objects[
                 'tickets']]
        if state in ['tickets_1', 'tickets_2',
                     'tickets_3', 'tickets_4',
                     'counts_discounts',
                     'summary', 'payment_method']:
            [(ui_object.update(APP_STATE, IN_STATE),
             ui_object.draw(screen)) for ui_object in ui_objects[
                 'steps']]

        if DEBUG:
            drawGrid(screen, 20)
            print(pygame.mouse.get_pos())
        pygame.display.flip()


def main():
    pygame.init()
    game_objects = init()
    run(*game_objects)


if __name__ == '__main__':
    main()
