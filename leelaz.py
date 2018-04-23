import subprocess
import sys
import os
#import signal
import random
from threading import Thread
#import ctypes

##process = subprocess.Popen(
##    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
##)
##
##while True:
##    out = process.stdout.read(1)
##    if out == b'' and process.poll() != None:
##        break
##    if out != b'':
##        sys.stdout.write(out.decode('utf8'))
##        sys.stdout.flush()


##    p.stdin.close()



##n = 0
##for line in iter(p.stdout.readline, b''):
##    print("# " + line.decode('utf8').rstrip())
##    if 'Haswell' in line.decode('utf8'):
##        genmove()
##    elif '=' in line.decode('utf8') and random.choices(range(3))[0] == 1:
##        genmove()



class leelaz:
    def __init__(self,command):
        self.inputlist = []
        self.bufferlist = []
        self.bestmoves = []
        self.pondering = False
        self.reading = False
        self.sgf = [[],[]]
##        self.ready = False
        self.color = 'b'
##        self.passed = False
        self.cmd = command#['leelaz','-wnetwork','-g']
        self.process = self.loadengine()
##        self.ponder()
        thread = Thread(target=self.readinfo).start()
        
        
    def loadengine(self):
        p = subprocess.Popen(self.cmd,
                             bufsize=1,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
##                             shell=True
                             )
        return p

    def loadsgf(self):
        self.sendcmd('clear_board\r\n')
        for i in self.sgf[0]:
            self.sendcmd('play b {}\r\n'.format(i))
        for i in self.sgf[1]:
            self.sendcmd('play w {}\r\n'.format(i))
            
        if self.color == 'w' and len(self.sgf[1]):
                self.sendcmd('play b pass\r\n')
        if self.color == 'b' and len(self.sgf[0]) and not len(self.sgf[1]):
            self.sendcmd('play w pass\r\n')
            
    def start(self):
        self.loadsgf()
##        if self.color == 'w':
##            self.sendcmd('play b pass\r\n')
        self.ponder()
##        thread = Thread(target=self.readinfo).start()
        
    def ponder(self):
        cmd = 'time_left {} 0 0\r\n'.format(self.color)
##        print(self.process.stdout.readline())
        self.sendcmd(cmd)

    def toggleponder(self):
        if self.pondering:
            self.pondering = False
            self.sendcmd('name\r\n')
        else:
            self.pondering = True
            self.ponder()
            
    def shutdown(self):
##        self.process.terminate()
        self.process.kill()
##        ctypes.windll.kernel32.TerminateProcess(int(self.process._handle), -1)

    

    def sendcmd(self,cmd):
        self.process.stdin.write(cmd.encode('utf8'))
        self.process.stdin.flush()
##        print(self.process.stdout.readline())


    def readinfo(self):
##        self.process.stdin.write(b'genmove b\r\n')
##        self.process.stdin.flush()
##        print(self.process.stdout.readline())
        while not self.process.poll():
            buffer = self.process.stdout.readline()
            #print(buffer)
            if self.pondering:
                self.parseline(buffer.decode('utf8'))
            
            if len(self.inputlist):
                cmd = self.inputlist.pop()
                self.sendcmd(cmd)

        return

    def parseline(self,buffer):
        if buffer.startswith('~begin'):
            self.reading = True
            self.bufferlist = []
        elif buffer.startswith('~end'):
            self.reading = False
            self.bestmoves = [self.parsemove(i) for i in self.bufferlist
                              if self.parsemove(i)]
            self.bufferlist = []
        elif self.reading:
            self.bufferlist.append(buffer)
        else:
            print(buffer.rstrip())
            pass

    def parsemove(self,movestr):

        infotmp = [i for i in movestr.strip().split() if i]
        if len(infotmp) > 8:
            return[infotmp[0],infotmp[2],infotmp[4][:-2],infotmp[8:]]
        else:
            return False

if __name__ == "__main__":
    import time
    a = time.time()
    lz = leelaz()
##    time.sleep(2)
##    while lz.bestmoves
    lz.start()
    
    print(lz.bestmoves)
    time.sleep(3)
    print(lz.bestmoves)
    time.sleep(6)
    print(lz.bestmoves)
    lz.shutdown()
