import pytest
from ssd_core.abstract_ssd import AbstractSSD
from shell_core.commands.erase_range_command import EraseRangeCommand

@pytest.mark.parametrize("start,end", [(0,3),(1,8),(5,5)])
def test_erase_range_성공(mocker, start, end):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    erase_cmd = EraseRangeCommand(ssd, start, end)

    # act
    erase_cmd.execute()

    # assert
    assert ssd.erase.call_count == 1


@pytest.mark.parametrize("start,end,result", [(0, 11, 2),(8,52,5)])
def test_erase_range_10개초과_성공(mocker, start, end, result):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    erase_cmd = EraseRangeCommand(ssd, start, end)

    # act
    erase_cmd.execute()

    # assert
    assert ssd.erase.call_count == result


@pytest.mark.parametrize("start,end,result", [(10,0,2), (22, 13, 1), (5, -1, 1)])
def test_erase_range_start_end가반대인경우_성공(mocker, start, end, result):
    # arrange
    ssd: AbstractSSD = mocker.Mock()
    erase_cmd = EraseRangeCommand(ssd, start, end)

    # act
    erase_cmd.execute()

    # assert
    assert ssd.erase.call_count == result
