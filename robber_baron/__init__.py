from minizinc import Instance, Model, Solver
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
from typing import Any, Dict, Optional


class Browser:
    def __init__(self, driver: Optional[WebDriver] = None):
        """Create a new browser."""
        self._driver: WebDriver = driver or webdriver.Chrome()

    def get(self, url: str):
        """Get a page by URL."""
        self._driver.get(url)

    def find_element(self, css_selector: str, timeout_seconds: int = 10) -> WebElement:
        """Find an element on the page, waiting for the element to become clickable."""
        return WebDriverWait(self._driver, timeout_seconds).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )

    def find_invisible_element(
        self, css_selector: str, max_retries: int = 10, retry_seconds: int = 1
    ) -> WebElement:
        """Find an invisible element on the page, retrying if the element cannot be found."""
        retries = 0
        while retries < max_retries:
            try:
                return self._driver.find_element_by_css_selector(css_selector)
            except Exception:
                retries += 1
                time.sleep(retry_seconds)
        return None

    def execute_script(self, script: str, *args):
        """Execute JavaScript in the context of the page."""
        self._driver.execute_script(script, *args)

    def select_by_value(self, element: WebElement, value: str):
        """Select an option by value."""
        Select(element).select_by_value(value)

    def request_history(self) -> Any:
        """Return the request history of the browser; requires a selenium-wire driver."""
        return self._driver.requests

    def quit(self):
        """Quit the browser."""
        self._driver.quit()


class ConstraintSolver:
    def __init__(self, solver_tag: str = "gecode"):
        """Create a new constraint solver."""
        self._solver = Solver.lookup(solver_tag)

    def solve(self, model_file: Path, instance_params: Dict[str, Any]) -> Any:
        """Solve an instance of a model."""
        model = Model(model_file)
        instance = Instance(self._solver, model)
        for k, v in instance_params.items():
            instance[k] = v
        return instance.solve()


class Bot:
    def __init__(
        self,
        *,
        browser: Optional[Browser] = None,
        solver: Optional[ConstraintSolver] = None,
    ):
        """Creates a new bot."""
        self.browser = browser or Browser()
        self.solver = solver or ConstraintSolver()

    def login(self):
        """Login to a Puzzle Baron account."""
        username = os.getenv("PB_USERNAME")
        if not username:
            raise ValueError("missing username; please set PB_USERNAME")

        password = os.getenv("PB_PASSWORD")
        if not password:
            raise ValueError("missing password; please set PB_PASSWORD")

        login_url = "https://wordtwist.puzzlebaron.com/"
        print(f"Loading login url: {login_url} ...")
        self.browser.get(login_url)

        print(f"Logging in as: {username} ...")
        self.browser.find_element("input#idLoginUserName").send_keys(username)
        self.browser.find_element("input#idLoginPassword").send_keys(password)
        self.browser.find_element("input#idLoginBtn").click()

        print("Verifying login ...")
        _ = self.browser.find_element("a.loggedin_username")
