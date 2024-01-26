class ChromeCannotOpenError(Exception):
    def __init__(self):
        super().__init__('cannot open chrome')
