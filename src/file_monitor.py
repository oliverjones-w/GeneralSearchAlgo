import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

def load_excel_to_dataframe(file_path):
    df = pd.read_excel(file_path, sheet_name='Master')
    return df

class ExcelFileHandler(FileSystemEventHandler):
    def __init__(self, file_path, update_callback):
        self._file_path = file_path
        self._update_callback = update_callback

    def on_modified(self, event):
        if event.src_path == self._file_path:
            print(f'{self._file_path} has been modified.')
            self._update_callback()

def monitor_file(file_path, update_callback):
    observer = Observer()
    event_handler = ExcelFileHandler(file_path, update_callback)
    observer.schedule(event_handler, path=file_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()