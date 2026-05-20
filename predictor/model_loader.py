import os
import joblib

_MODEL = None

def get_model():
    global _MODEL
    if _MODEL is not None:
        return _MODEL

    # default path to predictor/model/model.joblib
    default_path = os.path.join(os.path.dirname(__file__), "model", "model.joblib")
    model_path = os.getenv("HOUSE_MODEL_PATH", default_path)

    if os.path.exists(model_path):
        try:
            print(f"[model_loader] Loading model from: {model_path}")
            _MODEL = joblib.load(model_path)
            print("[model_loader] Model loaded successfully ✅")
            return _MODEL
        except Exception as e:
            print(f"[model_loader] Failed to load model: {e}")

    # fallback dummy model if file missing
    class DummyModel:
        def predict(self, X):
            try:
                n = len(X)
            except Exception:
                return [0.0]
            return [0.0] * n

    _MODEL = DummyModel()
    print("[model_loader] Using DummyModel (fallback)")
    return _MODEL
