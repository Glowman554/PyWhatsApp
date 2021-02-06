from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver

commands = {}

def goto_idle(driver: WebDriver):
    return select_chat(driver, "Idle")


def select_chat(driver: WebDriver, where: str) -> bool:
    try:
        user = driver.find_element_by_xpath(f"//span[@title='{where}']")
        user.click()
        sleep(0.1)
        return True
    except:
        return False


def send_message(driver: WebDriver, where: str, message: str) -> bool:
    try:
        select_chat(driver, where)
        box = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
        box.send_keys(message)
        driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()
        goto_idle(driver)
        return True
    except:
        return False


def send_message_current_chat(driver: WebDriver, message: str) -> bool:
    try:
        box = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
        box.send_keys(message)
        driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()
        goto_idle(driver)
        return True
    except:
        return False


def get_last_message(driver: WebDriver) -> str:
    try:
        msg = driver.find_elements_by_xpath("//span[@dir='{}']/span".format("ltr"))
        return msg[-1].text
    except:
        pass


def wait_for_message(driver: WebDriver) -> str:
    while True:
        try:
            msg = driver.find_element_by_xpath("//span[@aria-label='{}']".format("1 ungelesene Nachricht"))
            msg.click()
            sleep(0.1)
            return get_last_message(driver)
        except:
            pass


def get_user_and_time(driver: WebDriver) -> str:
    try:
        user = driver.find_elements_by_xpath("//span[@dir='{}']".format("ltr"))[-1].find_element_by_xpath("./../..").get_attribute("data-pre-plain-text")
        return user
    except:
        pass

def command(driver: WebDriver, message: str) -> (bool, str):
    pass

def help_command(driver: WebDriver, message: str) -> (bool, str):
    if len(message.split(" ")) != 1:
        return (True, "OMG Not like that")

    msg = ""
    for i in commands:
        msg += ">> " + i + "\n"

    return (True, msg)

def register_command(what: str, handler: command):
    commands[what] = handler;
    print("Registrating command", what)

def on_message(driver: WebDriver, message: str):
    command = message.split(" ")[0]

    for i in commands:
        if i == command:
            is_response, what = commands[i](driver, message)
            if is_response:
                send_message_current_chat(driver, what)

def mainloop(driver: WebDriver):
    while True:
        message = wait_for_message(driver)
        print(get_user_and_time(driver) + message)
        on_message(driver, message)
        goto_idle(driver)