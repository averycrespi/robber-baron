from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def find_element(driver, css_selector: str, timeout_seconds: int = 10):
    """Find an element on the page, waiting for the element to become clickable."""
    return WebDriverWait(driver, timeout_seconds).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )
