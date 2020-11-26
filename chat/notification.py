import threading
from threading import Thread
import time

class NotificationThread(threading.Thread):
    def __init__(self, subject):
        self.test = subject
        threading.Thread.__init__(self)

    def run (self):
        time.sleep(10)
        print(self.test)
        return self.test

def send_html_mail(subject):
    NotificationThread(subject).start()