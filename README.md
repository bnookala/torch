# torch

Remotely control Google Chrome instances via [Hubot][1].

## Setup

Torch has three parts: `hubot-scripts`, `lighter`, and one or more `wick`s. They communicate with one other via HTTP.

      [ hubot ] (lives on some server)
          |
          | messages go from irc to internet
          |
      [ lighter ] (lives on some server, possibly the same one)
        / | \
      /   |   \   (internet magic http dust)
    ...   |   ...
          |
       [ wick ] (lives on a TV machine, has a 'prefix')
         /|\
          |    (connected to multiple browser windows, indexed prefix1, prefix2, etc)
          |
      [ browser ]
         /|\
         tabs..

### hubot-scripts

1. Edit `hubot-scripts/torch.coffee` to set `LIGHTER_ADDRESS` to the host running `lighter`.
2. Add it to your hubot scripts directory.

### lighter

This is the central server which receives commands from hubot and sends them to the hosts running Chrome.

1. Install dependencies: `pip install -r lighter/requirements.txt`
2. Edit `lighter/config.py` to configure `prefix_to_channels`, a mapping from TV name prefix (defined in a wick instance's config) to a list of IRC channel names from which users are allowed to control it.
3. Run `python lighter/lighter.py`.

### wick

This is what you'll run on each computer that is connected to a TV/monitor you want to control remotely.

1. Install dependencies: `pip install -r wick/requirements.txt`
2. Edit `wick/config.py` to configure `screen_name_prefix` (prefix to use when naming the browser windows on this computer), `port` to run on, and `lighter_host` where lighter is running.
3. Run `python wick/wick.py`.

## Note

We wrote this in a day and a half during a hackathon. Some parts are more stable than others. `rotate` is known to have some quirks.

http://procatinator.com is a good site to use with the `fullscreen on` command.

[1]: http://hubot.github.com/
