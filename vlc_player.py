import threading, vlc, queue

class VlcPlayer:
    def __init__(self, vlc_inst):
        self.inst = vlc_inst
        self.player = self.inst.media_player_new()

        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._thread_entrypoint)
        self.medias = []

        self.action_handlers = {
            'play': self._handle_play,
            'next': self._handle_next
        }
        self.player.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached,
            lambda _: self.queue.put(('next', None))
        )

        self.thread.start()

    def _thread_entrypoint(self):
        while True:
            action, args = self.queue.get()
            if action == 'stop':
                return

            self.action_handlers[action](args)

    def _handle_play(self, args):
        self.medias = args.copy()
        self.queue.put(('next', None))

    def _handle_next(self, args):
        if len(self.medias) > 0:
            next_media = self.medias.pop(0)
            self.player.set_media(next_media)
            self.player.play()

    def play(self, medias):
        self.queue.put(('play', medias))

    def stop(self):
        self.queue.put(('stop', None))
        self.thread.join()
