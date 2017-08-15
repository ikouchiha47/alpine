from os import listdir
from os.path import isfile, join
import argparse
from music import MusicApp


class Stuff:
    def __init__(self):
        hlpTxt = 'provide music directory, defaults ~/Music'
        parser = argparse.ArgumentParser()
        parser.add_argument('--dir', nargs='+', required=False, default=[], help=hlpTxt)
        args = parser.parse_args()
        self.dirs = args.dir

    def run(self):
        paths = []
        for path in self.dirs:
            filesindir = [path + "/" + f for f in listdir(path) if isfile(join(path, f)) and f.endswith(('.mp3', 'wav'))]
            paths.extend(filesindir)

        with open("songs.txt", "w+") as file:
            for path in paths:
                file.write(path + "\n")

        MusicApp().run()


if __name__ == '__main__':
    s = Stuff()
    s.run()
