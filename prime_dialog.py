import os
import sys


class Solution:
    def __init__(self, name: str, command: str = None):
        self.name = name
        self.command = command

    def __str__(self):
        return self.name


class Solutions:
    @staticmethod
    def __is_installed(executable: str) -> bool:
        sh = os.popen('which ' + executable + ' 2> /dev/null')
        return sh.read() != ''

    def __init__(self):
        self.run_list = [Solution('Run normally')]
        # Test for optimus-manager:
        self.optimus_manager = self.__is_installed('optimus-manager')
        # Test for prime-run:
        self.prime_run = self.__is_installed('prime-run')
        if self.prime_run:
            self.run_list.append(Solution('NVIDIA Prime', 'prime-run'))
        # Test for pvkrun
        self.bb_primus_vk = self.__is_installed('pvkrun')
        if self.bb_primus_vk:
            self.run_list.append(Solution('Bumblebee Vulkan (pvkrun)', 'pvkrun'))
        # Test for primusrun:
        self.bb_primusrun = self.__is_installed('primusrun')
        if self.bb_primusrun:
            self.run_list.append(Solution('Bumblebee (primusrun)', 'primusrun'))
        # Test for optirun:
        self.bb_optirun = self.__is_installed('optirun')
        if self.bb_optirun:
            self.run_list.append(Solution('Bumblebee (optirun)', 'optirun'))


def get_optimus_manager_mode() -> str:
    sh = os.popen('optimus-manager --print-mode')
    return sh.read().split(' : ')[1].replace('\n', '')


def run_with_solution(command: str, using: Solution = None) -> None:
    if using.command:
        command = using.command + " " + command
    print(command)
    os.system(command)


if __name__ == "__main__":
    solutions = Solutions()

    solution = None

    if solutions.optimus_manager:
        # Check if X is running on the nvidia card
        mode = get_optimus_manager_mode()
        print('You are running on ' + mode + ' graphics using optimus-manager')
        if mode == 'nvidia':
            solution = ''
            print('continue')
    for i, run in enumerate(solutions.run_list):
        print(str(i) + ': ' + str(run))
    solution = solutions.run_list[int(input('Choose a solution: '))]

    cmd = " ".join([arg for i, arg in enumerate(sys.argv) if i != 0])
    run_with_solution(cmd, solution)
