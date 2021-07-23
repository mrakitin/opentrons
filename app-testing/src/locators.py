"""Elements on the screen we will locate with coordinates."""
from dataclasses import dataclass
import platform
from src.ot_region import OtRegion


@dataclass
class Location:
    """Dot annotated class for an x,y location on screen."""

    x: int  # pylint: disable=C0103
    y: int  # pylint: disable=C0103


class Locators:
    """Location of elements onscreen."""

    def __init__(self, ot_region: OtRegion) -> None:
        """Load the region."""
        self.ot_region: OtRegion = ot_region
        self.platform = platform.system()

    def more_menu(self) -> Location:
        """More menu on bottom left."""
        return Location(
            self.ot_region.x_ot_screen_zero + 30,
            self.ot_region.y_ot_screen_zero + self.ot_region.ot_screen_height - 45,
        )

    def privacy_toggle(self) -> Location:
        """Privacy toggle button."""
        locator = {
            "Windows": Location(
                self.ot_region.x_ot_screen_zero + 947,
                self.ot_region.y_ot_screen_zero + 523,
            ),
            "Darwin": Location(
                self.ot_region.x_ot_screen_zero + (1920 / 2),
                self.ot_region.y_ot_screen_zero + (1005 / 2),
            ),
        }
        return locator.get(self.platform)

    def top_bar_center(self) -> Location:
        """Usefull to activate the window."""
        return Location(
            self.ot_region.x_ot_screen_zero + self.ot_region.ot_screen_width / 2,
            self.ot_region.y_ot_screen_zero + 6,
        )
