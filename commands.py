import json
import urllib.request

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from pybot import WhatsApp


def help_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len != 0:
        return True, "OMG Not like that"

    box = whatsapp.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")

    for i in whatsapp.commands:
        box.send_keys(">> " + i)
        ActionChains(whatsapp.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).perform()

    whatsapp.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()

    return False, ""


def ping_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len != 0:
        return True, "OMG Not like that"
    return True, "Pong!"


def wikipedia_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len < 1:
        return True, "OMG Not like that"
    try:
        with urllib.request.urlopen(
                "https://en.wikipedia.org/api/rest_v1/page/summary/" + message.replace(" ", "_")) as response:
            result = response.read()
        result = json.loads(result)
        return True, result["extract"]
    except Exception as e:
        return True, "Internal error: " + str(e)


def hello_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len != 0:
        return True, "OMG Not like that"
    return True, "Hello " + whatsapp.get_user()


def spam_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len != 1:
        return True, "OMG Not like that"

    for i in range(0, int(message)):
        whatsapp.send_message_current_chat("SPAM " + str(i))

    return False, ""


def say_command(whatsapp: WhatsApp, message: str, arg_len: int) -> (bool, str):
    if arg_len < 1:
        return True, "OMG Not like that"
    return True, message


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
    return True, whatsapp.get_user()
