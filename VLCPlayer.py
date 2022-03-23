import vlc


class VLCPlayer:
    def __init__(self, path):
        # -self.player = vlc.Instance('--loop')
        self.media_player = vlc.MediaPlayer()
        self.media = vlc.Media(path)
        self.media_player.set_media(self.media)

    def __del__(self):
        if self.is_playing():
            self.stop()

    def is_playing(self):
        return self.media_player.is_playing() == 1

    # Faccio partire la riproduzione del video 
    def play(self):
        self.media_player.play()

    def next(self):
        self.media_player.next()
    
    # Metto il video in pausa
    def pause(self):
        # Verifico che sta avvenendo la riproduzione 
        if self.is_playing():
            self.media_player.pause()

    def previous(self):
        self.media_player.previous()

    def stop(self):
        self.media_player.stop()

    def set_volume(self, volume):
        self.media_player.audio_set_volume(int(volume))

    def get_volume(self):
        return self.media_player.audio_get_volume()