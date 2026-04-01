# sensors/process_layer/process_event.py

class ProcessEvent:
    def __init__(self):
        self.pid = None
        self.process_name = None
        self.exe_path = None
        self.parent_pid = None
        self.parent_name = None