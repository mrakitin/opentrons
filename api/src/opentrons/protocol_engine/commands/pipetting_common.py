"""Common pipetting command base models."""
from pydantic import BaseModel, Field

from ..types import WellLocation


# todo(mm, 2021-04-02): Does it make sense to split liquid handling requests
# and pipetting requests into this taxonomy? It doesn't necessarily cleanly
# fit what we want to do with pipettes. e.g. it shouldn't be legal to apply an
# offset to a pick_up_tip(), but it should be legal to apply it to an aspirate
# or generic move_to().
class BasePipettingRequest(BaseModel):
    """Base class for pipetting requests that interact with wells."""

    pipetteId: str = Field(
        ...,
        description="Identifier of pipette to use for liquid handling.",
    )
    labwareId: str = Field(
        ...,
        description="Identifier of labware to use.",
    )
    wellName: str = Field(
        ...,
        # FIXME IMMEDIATELY: Single well?
        description="Name of well to use in labware.",
    )


class BaseLiquidHandlingRequest(BasePipettingRequest):
    """Base class for liquid handling requests."""

    volume: float = Field(
        ...,
        # FIXME IMMEDIATELY: Tip maximum volume?
        description="Amount of liquid in uL. Must be greater than 0 and less "
                    "than a pipette-specific maximum volume.",
        gt=0,
    )
    wellLocation: WellLocation = Field(
        ...,
        description="Relative well location at which to perform the operation",
    )

    # todo(mm, 2021-03-26): This class or one of its subclasses should have a
    # field for liquid flow rate in microliters per second.
    # See Opentrons/opentrons#4837 for terminology concerns.


class BaseLiquidHandlingResult(BaseModel):
    """Base properties of a liquid handling result."""

    volume: float = Field(
        ...,
        description="Amount of liquid in uL handled in the operation.",
        gt=0,
    )
