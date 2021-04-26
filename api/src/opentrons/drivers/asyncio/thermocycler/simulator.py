from typing import Optional

from opentrons.drivers.asyncio.thermocycler.abstract import AbstractThermocyclerDriver
from opentrons.drivers.types import Temperature, PlateTemperature, ThermocyclerLidStatus


class SimulatingDriver(AbstractThermocyclerDriver):

    def __init__(self):
        self._target_temp: Optional[float] = None
        self._ramp_rate: Optional[float] = None
        self._hold_time: Optional[float] = None
        self._lid_status = ThermocyclerLidStatus.OPEN
        self._lid_target: Optional[float] = None

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def is_connected(self) -> bool:
        return True

    async def open_lid(self) -> None:
        self._lid_status = ThermocyclerLidStatus.OPEN

    async def close_lid(self) -> None:
        self._lid_status = ThermocyclerLidStatus.CLOSED

    async def get_lid_status(self) -> ThermocyclerLidStatus:
        return self._lid_status

    async def get_lid_temperature(self) -> Temperature:
        current = 0 if self._lid_target is None else self._lid_target
        return Temperature(current=current, target=self._lid_target)

    async def set_plate_temperature(self, temp: float,
                                    hold_time: Optional[float] = None,
                                    volume: Optional[float] = None) -> None:
        self._target_temp = temp
        self._hold_time = hold_time

    async def get_plate_temperature(self) -> PlateTemperature:
        current = 0 if self._target_temp is None else self._target_temp
        return PlateTemperature(
            current=current, target=self._target_temp, hold=self._hold_time)

    async def set_ramp_rate(self, ramp_rate: float) -> None:
        self._ramp_rate = ramp_rate

    async def set_temperature(self,
                              temp: float,
                              hold_time: float = None,
                              ramp_rate: float = None,
                              volume: float = None) -> None:
        self._target_temp = temp
        self._hold_time = hold_time
        self._ramp_rate = ramp_rate

    async def set_lid_temperature(self, temp: Optional[float]):
        """ Set the lid temperature in deg Celsius """
        self._lid_target = temp

    async def deactivate_lid(self):
        pass

    async def deactivate_block(self):
        pass

    async def deactivate_all(self):
        pass

    async def get_device_info(self):
        return {'serial': 'dummySerialTC',
                'model': 'dummyModelTC',
                'version': 'dummyVersionTC'}

    async def enter_programming_mode(self):
        pass