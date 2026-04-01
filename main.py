from sensors.file_layer.file_scanner import FileScanner
from intelligence.decision_engine import DecisionEngine
from analysis.feature_builder import FeatureBuilder
from analysis.baseline_manager import BaselineManager
from response.enforcer import Enforcer

def main():
    enforcer = Enforcer()
    scanner = FileScanner()
    engine = DecisionEngine()
    feature_builder = FeatureBuilder()
    baseline_manager = BaselineManager()

    file_path = r"C:\Users\Asus\Documents\WORK-SPACE\test_downloads\test_block.bat"
    pid = 1234  # fake PID

    event = scanner.scan(file_path, pid)

    if not event:
        print("File scan failed.")
        return

    # ---------------------------------------
    # Analysis Layer: Feature Extraction
    # ---------------------------------------
    feature_vector = feature_builder.build(event)

    # Save to baseline storage
    baseline_manager.save(feature_vector)

    # ---------------------------------------
    # Intelligence Layer: Decision
    # ---------------------------------------
    decision = engine.decide(event)

    # ---------------------------------------
    # Output
    # ---------------------------------------
    event.pretty_print()
    decision.pretty_print()
    enforcer.enforce(event, decision)
    

if __name__ == "__main__":
    main()