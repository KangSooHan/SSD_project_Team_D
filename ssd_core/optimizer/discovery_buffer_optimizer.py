from itertools import combinations
from ssd_core.optimizer.abstract_buffer_optimizer import AbstractBufferOptimizer
from validator import Packet

MAX_LBA_ADDRESS = 100

VALUE_EMPTY = 0
VALUE_VALID = 1

DEBUG_FEATURE = False   # True로 설정하면, stdout으로 각 케이스에 대한 중간 계산 결과가 출력됨

class DiscoveryBufferOptimizer(AbstractBufferOptimizer):
    def calculate(self, buffer_lst: list[Packet]) -> list[Packet]:
        self.print_result("")

        # trivial case
        if len(buffer_lst) == 0 or len(buffer_lst) == 1:
            return buffer_lst

        # '0'으로 write하는 명령은 erase 명령으로 교체한다.
        replaced_buffer_lst = self.replace_zero_write(buffer_lst)

        # erase 영역을 모은다.
        erase_mask = self.project_erase(replaced_buffer_lst)
        self.print_format("ERASE_MASK", erase_mask)

        # write 영역을 모은다.
        write_mask, write_value = self.project_write(replaced_buffer_lst)
        self.print_format("WRITE_MASK", write_mask)

        # erase, write mask를 합친다.
        merged_mask = self.merge_erase_and_write(erase_mask, write_mask)
        self.print_format("MERGED_MASK", merged_mask)

        # write에 의해 overwrite 되는 erase 영역을 찾는다.
        overwritten_idx = [i for i, x in enumerate(write_mask) if x == VALUE_VALID]
        self.print_format("OVER_WRITTEN_IDX", overwritten_idx, lst_seperator=',')

        best_erase_mask = erase_mask
        best_erase_cmd_lst = [cmd for cmd in replaced_buffer_lst if cmd.COMMAND == "E"]
        best_write_cmd_lst = [Packet("W", i, pkt[1])
                              for i, pkt in enumerate(zip(write_mask, write_value))
                              if pkt[0] == VALUE_VALID]

        # overwrite 영역은 erase 해도 되고 안해도 된다.
        # overwrite 영역을 하나씩 선택 하면서, 최소 erase 횟수를 찾는다.
        try_cnt = 1
        for r in range(0, len(overwritten_idx) + 1):
            for selected_element in combinations(overwritten_idx, r):
                # erase 명령은 명령이 있는 경우 1이 최소값이다. 최소값을 찾으면 추가 탐색하지 않는다.
                if len(best_erase_cmd_lst) <= 1:
                    break

                next_erase_mask = merged_mask.copy()
                for idx in selected_element:
                    next_erase_mask[idx] = VALUE_EMPTY

                current_erase_cmd_cnt = 0
                counting = False
                counting_cnt = 0
                current_erase_cmd_lst = []
                erase_cmd_new: Packet = None

                # 0~MAX_LBA_ADDRESS 까지 영역을 순회하면서 merge 가능한 erase lba를 찾는다.
                for i, value in enumerate(next_erase_mask):

                    # 탐색 중, 이미 찾은 최적값과 동일한 경우 탐색 중단
                    if current_erase_cmd_cnt >= len(best_erase_cmd_lst):
                        break

                    if value == VALUE_VALID:
                        if not counting:
                            counting = True
                            counting_cnt = 1
                            erase_cmd_new = Packet("E", i)
                        else:
                            if counting_cnt == 9:
                                current_erase_cmd_cnt += 1
                                erase_cmd_new.OP2 = 10
                                current_erase_cmd_lst.append(erase_cmd_new)
                                erase_cmd_new = None
                                counting = False
                                counting_cnt = 0
                            elif i == MAX_LBA_ADDRESS - 1:
                                current_erase_cmd_cnt += 1
                                erase_cmd_new.OP2 = counting_cnt + 1
                                current_erase_cmd_lst.append(erase_cmd_new)
                                erase_cmd_new = None
                                counting = False
                                counting_cnt = 0
                            else:
                                counting_cnt += 1
                    elif value == VALUE_EMPTY:
                        if counting:
                            current_erase_cmd_cnt += 1
                            erase_cmd_new.OP2 = counting_cnt
                            current_erase_cmd_lst.append(erase_cmd_new)
                            erase_cmd_new = None
                            counting = False
                            counting_cnt = 0

                if current_erase_cmd_cnt < len(best_erase_cmd_lst):
                    best_erase_mask = next_erase_mask
                    best_erase_cmd_lst = current_erase_cmd_lst

                try_cnt += 1
                self.print_format(f"#{try_cnt:>3},r={r},selected={selected_element},"
                                  f"result={current_erase_cmd_cnt},best={len(best_erase_cmd_lst)}",
                                  next_erase_mask)

        self.print_format("ERASE_MASK", erase_mask)
        self.print_format("FINAL_ERASE_BEST", best_erase_mask)
        self.print_format("WRITE_MASK", write_mask)
        self.print_format("MERGED_MASK", merged_mask)


        self.print_result(f"INPUT CMD(ORG),{len(buffer_lst)}={buffer_lst}")
        final_cmd_lst = best_erase_cmd_lst + best_write_cmd_lst     # erase + write 순서가 유지 되어야 함.
        if len(final_cmd_lst) < len(buffer_lst):
            self.print_result(f"FINAL CMD(OPT),{len(final_cmd_lst)}={final_cmd_lst}")
            return final_cmd_lst
        else:
            self.print_result(f"FINAL CMD(ORG),{len(buffer_lst)}={buffer_lst}")
            return buffer_lst

    def replace_zero_write(self, buffer_lst: list[Packet]) -> list[Packet]:
        new_lst = []
        for item in buffer_lst:
            if item.COMMAND == "W" and item.OP2 == 0:
                new_lst.append(Packet("E", item.OP1, 1))
            else:
                new_lst.append(item)
        return new_lst

    def project_erase(self, buffer_lst: list[Packet]) -> list[int]:
        mask = [0] * MAX_LBA_ADDRESS  # LBA 0~99
        for cmd in buffer_lst:
            if cmd.COMMAND == "E":
                for i in range(cmd.OP2):
                    mask[cmd.OP1 + i] = VALUE_VALID
        return mask

    def project_write(self, buffer_lst: list[Packet]) -> tuple[list[int], list[int]]:
        mask = [0] * MAX_LBA_ADDRESS  # LBA 0~99
        value = [0] * MAX_LBA_ADDRESS
        for cmd in buffer_lst:
            if cmd.COMMAND == "E":
                for i in range(cmd.OP2):
                    mask[cmd.OP1 + i] = VALUE_EMPTY  # overwrite
            elif cmd.COMMAND == "W":
                mask[cmd.OP1] = VALUE_VALID  # written
                value[cmd.OP1] = cmd.OP2
        return mask, value

    def merge_erase_and_write(self, erase_lst, write_lst) -> list[int]:
        mask = erase_lst.copy()
        for i in range(len(write_lst)):
            if write_lst[i] == VALUE_VALID:
                mask[i] = VALUE_VALID

        return mask

    def print_format(self, prefix, lst, lst_seperator=''):
        if DEBUG_FEATURE:
            print(f"{prefix:>50} [{lst_seperator.join(map(str, lst))}]")

    def print_result(self, data: str):
        if DEBUG_FEATURE:
            print(data)
