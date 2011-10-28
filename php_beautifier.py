import commands
import sublime, sublime_plugin

class PhpBeautifierCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        FILE = self.view.file_name()
        if FILE[-3:] == 'php':
            PHP_OPTIONS = "-s4 -l \'ArrayNested() NewLines(before=switch:while:for:foreach:T_CLASS:return:break,after=T_COMMENT:protected:private)\' "
            selection = self.view.sel()[0]
            replaceRegion = selection if len(selection) > 0 else sublime.Region(0, self.view.size())
            res = commands.getoutput("php_beautifier " + PHP_OPTIONS +
            "-f " + self.view.file_name() + " -o -")
            resu = unicode( res, "utf-8" )
            self.view.replace(edit, replaceRegion, resu)
