import pytest
from ssd.abstract_ssd import AbstractSSD
from shell.commands.write_command import WriteCommand

def test_write_성공(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    write_cmd = WriteCommand(ssd)

    # act
    write_cmd.execute(3, '0xAAAABBBB')

    # assert
    assert ssd.write.call_count == 1

def test_write_실패_LBA범위초과(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    write_cmd = WriteCommand(ssd)

    # act & assert
    with pytest.raises(Exception):
        write_cmd.execute(100, '0xAAAABBBB')


def test_write_실패_VALUE길이_10자초과(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    write_cmd = WriteCommand(ssd)

    # act & assert
    with pytest.raises(Exception):
        write_cmd.execute(3, '0xAAAABBBBB')


def test_write_실패_VALUE길이_10자미만(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    write_cmd = WriteCommand(ssd)

    # act & assert
    with pytest.raises(Exception):
        write_cmd.execute(3, '0xAAAABBB')

def test_write_실패_VALUE값_16진수범위초과(mocker):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    write_cmd = WriteCommand(ssd)

    # act & assert
    with pytest.raises(Exception):
        write_cmd.execute(3, '0xAAAAFFFG')

