from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from commands import *
from whatsapp import *

options = Options()
options.add_argument("user-data-dir=chrome/.")

driver = webdriver.Chrome("chromedriver.exe", options=options)
driver.get("https://web.whatsapp.com/")
driver.maximize_window()

while goto_idle(driver) != True:
    sleep(0.2)


register_command("!ping", ping)
register_command("!wikipedia", wikipedia)
register_command("!msg", msg)
register_command("!help", help_command)


mainloop(driver)
