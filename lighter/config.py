from collections import defaultdict

prefix_to_channels = {
    'test': ['marley', 'consumer'],
    'bomb': ['marley', 'consumer'],
}

channel_to_prefixes = defaultdict(list)
for k, vs in prefix_to_channels.iteritems():
    for v in vs:
        channel_to_prefixes[v].append(k)

# This is populated by requests from wicks to /register_prefix
wick_daemons = {
	#TODO remove
	'bomb': '10.10.6.88:5000'
}
