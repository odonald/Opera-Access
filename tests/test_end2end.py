import pyautogui
import time
from config.config import AppConfig
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)

initial_mouse_position = pyautogui.position()
print(f"Initial mouse position: {initial_mouse_position}")

time.sleep(.5)

def test_import_text_button():
        
        button_x = 90
        button_y = 150
        pyautogui.click(button_x, button_y)

        dialog_image = "tests/pyautogui_img/test_select_language_box.png"  
        dialog_location = pyautogui.locateOnScreen(dialog_image, confidence=0.8)
        assert dialog_location is not None, "Import Language Dialog not found on the screen"

def test_languages_list():

        english_x = 95
        english_y = 250
        pyautogui.click(english_x, english_y)

        languages_list_image = "tests/pyautogui_img/test_languages_list.png"  
        languages_list_location = pyautogui.locateOnScreen(languages_list_image, confidence=0.8)
        assert languages_list_location is not None, "Import Language Dialog not found on the screen"

def test_import_button():

        import_button_x = 125
        import_button_y = 450
        pyautogui.click(import_button_x, import_button_y)

        time.sleep(.5)
        file_x = 1145
        file_y = 315
        pyautogui.click(file_x, file_y)

        open_button_x = 1245
        open_button_y = 630
        pyautogui.click(open_button_x, open_button_y)
        
        time.sleep(.5)
        next_button_x = 680
        next_button_y = 475
        pyautogui.doubleClick(next_button_x, next_button_y)

        pyautogui.moveTo(initial_mouse_position)
        print(f"Mouse moved back to the initial position: {initial_mouse_position}")

        time.sleep(.1)

def test_text_on_website():
    try:
        driver.get(AppConfig.URL)
        expected_text = "Line 1"
        WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{expected_text}')]")))
        assert True, "Line of text found on the website"

    except:
        assert False, "Line of text wasn't sent to website"

    finally:
        driver.quit()