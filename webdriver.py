import time
from selenium import webdriver

options = webdriver.ChromeOptions()
print("driver créé")
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('start-maximized')
print("options ok")
driver = webdriver.Remote(command_executor='http://192.168.65.4:4444', options=options)
print("webdriver ok")

for x in range(15):
    time.sleep(60)
    driver.current_url
    print(f"Tour {x}")