from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from commands import *
from whatsapp import *

options = Options()
options.add_argument("user-data-dir=chrome/.")

driver = webdriver.Chrome("chromedriver.exe", options=options)
driver.get("https://web.whatsapp.com/")
driver.maximize_window()

while not goto_idle(driver):
    sleep(0.2)

register_command("!ping", ping_command)
register_command("!wikipedia", wikipedia_command)
register_command("!help", help_command)
register_command("!hello", hello_command)
register_command("!say", say_command)

mainloop(driver)
