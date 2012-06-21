import config


class Screen(object):
    def __getitem__(self, name):
        if name in config.screen_list:
            return Command(screen=name)
        else:
            return Command(name)

class Command(object):
    def __init__(self, screen=None):
        self.screen = screen
        self.command = None

    def __getitem__(self, cmd):
        if not self.command and cmd in config.cmd_list:
            self.command = cmd
        return self

