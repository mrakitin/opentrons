"""OtApplication class."""
import logging
from subprocess import Popen
from pathlib import Path
import time
import json
import os

logger = logging.getLogger(__name__)


class OtApplication:
    """Describe and manage the Opentrons application."""

    def __init__(
        self,
        executable_path: Path = Path(os.getenv("EXECUTEABLE_PATH")),
        config_path: Path = Path(os.getenv("CONFIG_PATH")),
    ) -> None:
        """Initialize the Application."""
        self.executable_path: Path = executable_path
        self.config_path: Path = config_path
        logger.info(f"executable path = {self.executable_path}")
        logger.info(f"config path = {self.config_path}")
        self.process: Popen = None
        self.start_modtime: float = None
        self.read_config()

    def read_config(self) -> None:
        """Read the configuration file into a dictionary."""
        try:
            with open(self.config_path) as config_file:
                self.config = json.load(config_file)
        except Exception as exception:  # pylint: disable=W0703
            logger.exception(exception)
        self.start_modtime = os.path.getmtime(self.config_path)

    def alive(self) -> bool:
        """Is the process running the executable alive?"""
        if self.process is not None:
            return self.process.poll
        return False

    def start(self) -> None:
        """Start the Opentrons executable."""
        if self.alive():
            pass
        self.process = Popen([self.executable_path])  # pylint: disable=R1732
        time.sleep(2)  # wait until we see render in the log???

    def stop(self) -> None:
        """Stop the Opentrons executable."""
        if self.process:
            self.process.kill()

    def is_config_modified(self) -> None:
        """Has the config file been modified since the last time we loaded it?"""
        return self.start_modtime != os.path.getmtime(self.config_path)

    def write_config(self) -> None:
        """Write the config property to the config file."""
        try:
            with open(self.config_path, "w") as config_file:
                # make it look like the format teh app uses
                data = json.dumps(self.config, indent=4).replace("    ", "\t")
                config_file.write(data)
        except Exception as exception:  # pylint: disable=W0703
            logger.exception(exception)
        self.start_modtime = os.path.getmtime(self.config_path)
