import json
import urllib.request
import whatsapp

from selenium.webdriver.chrome.webdriver import WebDriver

def ping(driver: WebDriver, message: str) -> (bool, str):
    if len(message.split(" ")) != 1:
        return (True, "OMG Not like that")
    return (True, "Pong!")

def wikipedia(driver: WebDriver, message: str) -> (bool, str):
    if len(message.split(" ")) < 2:
        return (True, "OMG Not like that")
    try:
        with urllib.request.urlopen("https://en.wikipedia.org/api/rest_v1/page/summary/" + "_".join(message.split(" ")[1:len(message.split(" "))])) as response:
            result = response.read()
        result = json.loads(result)
        return (True, result["extract"])
    except:
        return (True, "Internal error")

def msg(driver: WebDriver, message: str) -> (bool, str):
    if len(message.split(" ")) < 3:
        return (True, "OMG Not like that")
    try:
        whatsapp.send_message(driver, message.split(" ")[1], " ".join(message.split(" ")[2:len(message.split(" "))]))
        return (False, "")
    except:
        return (True, "Internal error")