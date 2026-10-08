from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from backend.app.llm import detect_intent

FALLBACK = {"intent": "unknown", "confidence": 0.0}


@pytest.fixture
def gemini():
    """Replace the module-level Gemini client; no network call can happen."""
    with patch("backend.app.llm.client") as mock_client:
        yield mock_client


def reply(gemini, text):
    gemini.models.generate_content.return_value = SimpleNamespace(text=text)


def test_valid_json(gemini):
    reply(gemini, '{"intent": "balance", "confidence": 0.95}')
    assert detect_intent("balance?") == {"intent": "balance", "confidence": 0.95}


def test_uses_expected_model(gemini):
    reply(gemini, '{"intent": "emi", "confidence": 1}')
    detect_intent("emi")
    kwargs = gemini.models.generate_content.call_args.kwargs
    assert kwargs["model"] == "gemini-flash-lite-latest"


@pytest.mark.parametrize(
    "text",
    [
        '```json\n{"intent": "emi", "confidence": 0.8}\n```',
        '```\n{"intent": "emi", "confidence": 0.8}\n```',
        '  ```JSON\n{"intent": "emi", "confidence": 0.8}```  ',
    ],
)
def test_markdown_fenced_json(gemini, text):
    reply(gemini, text)
    assert detect_intent("emi") == {"intent": "emi", "confidence": 0.8}


@pytest.mark.parametrize("text", ["", "   \n", None])
def test_empty_or_none_text(gemini, text):
    reply(gemini, text)
    assert detect_intent("hi") == FALLBACK


@pytest.mark.parametrize("text", ["not json", "{broken", "[1, 2]", '"just a string"'])
def test_invalid_json_or_shape(gemini, text):
    reply(gemini, text)
    assert detect_intent("hi") == FALLBACK


@pytest.mark.parametrize(
    "payload",
    [
        '{"intent": "hack_the_bank", "confidence": 0.9}',
        '{"confidence": 0.9}',
        '{"intent": 5, "confidence": 0.9}',
        '{"intent": ["balance"], "confidence": 0.9}',
    ],
)
def test_invalid_intent_becomes_unknown(gemini, payload):
    reply(gemini, payload)
    assert detect_intent("hi")["intent"] == "unknown"


@pytest.mark.parametrize(
    "payload",
    [
        '{"intent": "balance", "confidence": "high"}',
        '{"intent": "balance", "confidence": null}',
        '{"intent": "balance", "confidence": [1]}',
        '{"intent": "balance"}',
        '{"intent": "balance", "confidence": NaN}',
    ],
)
def test_invalid_confidence_becomes_zero(gemini, payload):
    reply(gemini, payload)
    assert detect_intent("hi") == {"intent": "balance", "confidence": 0.0}


def test_confidence_clamped(gemini):
    reply(gemini, '{"intent": "balance", "confidence": 7}')
    assert detect_intent("hi")["confidence"] == 1.0
    reply(gemini, '{"intent": "balance", "confidence": -3}')
    assert detect_intent("hi")["confidence"] == 0.0


def test_gemini_exception(gemini):
    gemini.models.generate_content.side_effect = RuntimeError("quota exceeded")
    assert detect_intent("hi") == FALLBACK


def test_response_without_text_attribute(gemini):
    gemini.models.generate_content.return_value = MagicMock(spec=[])
    assert detect_intent("hi") == FALLBACK
