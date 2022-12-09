class ApplicationState():
    def __init__(self) -> None:
        self.state = 'start'
        self.language = 'PL'

    def get_state(self):
        return self.state

    def set_state(self, setter):
        self.state = setter

    def get_language(self):
        return self.language

    def set_language(self, lang):
        if lang in ['PL', 'GB', 'DE', 'UA']:
            self.language = lang
        else:
            raise 'Invalid language specified.'


class InputState():
    def __init__(self) -> None:
        self.mouse_released = None
        self.mouse_pressed = None

    # ----- released
    def get_mouse_released(self):
        return self.mouse_released

    def set_mouse_released(self):
        self.mouse_released = True

    def reset_mouse_released(self):
        self.mouse_released = False

    # ----- pressed
    def get_mouse_pressed(self):
        return self.mouse_pressed

    def set_mouse_pressed(self):
        self.mouse_pressed = True

    def reset_mouse_pressed(self):
        self.mouse_pressed = False
