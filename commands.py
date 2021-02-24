import json
import urllib.request

import random
from time import sleep, time

from pybot import WhatsApp, WhatsAppStyle


def help_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len != 0:
        return True, "OMG Not like that"
    ws = WhatsAppStyle(whatsapp)

    for x in whatsapp.command_types:
        ws.fat(x)
        for y in whatsapp.command_types[x]:
            ws.typewriter(">> " + y)
        ws.format_print("")

    ws.send()

    return False, ""


def ping_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len != 0:
        return True, "OMG Not like that"
    return True, "Pong!"


def wikipedia_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len < 1:
        return True, "OMG Not like that"
    with urllib.request.urlopen(
            "https://en.wikipedia.org/api/rest_v1/page/summary/" + message.replace(" ", "_")) as response:
        result = response.read()
    result = json.loads(result)
    ws = WhatsAppStyle(whatsapp)
    ws.format_print(result["extract"])
    ws.send()
    return False, ""


def hello_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len != 0:
        return True, "OMG Not like that"
    ws = WhatsAppStyle(whatsapp)
    ws.type("Hello ")
    ws.tag(whatsapp.get_user())
    ws.send()
    return False, ""


def spam_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len < 1:
        return True, "OMG Not like that"
    if int(message.split("->")[1]) > 500:
        return True, "Please don't spam to much"

    ws = WhatsAppStyle(whatsapp)

    for i in range(0, int(message.split("->")[1])):

        ws.type("SPAM ")
        ws.tag(message.split("->")[0])
        ws.type(" " + str(i))
        ws.send()

    return False, ""

def spam_file_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len < 1:
        return True, "OMG Not like that"

    ws = WhatsAppStyle(whatsapp)

    with open(message) as file:
        for i in file.read().split("\n"):
            if i.strip():
                ws.type(i)
                ws.send()
    return True, "Spam done!"

def say_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len < 1:
        return True, "OMG Not like that"
    ws = WhatsAppStyle(whatsapp)
    ws.format_print(message)
    ws.send()
    return False, ""


def emote_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len != 1:
        return True, "OMG Not like that"
    emotes = {
        "shrug": "¯\_(ツ)_/¯",
        "tableflip": "(╯°□°）╯︵ ┻━┻",
        "unflip": "┬─┬ ノ( ゜-゜ノ)",
        "space": "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
    }

    if message == "keys":
        return True, str(emotes.keys())

    if message in emotes.keys():
        return True, emotes[message]
    return True, "Not found"


def whois_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len != 0:
        return True, "OMG Not like that"
    return True, "User: " + whatsapp.get_user() + ", Permissions: " + str(whatsapp.get_perms(whatsapp.get_user()))


def perms_add_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len < 1:
        return True, "OMG Not like that"
    whatsapp.set_perms(message, True)
    return True, "Changed permission of " + message + " to True"


def perms_remove_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len < 1:
        return True, "OMG Not like that"
    whatsapp.set_perms(message, False)
    return True, "Changed permission of " + message + " to False"


def perms_get_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len < 1:
        return True, "OMG Not like that"
    return True, "Permission of " + message + " is: " + str(whatsapp.get_perms(message))


def crash_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len != 0:
        return True, "OMG Not like that"

    var = 0 / 0


def crash_info_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len != 1:
        return True, "OMG Not like that"

    with open(message) as file:
        crash = file.read()
    ws = WhatsAppStyle(whatsapp)
    ws.typewriter(crash)
    ws.send()

    return False, ""


def msg_command(whatsapp: WhatsApp, message: str, arg_len: int):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len < 1:
        return True, "OMG Not like that"

    ws = WhatsAppStyle(whatsapp)
    ws.typewriter("Sending '" + message.split("->")[1] + "' to " + message.split("->")[0])
    ws.send()

    whatsapp.send_message(message.split("->")[0], message.split("->")[1])

    return False, ""


def random_command(whatsapp: WhatsApp, message: str, arg_len: int):
    if arg_len != 1:
        return True, "OMG Not like that"

    return True, "Your random number is: " + str(random.randint(0, int(message)))


def blacklist_add_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len < 1:
        return True, "OMG Not like that"
    whatsapp.set_blacklist(message, True)
    return True, "Changed blacklist of " + message + " to True"


def blacklist_remove_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len < 1:
        return True, "OMG Not like that"
    whatsapp.set_blacklist(message, False)
    return True, "Changed blacklist of " + message + " to False"


def blacklist_get_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len < 1:
        return True, "OMG Not like that"
    return True, "Blacklist of " + message + " is: " + str(whatsapp.get_blacklist(message))


def kill_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len != 0:
        return True, "OMG Not like that"

    whatsapp.send_message_current_chat("Im going to sleep now")

    sleep(1)

    whatsapp.driver.quit()
    exit(0)


def user_info_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len < 1:
        return True, "OMG Not like that"

    msg = "Permission: " + str(whatsapp.get_perms(message)) + "\n"
    msg += "Blacklist: " + str(whatsapp.get_blacklist(message)) + "\n"

    ws = WhatsAppStyle(whatsapp)
    ws.type("Userinfo for ")
    ws.tag(message)
    ws.format_print("\n")
    ws.typewriter(msg)
    ws.send()

    return False, ""


def join_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if not whatsapp.get_perms(whatsapp.get_user()):
        return True, "You can't do that"
    if arg_len < 1:
        return True, "OMG Not like that"

    user = whatsapp.get_user()

    if not message.__contains__("https://chat.whatsapp.com/"):
        return True, "Not a valid group"

    ws = WhatsAppStyle(whatsapp)
    ws.typewriter("Joining group: " + message.replace("https://chat.whatsapp.com/", ""))
    ws.send()

    sleep(1)

    message = message.replace("https://chat.whatsapp.com/", "https://web.whatsapp.com/accept?code=")
    whatsapp.driver.get(message)

    found = False

    start_ts = time()

    while not found:
        if start_ts + 30 < time():
            whatsapp.start()
            return True, "Something terrible happened\nI cant join the group " + message
        try:
            join_button = whatsapp.driver.find_element_by_xpath("//div[text()='Gruppe beitreten']")
            sleep(1)
            join_button.click()
            found = True
        except:
            pass

    sleep(2)

    try:
        ws.type("Hello world ")
        ws.tag(user)
        ws.type("added me")
        ws.send()
    except:
        pass

    while not whatsapp.select_chat(whatsapp.idle_chat):
        sleep(0.5)

    return False, ""
