from commands import *
from pybot import WhatsApp

w = WhatsApp(".", "chromedriver.exe", "Idle", False)
w.start()


def reloadBot(*args, **kwargs):
    def reloadBotInside():
        from importlib import reload
        from sys import modules

        reload(modules[kwargs["module"] if "module" in kwargs else "commands"])

    return reloadBotInside()


w.register_command("#reload", "Admin commands", reloadBot)
w.register_command("#help", "Basics", help_command)
w.register_command("#ping", "Basics", ping_command)
w.register_command("#wikipedia", "Basics", wikipedia_command)
w.register_command("#hello", "Communication", hello_command)
w.register_command("#SPAM", "Admin commands", spam_command)
w.register_command("#say", "Communication", say_command)
w.register_command("#emote", "Communication", emote_command)
w.register_command("#whois", "Userinfo", whois_command)
w.register_command("#perm->add", "Admin commands", perms_add_command)
w.register_command("#perm->remove", "Admin commands", perms_remove_command)
w.register_command("#perm->get", "Admin commands", perms_get_command)
w.register_command("#blacklist->add", "Admin commands", blacklist_add_command)
w.register_command("#blacklist->remove", "Admin commands", blacklist_remove_command)
w.register_command("#blacklist->get", "Admin commands", blacklist_get_command)
w.register_command("#crash", "Dev Commands", crash_command)
w.register_command("#crash->info", "Dev Commands", crash_info_command)
w.register_command("#msg", "Admin commands", msg_command)
w.register_command("#random", "Basics", random_command)
w.register_command("#kill", "Dev Commands", kill_command)
w.register_command("#userinfo", "Userinfo", user_info_command)
w.register_command("#join", "Admin commands", join_command)

w.mainloop()

w.stop()
