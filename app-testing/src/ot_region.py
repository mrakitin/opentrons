"""Region class."""
import pygetwindow


class OtRegion:  # pylint: disable=R0903
    """Descripe the region of the screen where the OT app lives."""

    X_OFFSET = 8
    Y_OFFSET = 0
    HEIGHT_OFFSET = -8
    WIDTH_OFFSET = -16

    def __init__(self) -> None:
        """Initialize the region with offsets."""
        self.ot_window = pygetwindow.getWindowsWithTitle("Opentrons")[0]
        self.x_ot_screen_zero = self.ot_window.left + self.X_OFFSET
        self.y_ot_screen_zero = self.ot_window.top + self.Y_OFFSET
        self.ot_screen_height = self.ot_window.height + self.HEIGHT_OFFSET
        self.ot_screen_width = self.ot_window.width + self.WIDTH_OFFSET
        self.screenshot_region = (
            self.x_ot_screen_zero,
            self.y_ot_screen_zero,
            self.ot_screen_width,
            self.ot_screen_height,
        )
