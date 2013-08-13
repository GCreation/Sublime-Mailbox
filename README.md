Sublime Mailbox
===============

A Mailbox plugin for sublime text

### Disclaimer
This plugin is in early development stage.
I'll not be responsible if this burst on your face, fry your computer, eat your kids or kill your kitten.

### Configuration
Clone this repo inside __Packages__ directory (If you cant locate that then sure enough it is not suitable for you at the moment, wait till I improve it and make available in Package Manager. Thanks for your interest)
Open up `Mailbox.sublime-settings` and add in the details under `email_accounts`:
 - name (Give you account a name to distinguish)
 - username (Your username which you use to log in)
 - password (Password, of course)
 - server (SMTP server, generally `smtp.yourdomain.com`)
 - port (Port to connect with server, generally 587)

### What It Does
Enables a rapid way to send out emails, optionally with an attachment.

### How It Does That
You can use the keyboard shortcut <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>M</kbd> or quick panel to access `Mailbox`.
If you have text selected in current view then it will automatically be appended to the email body.

A new tab will open where you can edit the content of your email, HTML is supported so feel free to go crazy.
Now just close the tab (hit <kbd>CTRL</kbd>+<kbd>W</kbd> or close the tab with mouse) and an input box will pop us asking for the recipient. Enter the email address of the person you want to send the email to and then enter the subject line in next input box that will appear.
You can also attach a file by providing absolute path to the file in next input box that will appear or just leave it blank if you dont want to attach any file.

Hit <kbd>ENTER</kbd> and away goes the email.

### Known Bugs
Consider this entire plugin a bug. I wrote this in about an hour or two (including the debugging time) so I cannot tell you what is broken. However, it works fine for my needs.

### Features Plan
 - Improvement in thread handling (I'm not sure if this will lag on a slow connection)
 - Ability to check new emails
 - Ability to read mails
 - Better email composition with syntax support or something like that
 - Something else that I'm missing