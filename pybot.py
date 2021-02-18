import json
import logging
import random
import traceback
from time import sleep

from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import platform


class WhatsApp:

    def __init__(self, data_dir: str, driver_path: str, idle_chat: str, headless: bool):
        self.commands = {}
        self.idle_chat = idle_chat
        options = Options()

        options.add_argument("user-data-dir=chrome/" + data_dir)

        if headless:
            from pyvirtualdisplay import Display
            display = Display(visible=0, size=(800, 600))
            display.start()

        if driver_path is None:
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome(driver_path, options=options)

    def start(self):
        self.driver.get("https://web.whatsapp.com/")

        while not self.select_chat(self.idle_chat):
            logging.info("Waiting for idle")
            sleep(0.5)

    def stop(self):
        self.driver.quit()
        logging.warning("Stopping")

    def select_chat(self, where: str) -> bool:
        try:
            user = self.driver.find_element_by_xpath(f"//span[@title='{where}']")
            user.click()
            sleep(0.1)
            return True
        except:
            return False

    def send_message(self, where: str, what: str) -> bool:
        try:
            self.select_chat(where)
            box = self.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
            box.send_keys(what)
            self.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()
            return True
        except:
            return False

    def send_message_current_chat(self, what: str) -> bool:
        try:
            box = self.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
            box.send_keys(what)
            self.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()
            return True
        except:
            return False

    def get_last_message(self) -> str:
        try:
            msg = self.driver.find_elements_by_xpath("//span[@dir='{}']/span".format("ltr"))
            return msg[-1].text
        except:
            pass

    def wait_for_message(self) -> str:
        while True:
            try:
                msg = self.driver.find_element_by_xpath("//span[@aria-label='{}']".format("1 ungelesene Nachricht"))
                msg.click()
                sleep(0.1)
                return self.get_last_message()
            except:
                for i in range(2, 99):
                    try:
                        msg = self.driver.find_element_by_xpath("//span[@aria-label='{}']".format(f"{i} ungelesene Nachrichten"))
                        msg.click()
                        sleep(0.1)
                        return self.get_last_message()
                    except:
                        pass

    def get_user(self) -> str:
        try:
            user = self.driver.find_elements_by_xpath("//span[@dir='{}']".format("ltr"))[-1].find_element_by_xpath(
                "./../..").get_attribute("data-pre-plain-text").split("] ")[1].replace(": ", "")
            return user
        except:
            pass

    def get_perms(self, user: str) -> bool:
        with open("perms.json") as file:
            obj = json.loads(file.read())
            try:
                return obj[user]
            except:
                return False

    def set_perms(self, user: str, what: bool):
        with open("perms.json") as file:
            obj = json.loads(file.read())
        obj[user] = what
        with open("perms.json", "w") as file:
            file.write(json.dumps(obj))
            file.flush()

    def get_blacklist(self, user: str) -> bool:
        with open("blacklist.json") as file:
            obj = json.loads(file.read())
            try:
                return obj[user]
            except:
                return False

    def set_blacklist(self, user: str, what: bool):
        with open("blacklist.json") as file:
            obj = json.loads(file.read())
        obj[user] = what
        with open("blacklist.json", "w") as file:
            file.write(json.dumps(obj))
            file.flush()

    def register_command(self, what: str, handler):
        self.commands[what] = handler
        logging.info("Register command " + what)

    def handle_message(self, message: str):
        curr_command = message.split(" ")[0]

        for i in self.commands:
            if i == curr_command:
                logging.warning("[" + self.get_user() + "] Executing command " + curr_command)
                try:
                    if self.get_blacklist(self.get_user()):
                        return
                    if not len(message.split(" ")) < 1:
                        is_response, what = self.commands[i](self,
                                                             " ".join(message.split(" ")[1:len(message.split(" "))]),
                                                             len(message.split(" ")) - 1)
                    else:
                        is_response, what = self.commands[i](self, None, 0)
                    if is_response:
                        logging.warning("Sending response " + what)
                        self.send_message_current_chat(what)
                except Exception as e:
                    exc = traceback.format_exc()
                    crash_id = str(hex(random.randint(0, 100000000)))

                    crash_report = exc + "\n"
                    crash_report += "User: " + self.get_user() + ", Permissions: " + str(self.get_perms(self.get_user())) + "\n"
                    crash_report += "Command: " + message + "\n"
                    crash_report += "Platform: " + platform.platform() + "\n"
                    crash_report += "Processor: " + platform.processor() + "\n"
                    crash_report += "Machine: " + platform.machine() + "\n"
                    crash_report += "Time: " + str(datetime.now()) + "\n"

                    with open(crash_id, "w") as file:
                        file.write(crash_report)
                        file.flush()

                    user = self.get_user()

                    ws = WhatsAppStyle(self)
                    ws.typewriter("Internal error: " + str(e))
                    ws.fat("Saving crash report: " + crash_id)
                    ws.italic("User: " + user + ", Permissions: " + str(self.get_perms(user)))
                    ws.send()

                    self.select_chat(self.idle_chat)

                    ws.typewriter("Internal error: " + str(e))
                    ws.fat("Saving crash report: " + crash_id)
                    ws.italic("User: " + user + ", Permissions: " + str(self.get_perms(user)))
                    ws.send()

    def mainloop(self):
        while True:
            message = self.wait_for_message()
            user = self.get_user()
            if user is None:
                self.select_chat(self.idle_chat)
                continue
            logging.info(user + " " + message)
            self.handle_message(message)
            self.select_chat(self.idle_chat)


class WhatsAppStyle:
    def __init__(self, w: WhatsApp):
        self.whatsapp = w

    def format_print(self, what: str):
        box = self.whatsapp.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")

        for i in what.split("\n"):
            box.send_keys(i)
            ActionChains(self.whatsapp.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).perform()

    def type(self, what: str):
        box = self.whatsapp.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
        box.send_keys(what)

    def italic(self, what: str):
        self.format_print("_" + what + "_")

    def strikethrough(self, what: str):
        self.format_print("~" + what + "~")

    def fat(self, what: str):
        self.format_print("*" + what + "*")

    def typewriter(self, what: str):
        self.format_print("```" + what + "```")

    def tag(self, who: str):
        box = self.whatsapp.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
        box.send_keys("@" + who + "\t")

    def send(self):
        self.whatsapp.driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()
