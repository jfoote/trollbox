# trollbox

Trollbox enables quick storage, tagging, and retrieval of images from the web. 

![example](https://raw.githubusercontent.com/jfoote/trollbox/master/trollbox/test/data/1/images/example.gif?token=AB-eizPbdrW2ZcP5atUXRQvQMvVYHwl9ks5UoxMYwA%3D%3D)

Trollbox allows users to download, tag, and search for images quickly. The bold can run the app as root to enable instantaneous search via a glorified keylogger (please [understand how this works and the associated risks](https://github.com/jfoote/trollbox/blob/master/trollbox/wordlogger/__init__.py) if you choose to enable it). 

## About

This is a toy app that I developed as part of some ongoing software engineering and security research. The primary function of this project is to act as a test bed for some HCI data collection and experimentation. The development stack was chosen for excessive (and perhaps unfortunate) familiarity, not optimality, as the app istelf is not the focus of the research. 

The idea for Trollbox came from a concept of "thinking in gifs," which I've found to be a key skill for effective trolling of friends and colleagues in IRC, Slack, etc. :) 

## Requirements 

Trollbox works on OSX, Linux, and Windows. The keylogger isn't implemented for Linux or Windows yet, but everything else works.

Trollbox depends on PySide. See [the documentation](https://pypi.python.org/pypi/PySide) for up-to-date instructions on installing it. For example, on OSX:

```
$ brew install qt
$ pip install -U PySide
$ pyside_postinstall.py -install
```

And on ubuntu:

```
$ sudo apt-get install python-pyside
```

`pip install nose` is recommended for testing.

## Setup

To build the keylogger after cloning (OSX only):

``
pushd trollbox/wordlogger
gcc -framework ApplicationServices -o osx osx.c
popd
```

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

This app displays (i.e. processes) data from the internet, or any other network you are connected to. Proceed with caution. 

## TODO

These will probably never happen. But maybe.

- [ ] Port keylogger to Linux and Windows
- [ ] Add animation to UI
- [ ] Perform richer semantic analysis of input
- [ ] Add "import from web" feature
- [x] Port to Linux
- [x] Port to Windows
- [ ] Automatically search online image resources
    - imgur
    - flickr
    - replygif
    - etc
- [ ] Automatically suggest tags
    - https://www.mashape.com/imagesearcher/camfind#!documentation
    - https://support.google.com/websearch/answer/1325808?hl=en
    - https://www.tineye.com/
- [ ] Add support for sharing trollboxes
- [ ] Build the mobile version, become app store millionaire
- [ ] Build the web version, get bought by Google/Facebook/et. al.
- [ ] Wipe ass with hundos

## Development

Trollbox is a work in progress. If you actually install and use the app, please file any bugs in the Issue Tracker.

*On backing up, restoring, and sharing trollboxes:*

By default all user-specific data is stored in the `$HOME/.trollbox` directory. trollbox stores tags, URLs, and images paths in a simple JSON file at `$HOME/.trollbox/metadata.json`. Image files are named by the MD5 hash of their URL and stored in the `images` subdirectory. 

## Other Notes

If you end up using Trollbox please [let me know what you think](mailto:jmfoote@loyola.edu). Happy trolling...

```
Jonathan Foote
jmfoote@loyola.edu
23 Dec 2014
```
