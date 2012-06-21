class Screen(object):
    __name__ = 'screen'

    def __getitem__(self, screen_alias):
        return Command(screen_alias)

class Command(object):
    __name__ = 'command'

    def __init__(self, screen_alias):
        self.screen_alias = screen_alias

    def __getitem__(self, command_alias):
        return "Command: {command} for screen {screen}".format(
            command=command_alias,
            screen=self.screen_alias
        )


