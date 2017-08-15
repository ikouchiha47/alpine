### Alpine

Simple music player, plays music with gsstreamer. (And I dont like ituning)

![Screenshot](https://github.com/argentum47/alpine/blob/master/screenshot.jpg "Alpine on mac")

### Usage

- run from cli, either provide a Music directory, or a playlist file which has paths separated by new lines
- if lines separated by `\r\n` may god be with you
- `python2.7 main.py --dir ~/List ~/Of ~/Dirs` , or
- `python main.py --playlist ~/playlist_file`
- having done that once, you can just run the main.py without any cli args

### Install stuff for devel

- Install `gstreamer`, `gst-plugins-base`, `gst-plugins-good`, `gst-plugins-bad`, `gst-plugins-ugly`, `gst-ffmpeg` or `gst-libav`
- Have pip and shit
- run pip install -r requirements.txt

I added an installer script to make an executable I guess, run `./installer` and check the `dist/` folder

#### TODO:

- [ ] Add a music list to click and play
