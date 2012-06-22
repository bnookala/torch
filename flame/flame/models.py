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

    def __getitem__(self, cmd):
        if cmd in config.cmd_list:
            return command_types[cmd](screen=self.screen)

    def execute(self):
        """To be implemented by the subclasses"""
        pass

class Close(Command):
    def execute(self):
        pass

class Desc(Command):
    def execute(self):
        pass

class Info(Command):
    def execute(self):
        print 'test'

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

command_types = {
    'close': Close,
    'desc': Desc,
    'info': Info,
    'list': List,
    'next': Next,
    'previous': Previous,
    'tabs': Tabs,
    'refresh': Refresh,
    'restart': Restart,
    'show': Show,
}


