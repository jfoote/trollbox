# trollbox

Trollbox enables quick storage, tagging, and retrieval of images for the web. 

![example](https://raw.githubusercontent.com/jfoote/trollbox/master/trollbox/test/data/1/images/example.gif?token=AB-eizPbdrW2ZcP5atUXRQvQMvVYHwl9ks5UoxMYwA%3D%3D)

Trollbox allows users to download, tag, and search for images quickly. The bold can run the app as root to enable instantaneous search via a glorified keylogger (please [understand how this works and the associated risks](https://github.com/jfoote/trollbox/blob/master/trollbox/wordlogger/__init__.py) if you choose to enable it).

## About

This is a toy app that I developed as part of some ongoing software/security research. The primary function of this project is to act as a test bed for some HCI data collection and experimentation. The development stack was chosen for excessive (and perhaps unfortunate) familiarity, not optimality, as the app istelf is not the focus of the research. 

The idea for trollbox came from a concept of "thinking in gifs," which I've found to be a key skill for effective trolling of friends and colleagues in IRC, Slack, etc. :) 

## Requirements 

OSX is the only supported operating system at this time, though the development technologies used (Python, PySide, Qt4.8, C) should allow for porting. Just add elbow grease.

Trollbox depends on PySide. See [the documentation](https://pypi.python.org/pypi/PySide) for up-to-date instructions on installing it.

```
$ brew install qt
$ pip install -U PySide
$ pyside_postinstall.py -install
```

`pip install nose` is recommended for testing.

## Usage

Run Trollbox from its local directory. Such polished.

```
$ ./trollbox.py
```

Or, to enable wordlogging:

```
$ sudo ./trollbox.py
```

**Use at your own risk**

## TODO

These will probably never happen. But maybe.

- [ ] Perform richer semantic analysis of input
- [ ] Add "import from web" feature
- [ ] Port to Linux
- [ ] Port to Windows
- [ ] Automatically search online image resources
    - imgur
    - flickr
    - https://www.mashape.com/imagesearcher/camfind#!documentation
    - https://support.google.com/websearch/answer/1325808?hl=en
    - https://www.tineye.com/
- [ ] Add support for sharing trollboxes

## Development

Trollbox is a work in progress. If you actually install and use the app, please file any bugs in the Issue Tracker.

## Other Notes

If you end up using Trollbox please [let me know what you think](mailto:jmfoote@loyola.edu). Happy trolling...

```
Jonathan Foote
jmfoote@loyola.edu
23 Dec 2014
```
