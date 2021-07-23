"""Region class."""
import platform
import pygetwindow


class OtRegion:  # pylint: disable=R0903
    """Descripe the region of the screen where the OT app lives."""

    WINDOWS_X_OFFSET = 8
    WINDOWS_Y_OFFSET = 0
    WINDOWS_HEIGHT_OFFSET = -8
    WINDOWS_WIDTH_OFFSET = -16

    def __init__(self) -> None:
        """Initialize the region with offsets."""
        if platform.system() == "Darwin":
            self.ot_window = pygetwindow.getWindowGeometry("Opentrons")
            print(self.ot_window)
            self.x_ot_screen_zero = self.ot_window[0]
            self.y_ot_screen_zero = self.ot_window[1]
            self.ot_screen_width = self.ot_window[2]
            self.ot_screen_height = self.ot_window[3]

            # retina display means multiply by 2
            self.screenshot_region = (
                self.x_ot_screen_zero * 2,
                self.y_ot_screen_zero * 2,
                self.ot_screen_width * 2,
                self.ot_screen_height * 2,
            )
        elif platform.system() == "Windows":
            self.ot_window = pygetwindow.getWindowsWithTitle("Opentrons")[0]
            self.x_ot_screen_zero = self.ot_window.left + self.WINDOWS_X_OFFSET
            self.y_ot_screen_zero = self.ot_window.top + self.WINDOWS_Y_OFFSET
            self.ot_screen_width = self.ot_window.width + self.WINDOWS_WIDTH_OFFSET
            self.ot_screen_height = self.ot_window.height + self.WINDOWS_HEIGHT_OFFSET

            self.screenshot_region = (
                self.x_ot_screen_zero,
                self.y_ot_screen_zero,
                self.ot_screen_width,
                self.ot_screen_height,
            )
