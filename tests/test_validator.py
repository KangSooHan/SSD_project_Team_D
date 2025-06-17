import pytest
from validator import Validator

def test_검증기_실행_테스트():
    validator = Validator()
    assert validator.run("test_input")