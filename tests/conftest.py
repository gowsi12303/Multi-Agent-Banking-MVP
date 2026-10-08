import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, ROOT.as_posix())

# llm.py builds a Gemini client at import time. A dummy key lets the module
# import without a real key; no request is ever sent (the client is mocked).
os.environ.setdefault("GEMINI_API_KEY", "dummy-key-for-tests")

from fastapi.testclient import TestClient  # noqa: E402

from backend.app.main import app  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)
