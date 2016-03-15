
# coding: utf-8

__all__ = ['formatter']

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter
import jsonpickle
import sys

class ScrutinizerOutputFormatter(BaseReporter):

    __implements__ = IReporter

    def __init__(self, output=None):
        BaseReporter.__init__(self, output)
        self.messages = []
        self.i = 0

    def handle_message(self, msg):
        self.messages.append([msg.module, msg.msg_id, str(msg.line), str(msg.msg)])
        self.advance();

    def on_set_current_module(self, module, filepath):
        self.advance();

    def _display(self, layout):
        pass

    def on_close(self, stats, previous_stats):
        self.do_print("\nAnalysis finished, " + str(len(self.messages)) + " issues found.\n")

        f = open('./pylint_result.json', 'w')
        f.write(jsonpickle.encode(self.messages))
        f.close()

    def do_print(self, message):
        sys.stdout.write(message)
        sys.stdout.flush()

    def advance(self):
        if self.i % 5 == 0:
            self.do_print(".")

        self.i += 1

        if self.i % 400 == 0:
            self.do_print("\n")

