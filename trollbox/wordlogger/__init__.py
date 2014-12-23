from PySide.QtCore import QObject, Signal
from threading import Thread, Event
import subprocess, os, shlex

def get_wordlogger():
    # pick keylogger based on arch here
    return WordLogger()

class WordLogger(QObject):
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
        self.thread = Thread(target=self.log_keys).start()

    def stop(self):
        print "wordlogger stop"
        if not self.thread:
            self._stop.set()
            return 
        self.proc.kill()
        self._stop.set()

    def log_keys(self):
        print "log_keys entered"
        word = ""
        path = os.path.join(self.bin_dir, "osx")
        cmd = "sudo " + path
        print "cmd",cmd 
        self.proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
        while not self._stop.is_set():
            key = self.proc.stdout.readline().strip() # osx: proc killed upon CTRL-C
            print "got key '%s'" % key
            if key == "<Return>":
                print "got word", word
                self.wordEntered.emit(word)
                word = ""
                continue
            elif key == '': # proc exited/EOF
                break
            word += key
        print "keylogger exiting"
        self.proc.kill() # not necessary on osx
