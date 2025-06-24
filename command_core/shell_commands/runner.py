import os
import inspect
import sys
from command_core.base_command import BaseCommand
from command_core.shell_commands import testscenario
from adapter.ssd_adapter_interface import SSDShellInterface
from command_core.shell_commands.testscenario import TestScenario
from command_core.exceptions import InvalidLBAError

scenario_map = {
    "1_FullWriteAndReadCompare": testscenario.TestScenario1,
    "2_PartialLBAWrite": testscenario.TestScenario2,
    "3_WriteReadAging": testscenario.TestScenario3,
    "4_EraseAndWriteAging": testscenario.TestScenario4,
}


class Runner(BaseCommand):
    def __init__(self, ssd: SSDShellInterface):
        self.ssd = ssd

    def execute(self):
        script_path = os.path.join(os.path.dirname(__file__), "..", "..", "shell_scripts.txt")
        script_path = os.path.abspath(script_path)

        if not os.path.exists(script_path):
            print(script_path)
            print("Error: shell_scripts.txt not exists")
            return

        with open(script_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        for scenario_name in lines:
            try:
                # testscenario 모듈에서 클래스 가져오기
                scenario_class = scenario_map.get(scenario_name)
                if scenario_class is None:
                    print(f"[Runner] '{scenario_name}' not found")
                    return

                if not inspect.isclass(scenario_class) or not issubclass(scenario_class, TestScenario):
                    print(f"[Runner] '{scenario_name}'는 유효한 TestScenario가 아닙니다.")
                    return

                print(f"{scenario_name} ___ Run...", end='',flush=True)
                scenario = scenario_class(self.ssd)
                scenario.set_loop(1)
                result = scenario.execute(is_runner_called=True)
                if result:
                    print(f"Pass")
                else:
                    print(f"FAIL!")
                    sys.exit(0)

            except InvalidLBAError as e:
                print(f"[Runner] LBA 범위 오류: {e}")
            except Exception as e:
                print(f"[Runner] '{scenario_name}' 실행 중 오류 발생: {e}")

        sys.exit(0)