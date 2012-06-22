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
        self.command_type = None

    def __getitem__(self, cmd):
        if not self.command and cmd in config.cmd_list:
            self.command = cmd
        return self

    def execute(self):
        pass

class Close(Command):
    def execute(self):
        pass

class Desc(Command):
    def execute(self):
        pass

class Info(Command):
    def execute(self):
        pass

class List(Command):
    def execute(self):
        pass

class Next(Command):
    def execute(self):
        pass

class Previous(Command):
    def execute(self):
        pass

class Tabs(Command):
    def execute(self):
        pass

class Refresh(Command):
    def execute(self):
        pass

class Restart(Command):
    def execute(self):
        pass

class Show(Command):
    def execute(self):
        pass
