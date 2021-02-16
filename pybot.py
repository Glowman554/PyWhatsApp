from time import sleep

import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WhatsApp:

    def __init__(self, data_dir: str, driver_path: str, idle_chat: str, headless: bool):
        self.commands = {}
        self.idle_chat = idle_chat
        options = Options()

        user_aget = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68"

        options.add_argument("user-data-dir=chrome/" + data_dir)
        options.add_argument(f"user-agent={user_aget}")

        if headless:
            options.add_argument("--headless")
        if driver_path is None:
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome(driver_path, options=options)
        if headless:
            self.driver.set_window_size(1120, 550)

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
                pass

    def get_user(self) -> str:
        try:
            user = self.driver.find_elements_by_xpath("//span[@dir='{}']".format("ltr"))[-1].find_element_by_xpath(
                "./../..").get_attribute("data-pre-plain-text").split("] ")[1].replace(": ", "")
            return user
        except:
            pass

    def register_command(self, what: str, handler):
        self.commands[what] = handler
        logging.info("Register command " + what)

    def handle_message(self, message: str):
        curr_command = message.split(" ")[0]

        for i in self.commands:
            if i == curr_command:
                logging.warning("[" + self.get_user() + "] Executing command " + curr_command)
                is_response, what = self.commands[i](self, message)
                if is_response:
                    logging.warning("Sending response " + what)
                    self.send_message_current_chat(what)

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