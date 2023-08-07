from logic.handlers.base import BaseHandler


class CommandHandler(BaseHandler):
    def __init__(self, game_loop):
        super(CommandHandler, self).__init__(game_loop)


    def handle(self, event):
        pass