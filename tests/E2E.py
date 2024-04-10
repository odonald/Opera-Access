import unittest
import os
import time
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

local_ip = socket.gethostbyname(socket.gethostname())
port_number = 7832

class EndToEndTest(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Set up mobile emulation
        # mobile_emulation = {
        #     "deviceMetrics": {"width": 896, "height": 414, "pixelRatio": 3.0},
        # }
        # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        self.driver = webdriver.Chrome(options=chrome_options)

        #leftovers from exploring headless mode:
        # os.environ["HEADLESS_MODE"] = "1"
        self.tkinter_app_process = os.system("python ../main.py &")
        time.sleep(.5)

    def tearDown(self):
        self.driver.quit()
        os.system("pkill -f main.py")
        #leftovers from exploring headless mode:
        #del os.environ["HEADLESS_MODE"]

    def test_website_is_served(self):
        website_url = f"http://{local_ip}:{port_number}"
        self.driver.get(website_url)
        
        expected_title = "Opera Access"
        self.assertEqual(self.driver.title, expected_title)
        
        expected_button_language = self.driver.find_element(by=By.ID, value="language")
        expected_button_language.click()

        expected_button_toggle = self.driver.find_element(by=By.ID, value="language")
        expected_button_toggle.click()
        
        cssValue = self.driver.find_element(By.ID, "text-size-plus").value_of_css_property('font-size')
        assert cssValue == "32px"

if __name__ == '__main__':
    unittest.main()