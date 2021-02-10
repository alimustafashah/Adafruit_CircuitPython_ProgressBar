# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`progressbar`
================================================================================

Dynamic progress bar widget for CircuitPython displays


* Author(s): Brent Rubell

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from . import ProgressBarBase


# pylint: disable=too-many-arguments, too-few-public-methods
class ProgressBar(ProgressBarBase):
    """A dynamic progress bar widget.

    :param x: The x-position of the top left corner.
    :type x: int
    :param y: The y-position of the top left corner.
    :type y: int
    :param width: The width of the progress bar.
    :type width: int
    :param height: The height of the progress bar.
    :type height: int
    :param progress: The percentage of the progress bar.
    :type progress: float
    :param bar_color: The color of the progress bar. Can be a hex
        value for color.
    :param outline_color: The outline of the progress bar. Can be a hex
        value for color.
    :type outline_color: int
    :param stroke: Used for the outline_color
    :type stroke: int
    """

    # pylint: disable=invalid-name
    def __init__(
        self,
        x,
        y,
        width,
        height,
        progress=0.0,
        bar_color=0x00FF00,
        outline_color=0xFFFFFF,
        stroke=1,
    ):

        # This needs to remain, since for backward compatibility, the default ProgressBar class
        # should only be able to handle values of type "float"
        assert isinstance(progress, float), "Progress must be a floating point value."

        super().__init__(
            (x, y),
            (width, height),
            progress,
            bar_color,
            0xAAAAAA,
            0x444444,
            border_thickness=stroke,
            show_margin=True,
            value_range=(0.0, 1.0),
        )

    @property
    def progress(self):
        return ProgressBarBase.progress.fget(self)

    @progress.setter
    def progress(self, value):
        """Draws the progress bar

        :param value: Progress bar value.
        :type value: float
        """
        assert value <= 1.0, "Progress value may not be > 100%"
        assert isinstance(
            value, float
        ), "Progress value must be a floating point value."

        ProgressBarBase.progress.fset(self, value)

    @property
    def fill(self):
        """The fill of the progress bar. Can be a hex value for a color or ``None`` for
        transparent.
        """
        return self._palette[0]

    @fill.setter
    def fill(self, color):
        """Sets the fill of the progress bar. Can be a hex value for a color or ``None`` for
        transparent.
        """
        if color is None:
            self._palette[2] = 0
            self._palette.make_transparent(0)
        else:
            self._palette[2] = color
            self._palette.make_opaque(0)

    def render(self, _previous_value, _new_value, _progress_value):
        """
        The rendering mechanism to display the newly set value.

        :param _previous_value:  The value from which we are updating
        :type _previous_value: object
        :param _new_value: The value to which we are updating
        :type _new_value: object
        :param _progress_value: The value of the progress, or ratio between the new value and the
            maximum value
        :type _progress_value: float
        :return: None
        """
        #         print("Calling 'super().render()' before our own code")
        #         super().render()
        #        print("Calling own 'render()' code")

        if _previous_value > _new_value:
            # uncolorize range from width*value+margin to width-margin
            # from right to left
            _prev_pixel = max(2, int(self.width * self.progress - 2))
            _new_pixel = max(int(self.width * _new_value - 2), 2)
            for _w in range(_prev_pixel, _new_pixel - 1, -1):
                for _h in range(2, self.height - 2):
                    self._bitmap[_w, _h] = 0
        else:
            # fill from the previous x pixel to the new x pixel
            _prev_pixel = max(2, int(self.width * self.progress - 3))
            _new_pixel = min(
                int(self.width * _new_value - 2), int(self.width * 1.0 - 3)
            )
            for _w in range(_prev_pixel, _new_pixel + 1):
                for _h in range(2, self.height - 2):
                    self._bitmap[_w, _h] = 2
