import vlc


class VLCPlayer:
    def __init__(self, path):
        # -self.player = vlc.Instance('--loop')
        self.media_player = vlc.MediaPlayer()
        self.media = vlc.Media(path)
        self.media_player.set_media(self.media)

    def is_playing(self):
        return self.media_player.is_playing() == 1

    def play(self):
        self.media_player.play()

    def next(self):
        self.media_player.next()

    def pause(self):
        # check if is playing
        if self.is_playing():
            self.media_player.pause()

    def previous(self):
        self.media_player.previous()

    def stop(self):
        self.media_player.stop()
