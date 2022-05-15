from pydantic import BaseModel, Field


class LaMetricFrame(BaseModel):
    """Each frame occupies a whole screen of LaMetric Time device at a single time.
    https://help.lametric.com/support/solutions/articles/6000225467-my-data-diy"""

    text: str = Field(
        None,
        description="Text that will be displayed. If it is too long – it will scroll.",
    )
    icon: str = Field(
        None,
        description="Can be an ID of an icon (go to https://developer.lametric.com/icon"
        "s to browse for icons and know their IDs).",
    )


class LaMetricFrames(BaseModel):
    """In some cases you just want to display your data on a LaMetric Time and do it in
    a very simple way.
    https://help.lametric.com/support/solutions/articles/6000225467-my-data-diy"""

    frames: list[LaMetricFrame]
