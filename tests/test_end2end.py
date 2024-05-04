import pyautogui
import time
import pytest
from config.config import AppConfig
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Set this scaling factor to adjust for screen resolution and scaling
SCALING_FACTOR = 0.5  # Modify this as needed to find the right factor for your screen
pyautogui.FAILSAFE = True

def apply_scaling(x, y):
    """Applies scaling factor to coordinates."""
    return int(x * SCALING_FACTOR), int(y * SCALING_FACTOR)

@pytest.fixture(scope="session")
def driver():
    """Provides a Selenium WebDriver instance with Chrome Options configured for headless use."""
    chrome_options = Options()
    # Use headless mode for automation
    chrome_options.add_argument("--headless=new")
    with webdriver.Chrome(options=chrome_options) as driver:
        yield driver

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    """Sets up initial conditions once before all tests and cleans up after all tests."""
    initial_mouse_position = pyautogui.position()
    print(f"Initial mouse position: {initial_mouse_position}")
    yield
    pyautogui.moveTo(initial_mouse_position)
    print("Mouse moved back to the initial position after all tests.")

def locate_center_on_screen_with_scaling(image_path, confidence=0.8):
    """Locates the center of an image on screen with scaling adjustment."""
    center = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    if center is None:
        pytest.fail(f"Image not found on screen: {image_path}")
    scaled_x, scaled_y = apply_scaling(center.x, center.y)
    return scaled_x, scaled_y

@pytest.mark.e2e
def test_import_text_button():
    """Tests clicking on the import text button."""
    button_x, button_y = locate_center_on_screen_with_scaling(
        "tests/pyautogui_img/button_image.png")
    pyautogui.click(button_x, button_y)

@pytest.mark.e2e
def test_languages_list():
    """Tests clicking on the languages list."""
    languages_list_x, languages_list_y = locate_center_on_screen_with_scaling(
        "tests/pyautogui_img/test_languages_list.png")
    pyautogui.click(languages_list_x, languages_list_y)

@pytest.mark.e2e
def test_import_button():
    """Tests clicking the import button."""
    import_button_x, import_button_y = locate_center_on_screen_with_scaling(
        "tests/pyautogui_img/test_import_button.png")
    pyautogui.click(import_button_x, import_button_y)

@pytest.mark.e2e
def test_pick_language_file():
    """Tests selecting a language file."""
    time.sleep(1)
    pick_language_file_x, pick_language_file_y = locate_center_on_screen_with_scaling(
        "tests/pyautogui_img/test_pick_language_file.png")
    pyautogui.click(pick_language_file_x, pick_language_file_y)

@pytest.mark.e2e
def test_open_button():
    """Tests clicking the open button."""
    open_button_x, open_button_y = locate_center_on_screen_with_scaling(
        "tests/pyautogui_img/test_open_button.png")
    pyautogui.doubleClick(open_button_x, open_button_y)

@pytest.mark.e2e
def test_next_button():
    """Tests clicking the next button."""
    next_button_x, next_button_y = locate_center_on_screen_with_scaling(
        "tests/pyautogui_img/test_next_button.png")
    pyautogui.doubleClick(next_button_x, next_button_y)
    time.sleep(0.4)

@pytest.mark.e2e
@pytest.mark.usefixtures("driver")
def test_text_on_website(driver):
    """Tests the presence of a specific line of text on a website."""
    driver.get(AppConfig.URL)
    expected_text = "Line 1"
    WebDriverWait(driver, 1).until(EC.presence_of_element_located(
        (By.XPATH, f"//*[contains(text(), '{expected_text}')]")))
