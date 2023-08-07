from logic.handlers.base import BaseHandler


class InitialHandler(BaseHandler):
    def __init__(self, game_loop):
        super(InitialHandler, self).__init__(game_loop)


    def handle(self, event):
        super(InitialHandler, self).handle(event)