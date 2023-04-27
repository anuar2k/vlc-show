#!/usr/bin/env python3

import sys, vlc, time, argparse, threading

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

	finished_playing_sem = threading.Semaphore(0)

	inst = vlc.Instance()
	player = inst.media_player_new()
	player.event_manager().event_attach(
		vlc.EventType.MediaPlayerEndReached,
		lambda _: finished_playing_sem.release()
	)

	media_lists = [
		[inst.media_new(mrl) for mrl in mrl_set]
		for mrl_set
		in args.mrl_sets
	]

	while True:
		for i, media_list in enumerate(media_lists):
			print(f'Playing media list no {i}')

			for media in media_list:
				player.set_media(media)
				player.play()
				finished_playing_sem.acquire()
				print('finished playing, going to next material')
