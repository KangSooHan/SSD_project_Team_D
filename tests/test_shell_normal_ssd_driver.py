import pytest
from shell.normal_ssd_driver import NormalSSDDriver

def test_normal_ssd_driver_구현(mocker):
    # arrange
    ssd: NormalSSDDriver = mocker.Mock()

    # act & assert
    assert True