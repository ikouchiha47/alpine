from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
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

    def __init__(self, **kwargs):
        super(MusicPlayer, self).__init__(**kwargs)
        Window.size = (600, 400)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar':
            self.toggle()
        if keycode[1] == 'j':
            self.play(self.index + 1, self.isPlaying)
        elif keycode[1] == 'k':
            self.play(self.index - 1, self.isPlaying)
        elif keycode[1] == 'escape':
            self._keyboard.release()
            App.get_running_app().stop()

        return True

    def add_songs(self, songs):
        self.songs = songs
        self.index = 0

        for idx, song in enumerate(songs):
            def play_song(bt):
                self.play(int(bt.id), True)
    
            song_text = song.rstrip().rpartition('/')[-1]
            btn = Button(text=song_text, background_color=(0,0,0,0.2), size=(1200, 40), size_hint=(None, None))
            btn.text_size = (1100, None)
            btn.shorten = True
            btn.id = str(idx)
            btn.shorten_from = 'right'
            btn.bind(on_press=play_song)
            self.ids.scroll.add_widget(btn)

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
            ## gana khatam go to next song
            if self.isPlaying:
                self.play(self.index + 1, self.isPlaying)
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
            self.ids.play.source = "icons/pause.png"
            self.nowPlaying.play()

    def pause(self):
        self.isPlaying = False
        self.ids.play.source = "icons/play.png"
        self.nowPlaying.stop()

    def toggle(self):
        if self.isPlaying:
            self.pause()
        else:
            self.play(self.index, True)

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
                    self.play(self.index, True)
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
        with open('playlist.txt', 'r') as f:
            lines = f.readlines()

        music = MusicPlayer(size=(600, 100))
        music.add_songs(lines)

        return music




