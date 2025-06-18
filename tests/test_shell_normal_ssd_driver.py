import pytest
from shell.normal_ssd_driver import NormalSsdDriver

def test_normal_ssd_driver_구현(mocker):
    # arrange
    ssd: NormalSsdDriver = mocker.Mock()

    # act & assert
    assert True