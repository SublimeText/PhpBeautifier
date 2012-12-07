import re
import os
import subprocess

import sublime
import sublime_plugin


class PhpBeautifierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Test environment
        if self.view.is_scratch():
            return

        if self.view.is_dirty():
            return sublime.status_message("Please save the file.")

        FILE = self.view.file_name()
        if not FILE or not os.path.exists(FILE):
            return self.status("File does not exist.")

        if not FILE[-3:] == 'php':
            return self.status("File does not have php extension.")

        # Start doing stuff
        cmd = "php_beautifier"
        indent = "-s4"
        filters = "ArrayNested() NewLines(before=switch:while:for:foreach:T_CLASS:return:break) Pear(add-header=false)"

        allFile = sublime.Region(0, self.view.size())
        AllFileText = self.view.substr(allFile).encode('utf-8')

        p = subprocess.Popen([cmd, indent, "-l", filters, "-f", "-", "-o", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate(AllFileText)
        if len(stderr) == 0:
            self.view.replace(edit, allFile, self.fixup(stdout))
        else:
            self.show_error_panel(self.fixup(stderr))

    # Error panel & fixup from external command
    # https://github.com/technocoreai/SublimeExternalCommand
    def show_error_panel(self, stderr):
        panel = self.view.window().get_output_panel("php_beautifier_errors")
        panel.set_read_only(False)
        edit = panel.begin_edit()
        panel.erase(edit, sublime.Region(0, panel.size()))
        panel.insert(edit, panel.size(), stderr)
        panel.set_read_only(True)
        self.view.window().run_command("show_panel", {"panel": "output.php_beautifier_errors"})
        panel.end_edit(edit)

    def fixup(self, string):
        return re.sub(r'\r\n|\r', '\n', string.decode('utf-8'))
