from PySide.QtCore import QObject, Signal
from threading import Thread, Event
import subprocess, os, shlex, string, sys

def get_wordlogger():
    if "darwin" in sys.platform.lower():
        return WordLogger()
    print "WordLogger not implemented for", sys.platform.lower()
    return None

class WordLogger(QObject):
    '''
    Emits wordEntered when a word has been detected. Requires root because
    it's a keylogger. Use with caution.
    '''
    wordEntered = Signal(str)

    def __init__(self, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        
        self._stop = Event()
        self._stop.set()
        self.thread = None
        self.proc = None
        self.bin_dir = os.path.dirname(os.path.realpath(__file__)) 
        print "bin_dir", self.bin_dir

    def is_active(self):
        return not self._stop.is_set()

    def start(self):
        print "wordlogger start"
        self._stop.clear()
        self.thread = Thread(target=self.log_keys)
        self.thread.daemon = True # handle abrupt application exit
        self.thread.start()

    def stop(self):
        print "wordlogger stop"
        if not self.thread:
            self._stop.set()
            return 
        self.proc.kill()
        self._stop.set()

    def log_keys(self):
        from collections import deque
        # known issue: key combos result in extra letters on words
        # ... but NP, doesn't have to be perfect.
        print "log_keys entered"
        words = deque(maxlen=3)
        word = ""
        path = os.path.join(self.bin_dir, "osx")
        cmd = path
        print "cmd",cmd 
        self.proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
        while not self._stop.is_set():
            key = self.proc.stdout.readline().strip() # osx: proc killed upon CTRL-C
            #print "got key '%s'" % key
            if key == "<Delete>":
                # some minor support for typos
                if len(word) > 1:
                    word = word[:-1]
            elif (key in string.punctuation) or len(key) > 1: # some other non-keystroke
                word = filter(str.isalnum, word)
                if len(word) > 0:
                    #print "got word", word
                    words.append(word.strip())
                    #self.wordEntered.emit(word.strip())
                    self.wordEntered.emit(" ".join(words))
                    word = ""
            elif key == '': # proc exited/EOF
                break
            else:
                word += key
        print "keylogger thread exiting"
        self.proc.kill() 
