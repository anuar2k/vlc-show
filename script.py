#!/usr/bin/env python3

import sys, vlc, time

def main():
	if len(sys.argv) <= 1:
		print('Brak filmow', file=sys.stderr)
		return 1

	movies = sys.argv[1:]

	inst = vlc.Instance()
	player = inst.media_player_new()

	for movie in movies:
		media = inst.media_new(movie)
		player.set_media(media)
		player.play()
		time.sleep(2)
		player.pause()
		time.sleep(3)
		player.pause()
		time.sleep(9999)


if __name__ == '__main__':
	exit(main())
