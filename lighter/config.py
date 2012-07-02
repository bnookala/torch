from collections import defaultdict

#     [ marley ] (lives on dev12)
#         |
#         | messages go from irc to internet
#         |
#     [ lighter ] (also lives on dev12)
#       / | \
#     /   |   \   (internet magic http dust)
#   ...   |   ...
#         |
#      [ wick ] (lives on a TV machine, has a 'prefix')
#        /|\
#         |    (connected to multiple browsers, indexed prefix1, prefix2, etc)
#         |
#     [ browser ]
#        /|\
#        tabs..

prefix_to_channels = {
    'menus': ['#chrome', '#consumer', '#menus'],
    'community': ['#community'],
    'cnsmra': ['#chrome', '#consumer'],
    'cnsmrb': ['#chrome', '#consumer'],
}

channel_to_prefixes = defaultdict(list)
for k, vs in prefix_to_channels.iteritems():
    for v in vs:
        channel_to_prefixes[v].append(k)

# This is populated by requests from wicks to /register_prefix
wick_daemons = {
}

nyanwinning = False
nyanwin_queue = []
