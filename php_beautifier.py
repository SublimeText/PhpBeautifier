import sublime, sublime_plugin
import subprocess
from subprocess import Popen
from subprocess import PIPE

class PhpBeautifierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        FILE = self.view.file_name()
        if FILE[-3:] == 'php':
            indent = "-s4"
            filters = "ArrayNested() NewLines(before=switch:while:for:foreach:T_CLASS:return:break) Pear(add-header=false)"
            allFile = sublime.Region(0, self.view.size())
            AllFileText = self.view.substr(allFile)
            cmd = "php_beautifier"
            p = Popen([cmd, indent, "-l", filters, "-f", "-", "-o", "-"], stdin = PIPE, stdout = PIPE, stderr=PIPE)
            stdout, stderr = p.communicate(AllFileText)
            if len(stderr) == 0:
                self.view.replace(edit, allFile, stdout)
            else:
                self.show_error_panel(stderr)

    def show_error_panel(self, stderr):
        panel = self.view.window().get_output_panel("php_beautifier_errors")
        panel.set_read_only(False)
        edit = panel.begin_edit()
        panel.erase(edit, sublime.Region(0, panel.size()))
        panel.insert(edit, panel.size(), stderr)
        panel.set_read_only(True)
        self.view.window().run_command("show_panel", {"panel": "output.php_beautifier_errors"})
        panel.end_edit(edit)