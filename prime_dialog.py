import os
import sys

from PyQt5.QtWidgets import *


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


class Dialog(QWidget):
    def __init__(self, solutions: Solutions, command: str, om_mode: str = None):
        super().__init__()
        self.command = command
        self.solutions = solutions

        self.solution = None

        # Show optimus-manager information:
        if om_mode:
            text = 'You are running on '+om_mode+' graphics (using optimus-manager)'
            if om_mode == 'nvidia':
                text = 'You are already running on '+om_mode+' graphics (using optimus-manager)'
            self.optimus_manager_text = QLabel(self)
            self.optimus_manager_text.setText(text)

        # Show dropdown with solutions
        self.dropdown = QComboBox(self)
        for run in solutions.run_list:
            self.dropdown.addItem(run.name)

        self.dropdown.activated[str].connect(self.onChanged)

        # Add placeholder for the command that will be ran
        self.command_text = QLabel(self)

        # Add run button
        self.button = QPushButton('Run')
        self.button.clicked.connect(self.on_button_clicked)

        # Create layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.optimus_manager_text)
        self.layout.addWidget(self.dropdown)
        self.layout.addWidget(self.command_text)
        self.layout.addWidget(self.button)

        self.onChanged(self.dropdown.currentText())

        self.setLayout(self.layout)

    def onChanged(self, text):
        chosen_solution = [s for s in self.solutions.run_list if s.name == text][0]
        self.solution = chosen_solution

        self.command_text.setText('Command: ' +
                                  (chosen_solution.command + ' ' if chosen_solution.command else '') + self.command)
        self.command_text.adjustSize()

    def on_button_clicked(self):
        self.close()
        run_with_solution(self.command, self.solution)


if __name__ == "__main__":
    solutions = Solutions()

    solution = None

    # if solutions.optimus_manager:
    #     # Check if X is running on the nvidia card
    #     mode = get_optimus_manager_mode()
    #     print('You are running on ' + mode + ' graphics using optimus-manager')
    #     if mode == 'nvidia':
    #         solution = ''
    #         print('continue')
    # for i, run in enumerate(solutions.run_list):
    #     print(str(i) + ': ' + str(run))
    # solution = solutions.run_list[int(input('Choose a solution: '))]
    #
    cmd = " ".join([arg for i, arg in enumerate(sys.argv) if i != 0])
    # run_with_solution(cmd, solution)

    app = QApplication(sys.argv)
    diag = Dialog(solutions, cmd, get_optimus_manager_mode())
    # diag.resize(500, 500)
    diag.show()
    app.exec_()
