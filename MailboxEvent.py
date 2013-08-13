import sublime
import sublime_plugin
import smtplib
import os
import sys
import mimetypes
import threading
from email import encoders
from email.message import Message
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class MailboxDispatcher(threading.Thread):

	def __init__(self, mail, account):
		
		self.email = mail
		self.account = account
		self.result = None

		threading.Thread.__init__(self)

	def run(self):

		server = self.account['server']
		port = self.account['port']
		username = self.account['username']
		password = self.account['password']

		sublime.status_message('Mailbox: Connecting To Server ' + server + ':' + port)

		try:
			server = smtplib.SMTP(server, port)
		except smtplib.SMTPConnectError as WTF:
			self.result = "[Error]: Cannot connect to the server at " + server + " on port " + port

		server.ehlo()
		# server.starttls()
		server.esmtp_features['auth'] = 'LOGIN DIGEST-MD5 PLAIN'

		self.result = "[Success]: Email sent successfully"

		try:
			sublime.status_message('Mailbox: Logging in as ' + username)
			server.login(username, password)
		except smtplib.SMTPAuthenticationError as WTF:
			self.result = "[Error]: The server didn’t accept the username/password combination."
		except smtplib.SMTPException as WTF:
			self.result = "[Error]: Error Logging In. Cannot send the email"

		try:
			sublime.status_message('Mailbox: Dispatching Mail')
			# server.send_message(self.email)
			server.sendmail(self.email['From'], self.email['To'], self.email.as_string())
			
		except smtplib.SMTPRecipientsRefused as WTF:
			self.result = "[Error]: All recipients were refused, Nobody got the email."
		except smtplib.SMTPSenderRefused as WTF:
			self.result = "[Error]: Server refused your email as sender"
		except smtplib.SMTPDataError as WTF:
			self.result = "[Error]: Something wicked happened, Email was not sent."

		server.quit()

class MailboxEvent(sublime_plugin.EventListener):
	
	def on_pre_close(self, view):
		
		if view.name() == 'mailbox_mail_buffer':
			
			if view.size() > 0:		
				self.email_content = view.substr(sublime.Region(0, view.size()))
				
				self.view = view
				self.window = view.window()

				self.prepare_email()
			else:
				sublime.status_message('Not sending email. Aborted.')

	def prepare_email(self):

		self.settings = sublime.load_settings('Mailbox.sublime-settings')
		self.email_accounts = self.settings.get('email_accounts')

		self.items = []

		for account in self.email_accounts:
			listing = [account['name'], account['username']]
			self.items.append(listing)

		sublime.Window.show_quick_panel(self = self.window, items = self.items, on_select = self.prepare_sendmail, flags = 0, selected_index = -1, on_highlight = None)

	def prepare_sendmail(self, selected_account):

		if selected_account == -1:
			return

		self.selected_account = selected_account

		selected_account = self.email_accounts[selected_account];
		sublime.status_message('Using mailbox ' + selected_account['username'])

		self.email = MIMEMultipart()
		self.email['From'] = selected_account['username']

		sublime.Window.show_input_panel(self.window, 'Send To: ', '', self.prepare_receiver, None, None)

	def prepare_receiver(self, receiver):

		if len(receiver) == 0:
			return

		self.email['To'] = receiver
		self.receiver = receiver
		sublime.Window.show_input_panel(self.window, 'Subject: ', '', self.prepare_subject, None, None)

	def prepare_subject(self, subject):

		self.email['Subject'] = subject
		sublime.Window.show_input_panel(self.window, 'Attach File (Or leave blank for none): ', '', self.prepare_attachment, None, None)

	def prepare_attachment(self, attachment):
		
		if len(attachment) > 0:

			if os.path.isfile(attachment):
				filename = os.path.basename(attachment)

				sublime.status_message('Attaching file ' + attachment + ' as ' + filename)

				ctype, encoding = mimetypes.guess_type(attachment)

				if ctype is None or encoding is not None:
					ctype = 'application/octet-stream'

				maintype, subtype = ctype.split('/', 1)

				if maintype == 'text':
					fp = open(attachment)
					attachfile = MIMEText(fp.read(), _subtype=subtype)
					fp.close()
				elif maintype == 'image':
					fp = open(attachment, 'rb')
					attachfile = MIMEImage(fp.read(), _subtype=subtype)
					fp.close()
				elif maintype == 'audio':
					fp = open(attachment, 'rb')
					attachfile = MIMEAudio(fp.read(), _subtype=subtype)
					fp.close()
				else:
					fp = open(attachment, 'rb')
					attachfile = MIMEBase(maintype, subtype)
					attachfile.set_payload(fp.read())
					fp.close()
					encoders.encode_base64(attachfile)

				attachfile.add_header('Content-Disposition', 'attachment', filename=filename)
				self.email.attach(attachfile)

				sublime.status_message('File attached as ' + filename)

			else:
				sublime.status_message(attachment + ' is not a valid file. Nothing attached.')

		self.email.attach(MIMEText(self.email_content, 'html'))

		selected_account = self.email_accounts[self.selected_account]
		self.dispatch_email(selected_account)

	def dispatch_email(self, from_account):

		thread = MailboxDispatcher(self.email, from_account)
		thread.start()

		while thread.is_alive():
			continue

		message = thread.result or "Mailbox: Finished"
		sublime.status_message()