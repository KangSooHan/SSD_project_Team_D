from ssd_core.abstract_buffer_optimizer import AbstractBufferOptimizer
from ssd_core.discovery_buffer_optimizer import DiscoveryBufferOptimizer
from ssd_core.simple_buffer_optimizer import SimpleBufferOptimizer
from validator import Packet


class BufferOptimizerProvider:
    @classmethod
    def get_instance(cls, buffer_lst: list[Packet]) -> AbstractBufferOptimizer:
        """
        최적화 대상 명령어 구성에 따라 적합한 알고리즘(Optimizer)를 반환한다.
        """
        if len(buffer_lst) < 3:
            """
            최적화 대상 명령어가 3개 미만인 경우 
            메모리 사용량이 높지만 전체 탐색을 수행하는 DiscoveryOptimizer를 사용한다.
            """
            return DiscoveryBufferOptimizer()
        else:
            """
            최적화 대상 명령어가 3개 이상인 경우 반복 최적화가 필요한 경우의 수가 발생하므로
            내부적으로 ignore command, merge erase를 반복하는 SimpleBufferOptimizer를 사용한다.
            """
            return SimpleBufferOptimizer()
