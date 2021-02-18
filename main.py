from commands import *
from pybot import WhatsApp

w = WhatsApp(".", "chromedriver.exe", "Idle", False)
w.start()

w.register_command("#help", help_command)
w.register_command("#ping", ping_command)
w.register_command("#wikipedia", wikipedia_command)
w.register_command("#hello", hello_command)
w.register_command("#SPAM", spam_command)
w.register_command("#say", say_command)
w.register_command("#emote", emote_command)
w.register_command("#whois", whois_command)
w.register_command("#perm->add", perms_add_command)
w.register_command("#perm->remove", perms_remove_command)
w.register_command("#perm->get", perms_get_command)
w.register_command("#blacklist->add", blacklist_add_command)
w.register_command("#blacklist->remove", blacklist_remove_command)
w.register_command("#blacklist->get", blacklist_get_command)
w.register_command("#crash", crash_command)
w.register_command("#crash->info", crash_info_command)
w.register_command("#msg", msg_command)
w.register_command("#random", random_command)
w.register_command("#kill", kill_command)
w.register_command("#userinfo", user_info_command)
w.register_command("#join", join_command)

w.mainloop()

w.stop()
