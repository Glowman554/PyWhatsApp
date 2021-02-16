from commands import *
from pybot import WhatsApp

w = WhatsApp(".", "chromedriver.exe", "Idle", False)
w.start()

w.register_command("!help", help_command)
w.register_command("!ping", ping_command)
w.register_command("!wikipedia", wikipedia_command)
w.register_command("!hello", hello_command)
#w.register_command("!SPAM", spam_command)
w.register_command("!say", say_command)
w.register_command("!emote", emote_command)


w.mainloop()

w.stop()
