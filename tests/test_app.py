"""Smoke tests for process_input helper."""
import sys
import os
import unittest.mock

# Mock streamlit before importing app so module-level st.* calls are no-ops.
sys.modules["streamlit"] = unittest.mock.MagicMock()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import process_input  # noqa: E402


def test_process_input_returns_string():
    result = process_input("hello", temperature=0.7, max_tokens=50)
    assert isinstance(result, str)


def test_process_input_contains_input_text():
    result = process_input("test prompt", temperature=0.5, max_tokens=100)
    assert "test prompt" in result


def test_process_input_reflects_temperature():
    result = process_input("x", temperature=0.3, max_tokens=10)
    assert "0.3" in result


def test_process_input_reflects_max_tokens():
    result = process_input("x", temperature=0.7, max_tokens=200)
    assert "200" in result
