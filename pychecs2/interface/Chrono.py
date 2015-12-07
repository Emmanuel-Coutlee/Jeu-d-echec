from tkinter import *
import time

class StopWatch(Frame):
    """ Implements a stop watch frame widget. """
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.makeWidgets()
        self._start2 = 0.0
        self._elapsedtime2 = 0.0
        self._running2 = 0.0
        self.timestr2 = StringVar()
        self.makeWidgets2()
        self.chronoactif = 'blanc'



    def makeWidgets(self):
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=2, padx=2)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)

        self.timestr.set('%02d:%02d' % (minutes, seconds))

    def Start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def Stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):
        """ Reset the stopwatch. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)


    def makeWidgets2(self):
        l = Label(self, textvariable=self.timestr2)
        self._setTime2(self._elapsedtime2)
        l.pack(fill=X,expand=NO, pady=2, padx=2)

    def _update2(self):
        """ Update the label with elapsed time. """
        self._elapsedtime2 = time.time() - self._start2
        self._setTime2(self._elapsedtime2)
        self._timer = self.after(50, self._update2)

    def _setTime2(self, elap):
        """ Set the time string to Minutes:Seconds """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)

        self.timestr2.set('%02d:%02d' % (minutes, seconds))

    def Start2(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running2:
            self._start2 = time.time() - self._elapsedtime2
            self._update2()
            self._running2 = 1

    def Stop2(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running2:
            self.after_cancel(self._timer)
            self._elapsedtime2 = time.time() - self._start2
            self._setTime2(self._elapsedtime2)
            self._running2 = 0

    def Reset2(self):
        """ Reset the stopwatch. """
        self._star2t = time.time()
        self._elapsedtime2 = 0.0
        self._setTime2(self._elapsedtime2)

    def chronoactif(self):

        if self.Start == 'blanc':
           self.Stop2 = 'noir'


        elif self.Start2() == 'noir':
             self.Stop = 'blanc'




def main():
    root = Tk()
    sw = StopWatch(root)
    sw.pack(side=TOP)

    Button(root, text='Partir', command=sw.Start).pack(side=LEFT)
    Button(root, text='Arrêt', command=sw.Stop).pack(side=LEFT)
    Button(root, text='Recommencer', command=sw.Reset).pack(side=LEFT)
    Button(root, text='Quitter', command=root.quit).pack(side=LEFT)
    Button(root, text='Start', command=sw.Start2).pack(side=LEFT)
    Button(root, text='Stop', command=sw.Stop2).pack(side=LEFT)
    Button(root, text='Reset', command=sw.Reset2).pack(side=LEFT)
    Button(root, text='Chrono Actif', command = sw.chronoactif).pack(side=LEFT)


    root.mainloop()

if __name__ == '__main__':
    main()