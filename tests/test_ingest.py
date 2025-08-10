import pytest
from src.ingest import handle_from_url

def test_handle_from_url():
    assert handle_from_url("https://x.com/TwitterDev") == "TwitterDev"
    assert handle_from_url("https://twitter.com/TwitterDev") == "TwitterDev"
