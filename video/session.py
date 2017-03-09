import os
import signal
import subprocess
import multiprocessing
import time

class Session(object):
    channel = "****************"
    streamKey = "****-****-****-****"

    busy = False
    timeStamp = 0
    
    subscribers = []
    streamYtb = False
    proc = None

    def runYoutube(self):
        if not Session.streamYtb:
            Session.streamYtb = True
            
            with open(os.devnull, 'w') as devnull:
                Session.proc = subprocess.Popen("raspivid -o - -t 0 -n -w 1280 -h 720 -hf -vf -fps 30 -b 7000000 | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/" + self.streamKey,
                                                shell = True,
                                                stdin = devnull,
                                                stdout = devnull,
                                                stderr = subprocess.STDOUT)
                print 'start youtube session'
                
    def stopYoutube(self):
        if Session.streamYtb:
            Session.proc.terminate()
            Session().killProc()
            Session.streamYtb = False
            print 'stop youtube session'

    def killProc(self):
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        
        pid = None
        print 'stop ffmpeg & raspivid'
        for line in out.splitlines():
            if ("ffmpeg" in line) or ("raspivid" in line):
                pid = line.split()[0]
                if pid:
                    os.kill(int(pid), signal.SIGINT)
                    pid = None