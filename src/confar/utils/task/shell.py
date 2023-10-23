import subprocess
from ..Emitter import EventEmitter


class Shell(EventEmitter):

    def __init__(self, cmd: str):
        if not cmd:
            raise ValueError("cmd is mandatory!")
        super().__init__()
        self.cmd = cmd

    def run(self):
        # Use subprocess to run the command and capture its output
        process = subprocess.Popen(
            self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)

        # Read and process the output line by line in real-time
        for line in process.stdout:
            # Process each line as needed
            self.emit('data', line.strip())

        # Wait for the subprocess to finish
        # Check the exit code of the subprocess
        return process.wait() != 0
