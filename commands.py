import json
import urllib.request

from selenium.webdriver.chrome.webdriver import WebDriver


def ping_command(driver: WebDriver, message: str) -> (bool, str):
    if len(message.split(" ")) != 1:
        return True, "OMG Not like that"
    return True, "Pong!"


def wikipedia_command(driver: WebDriver, message: str) -> (bool, str):
    if len(message.split(" ")) < 2:
        return True, "OMG Not like that"
    try:
        with urllib.request.urlopen("https://en.wikipedia.org/api/rest_v1/page/summary/" + "_".join(
                message.split(" ")[1:len(message.split(" "))])) as response:
            result = response.read()
        result = json.loads(result)
        return True, result["extract"]
    except Exception as e:
        return True, "Internal error: \n" + str(e)


def hello_command(driver: WebDriver, message: str) -> (bool, str):
    if len(message.split(" ")) != 1:
        return True, "OMG Not like that"
    return True, "Hello world"


def say_command(driver: WebDriver, message: str) -> (bool, str):
    if len(message.split(" ")) < 2:
        return True, "OMG Not like that"
    return True, " ".join(message.split(" ")[1:len(message.split(" "))])
