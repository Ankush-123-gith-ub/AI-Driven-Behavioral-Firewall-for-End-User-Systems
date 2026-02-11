import os
import getpass
import time
import uuid

from sensors.file.hashing import calculate_sha256
from sensors.file.signature import check_signature

class FileExecutionEvent:
    def __init__(
        self,
        event_id,
        timestamp,
        pid,
        ppid,
        execution_user,
        file_path,
        file_name,
        file_size,
        file_hash_sha256,
        signed,
        signer,
        first_seen
    ):
        self.event_id = event_id
        self.timestamp = timestamp
        self.pid = pid
        self.ppid = ppid
        self.execution_user = execution_user
        self.file_path = file_path
        self.file_name = file_name
        self.file_size = file_size
        self.file_hash_sha256 = file_hash_sha256
        self.signed = signed
        self.signer = signer
        self.first_seen = first_seen

# @dataclass(frozen=True)
# class FileExecutionEvent:
#     # --- Identity ---
#     event_id: str                 # unique id for this execution event
#     timestamp: float              # unix timestamp (seconds)

#     # --- Process info ---
#     pid: int                      # process id
#     ppid: int                     # parent process id
#     execution_user: str           # username that executed the file

#     # --- File info ---
#     file_path: str                # full path to executable
#     file_name: str                # executable name
#     file_size: int                # bytes
#     file_hash_sha256: str         # stable file identity

#     # --- Trust info ---
#     signed: bool                  # digitally signed or not
#     signer: Optional[str]         # signer name if available

#     # --- Context ---
#     first_seen: bool              # first time this hash is seen on system

class FileScanner:
    def __init__(self, seen_hashes=None):
        # In-memory store for now (later → DB)
        if seen_hashes is not None:
            self.seen_hashes = seen_hashes
        else:
            self.seen_hashes = set()


    def scan_execution(self, file_path, pid, ppid):
        """
        Simulate detection of a file execution.
        """

        # --- Basic file info ---
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # --- Identity ---
        file_hash = calculate_sha256(file_path)

        # --- First seen logic ---
        first_seen = file_hash not in self.seen_hashes
        self.seen_hashes.add(file_hash)

        # --- Trust info ---
        signed, signer = check_signature(file_path)

        # --- Build event ---
        event = FileExecutionEvent(
            event_id=str(uuid.uuid4()),
            timestamp=time.time(),
            pid=pid,
            ppid=ppid,
            execution_user=getpass.getuser(),
            file_path=file_path,
            file_name=file_name,
            file_size=file_size,
            file_hash_sha256=file_hash,
            signed=signed,
            signer=signer,
            first_seen=first_seen
        )

        return event