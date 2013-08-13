import sublime
import sublime_plugin

class MailboxCommand(sublime_plugin.TextCommand):

	def run(self, selected_text):
		sels = self.view.sel()
		content = []

		for sel in sels:
			content.append(self.view.substr(sel))

		content = "\n".join(content)

		mail_buffer = sublime.Window.new_file(self.view.window())
		mail_buffer.set_scratch(True)
		mail_buffer.set_name('mailbox_mail_buffer')
		mail_buffer.insert(selected_text, 0, content)