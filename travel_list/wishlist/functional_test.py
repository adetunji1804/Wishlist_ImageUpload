import selenium
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from django.test import LiveServerTestCase


class TitleTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver
        cls.selenium.implicitly_wait(10)


@classmethod
def tearDownClass(cls):
    cls.selenium.quit()
    super().tearDownClass()


def test_title_shown_on_home_page(self):
    self.selenium.get(self.live_server_url)
    assert "Travel Wishlist" in self.selenium.title


class AddEditPlacesTests(LiveServerTestCase):

    fixture = ["test_places"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def terst_add_new_place(self):
        self.selenium.get(self.live_server_url)  # load home page
        input_name = self.selenium.find_element_by_id(
            "id_name"
        )  # find input textbox. Id was generated by django forms
        input_name.send_keys("Denver")  # enter place name
        add_button = self.selenium.find_element_by_id(
            "add-new-place"
        )  # find the add button
        add_button.click()  # and click it

        # Got to make the test code wait for the server to process the request and for page to reload
        # wait for new element to appear on page
        wait_for_denver = self.selenium.find_element_by_id("place-name-5")

        # assert places from test_places are on page
        assert "Tokyo" in self.selenium.page_source
        assert "New York" in self.selenium.page_source

        # And the new place too
        assert "Denver" in self.selenium.page_source

