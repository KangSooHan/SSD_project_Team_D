import pytest
from ssd_core.abstract_ssd import AbstractSSD
from ssd_core.normal_ssd import NormalSSD
from command_core.shell_commands.read_command import ReadCommand


@pytest.mark.parametrize("lba", [1, 2, 3, 4, 99])
def test_read_성공(mocker, lba):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    read_cmd = ReadCommand(ssd, lba)

    # act
    read_cmd.execute()

    # assert
    ssd.read.assert_called_once_with(lba)


@pytest.mark.parametrize("lba", [-1, 100])
def test_read_실패(mocker, lba):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    read_cmd = ReadCommand(ssd, lba)

    # act & assert
    with pytest.raises(Exception):
        read_cmd.execute()


@pytest.mark.parametrize("lba", [1, 2, 3, 4, 99])
def test_read_출력확인_성공(mocker, capsys, lba):
    # arrange
    ssd: NormalSSD = mocker.Mock()
    ssd.read.return_value = "0xABABABAB"
    read_cmd = ReadCommand(ssd, lba)

    # act
    read_cmd.execute()

    # assert
    captured = capsys.readouterr()
    expected_output = f"[Read] LBA {lba:02d} : 0xABABABAB\n"
    assert captured.out == expected_output
    ssd.read.assert_called_once_with(lba)


@pytest.mark.parametrize("lba", [-1, 100, 2000])
def test_read_잘못된범위_실패(mocker, lba):
    # arrange
    ssd: NormalSSD = mocker.Mock()
    read_cmd = ReadCommand(ssd, lba)

    # act & assert
    with pytest.raises(Exception):
        read_cmd.execute()
