import pytest
from ssd_core.abstract_ssd import AbstractSSD
from shell_core.commands.erase_command import EraseCommand

@pytest.mark.parametrize("lba,size", [(0,3),(1,8)])
def test_erase_성공(mocker, lba, size):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    erase_cmd = EraseCommand(ssd, lba, size)

    # act
    erase_cmd.execute()

    # assert
    assert ssd.erase.call_count == 1


@pytest.mark.parametrize("lba,size,result", [(0, 11, 2),(8,44,5), (5, 1, 1)])
def test_erase_10개초과_성공(mocker, lba, size, result):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    erase_cmd = EraseCommand(ssd, lba, size)

    # act
    erase_cmd.execute()

    # assert
    assert ssd.erase.call_count == result


@pytest.mark.parametrize("lba,size,result", [(0, -11, 1),(8,-3,1), (22, -13, 2), (5, -1, 1)])
def test_erase_size가음수인경우_성공(mocker, lba, size, result):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    erase_cmd = EraseCommand(ssd, lba, size)

    # act
    erase_cmd.execute()

    # assert
    assert ssd.erase.call_count == result

@pytest.mark.parametrize("lba,size,result", [(90, 11, 1),(95,20,1)])
def test_erase_size99초과_성공(mocker, lba, size, result):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    erase_cmd = EraseCommand(ssd, lba, size)

    # act
    erase_cmd.execute()

    # assert
    assert ssd.erase.call_count == result



