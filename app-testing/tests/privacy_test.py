"""Tests for privacy toggle."""
import platform
import time
from pathlib import Path
from applitools.images.eyes import Eyes

import pyautogui
from PIL import Image

from src.ot_region import OtRegion
from src.ot_application import OtApplication
from src.locators import Locators


def test_tutorial(eyes: Eyes, ot_application: OtApplication) -> None:
    """Make sure that you can toggle."""
    # make sure analytics in the right state
    ot_application.config["analytics"]["optedIn"] = False
    # popup wont appear
    ot_application.config["analytics"]["seenOptIn"] = True
    ot_application.write_config()
    eyes.open("ot", "Privacy Toggle")
    ot_application.start()
    ot_region: OtRegion = OtRegion()
    locators: Locators = Locators(ot_region)
    # make sure window is active
    pyautogui.click(x=locators.top_bar_center().x, y=locators.top_bar_center().y)
    img_path = Path(f"results/{platform.system()}-startup.png")
    pyautogui.screenshot(img_path, region=ot_region.screenshot_region)
    # Visual checkpoint #1.
    eyes.check_image(Image.open(img_path))
    # click the more menu
    pyautogui.click(x=locators.more_menu().x, y=locators.more_menu().y)
    time.sleep(1)
    img_path_more = Path(f"results/{platform.system()}-more.png")
    pyautogui.screenshot(img_path_more, region=ot_region.screenshot_region)
    # Visual checkpoint #2.
    eyes.check_image(Image.open(img_path_more))
    # click the privacy toggle
    pyautogui.click(x=locators.privacy_toggle().x, y=locators.privacy_toggle().y)
    time.sleep(0.5)
    # visual checkpoint #3.
    img_path_privacy = Path(f"results/{platform.system()}-privacy.png")
    pyautogui.screenshot(img_path_privacy, region=ot_region.screenshot_region)
    eyes.check_image(Image.open(img_path_privacy))
    assert ot_application.is_config_modified()
    eyes.close(False)
