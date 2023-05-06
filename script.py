#!/usr/bin/env python3


import sys, vlc, argparse
from .vlc_player import VlcPlayer

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='VLC Control')
	parser.add_argument(
		'--mrl-set',
		dest='mrl_sets',
		metavar='mrl',
		help='List of Media Resource Locators forming a set of resources',
		nargs='+',
		action='append',
		default=[]
	)

	args = parser.parse_args()
	if len(args.mrl_sets) == 0:
		print('No Media Resource Locator sets specified', file=sys.stderr)
		exit(1)

	for i, mrl_set in enumerate(args.mrl_sets):
		stringified_set = ', '.join(mrl_set)
		print(f'MRL set {i}: {stringified_set}')

	inst = vlc.Instance()

	media_lists = [
		[inst.media_new(mrl) for mrl in mrl_set]
		for mrl_set
		in args.mrl_sets
	]

	player = VlcPlayer(inst)

	while True:
		selection = input('Select next MRL set: ')
		if selection == '':
			print('Empty string, assuming exit')
			player.stop()
			break

		player.play(media_lists[int(selection)])
