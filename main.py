from os import listdir
from os.path import isfile, join
import argparse
from music import MusicApp
from shutil import copyfile

class Stuff:
    def __init__(self):
        hlpTxt = 'provide music directory, defaults ~/Music'
        parser = argparse.ArgumentParser()
        parser.add_argument('--dir', nargs='+', required=False, default=[], help=hlpTxt)
        parser.add_argument('--playlist', required=False, help='Path to playlist file')
        self.args = parser.parse_args()

    def run(self):
        paths = []

        if self.args.playlist:
            copyfile(self.args.playlist, "playlist.txt")
            return

        if len(self.args.dir) == 0:
            return

        for path in self.args.dir:
            filesindir = [path + "/" + f for f in listdir(path) if isfile(join(path, f)) and f.endswith(('.mp3', 'wav'))]
            paths.extend(filesindir)

        with open("playlist.txt", "w+") as file:
            for path in paths:
                file.write(path + "\n")



if __name__ == '__main__':
    s = Stuff()
    s.run()
    MusicApp().run()
