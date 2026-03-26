from analysis.baseline_manager import BaselineManager
from analysis.model_trainer import ModelTrainer

baseline = BaselineManager()
trainer = ModelTrainer()

data = baseline.load()

trainer.train(data)