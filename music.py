from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button

Config.set('graphics','width', '600')
Config.set('graphics','height', '100')

class MusicPlayer(Widget):
    nowPlaying = None
    songs = []

    def add_songs(self, songs):
        self.songs = songs
        self.index = 0

        if len(songs) > 0:
            self.nowPlaying = self.load_song(self.index) 

    def load_song(self, index):
        if index >= len(self.songs):
            self.index = 0
        elif index < 0:
            self.index = len(self.songs) - 1
        else:
            self.index = index

        return SoundLoader.load(self.songs[self.index].rstrip())

    def play_next(self):
        if not self.nowPlaying:
            return

        self.pause()
        self.nowPlaying.unload()
        self.nowPlaying = self.load_song(self.index + 1)
        self.play()
 
    def play_prev(self):
        if not self.nowPlaying:
            return

        self.pause()
        self.nowPlaying.unload()
        self.nowPlaying = self.load_song(self.index - 1)
        self.play()

    def play(self):
        self.nowPlaying.play()

    def pause(self):
        self.nowPlaying.stop()

    def set_volume(self, volume):
        self.volume = volume

        if self.nowPlaying:
            self.nowPlaying.volume = volume

    def callback(self, instance):
        command = self.get_id(instance)

        try:
            if command == "prev":
                self.play_prev()
            elif command == "next":
                self.play_next()
            elif command == "play" and self.nowPlaying:
                if self.nowPlaying.state == "stop":
                    self.play()
                else:
                    self.pause()
        except Exception as e:
            print e

    def get_id(self,  instance):
        for id, widget in self.ids.items():
            if widget.__self__ == instance:
                return id


class MusicApp(App):
    def build(self):
        with open('songs.txt', 'r') as f:
            lines = f.readlines()

        music = MusicPlayer()
        music.add_songs(lines)
        return music




