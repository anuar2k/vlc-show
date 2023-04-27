#!/usr/bin/env python3

import sys, vlc, time, argparse

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
	list_player = inst.media_list_player_new()
	media_lists = [inst.media_list_new(mrl_set) for mrl_set in args.mrl_sets]

	while True:
		for i, media_list in enumerate(media_lists):
			print(f'Playing media list no {i} in 1 sec for 3 secs')
			# list_player.stop()

			list_player.set_media_list(media_list)
			time.sleep(1)

			list_player.play()
			list_player.set_pause(0)
			time.sleep(3)
			list_player.set_pause(1)
