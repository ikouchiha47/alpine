from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.clock import Clock

Config.set('graphics','width', '600')
Config.set('graphics','height', '100')

class MusicPlayer(Widget):
    nowPlaying = None
    event = None
    isPlaying = False
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


        song = self.songs[self.index].rstrip()
        self.ids.filename.text = song.rpartition('/')[-1]

        return SoundLoader.load(song)

    def update_progress_bar(self, dt):
        length = self.nowPlaying.length
        played = self.nowPlaying.get_pos()

        if self.nowPlaying.state == "stop":
            self.event.cancel()
            return

        self.ids.pb.value = (self.width) * (played / length)

    def play(self, index, shouldPlay=True):
        if not self.nowPlaying:
            return

        self.pause()
        self.nowPlaying.unload()
        self.nowPlaying = self.load_song(index)

        if self.event:
            self.event.cancel()

        self.event = Clock.schedule_interval(self.update_progress_bar, 1/25.)
        if shouldPlay:
            self.isPlaying = True
            self.nowPlaying.play()

    def pause(self):
        self.isPlaying = False
        self.nowPlaying.stop()

    def set_volume(self, volume):
        self.volume = volume

        if self.nowPlaying:
            self.nowPlaying.volume = volume

    def callback(self, instance):
        command = self.get_id(instance)

        try:
            if command == "prev":
                self.play(self.index - 1, self.isPlaying)
            elif command == "next":
                self.play(self.index + 1, self.isPlaying)
            elif command == "play" and self.nowPlaying:
                if self.nowPlaying.state == "stop":
                    self.ids.play.source = "icons/pause.png"
                    self.play(self.index, True)
                else:
                    self.ids.play.source = "icons/play.png"
                    self.pause()
        except Exception as e:
            print e

    def get_id(self,  instance):
        for id, widget in self.ids.items():
            if widget.__self__ == instance:
                return id


class MusicApp(App):
    def build(self):

        with open('playlist.txt', 'r') as f:
            lines = f.readlines()

        music = MusicPlayer()
        music.add_songs(lines)
        return music




