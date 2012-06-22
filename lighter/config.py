import defaultdict

screen_to_channels = {
    'test': ['marley', 'consumer'],
}

channel_to_screens = defaultdict(list)
for k, vs in screen_to_channels.iteritems():
    for v in vs:
        channel_to_screens[v].append(k)

wick_daemons = {
	'test': '10.10.6.88:5000'
}
