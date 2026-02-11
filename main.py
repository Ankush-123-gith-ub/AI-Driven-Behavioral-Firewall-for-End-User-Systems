from sensors.file.file_scanner import FileScanner
from intelligence.decision_engine import DecisionEngine
from response.enforcer import Enforcer

scanner = FileScanner()
engine = DecisionEngine()
enforcer = Enforcer()

event = scanner.scan_execution(
    file_path=r"C:\Users\Asus\Documents\flag\challenge.bin",  # use any real file path
    pid=1234,
    ppid=1000
)

verdict, reasons = engine.decide(event)
enforcer.enforce(verdict, event, reasons)
