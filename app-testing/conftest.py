"""For pytest."""
import logging
import os
import pytest
from applitools.images import Eyes, BatchInfo
from dotenv import load_dotenv, find_dotenv
from src.ot_application import OtApplication


logger = logging.getLogger(__name__)
# pylint: disable:unused-argument

# Check to see if we have a dotenv file and use it
if find_dotenv():
    load_dotenv(find_dotenv())

logger.info(os.environ)


@pytest.fixture(name="eyes", scope="function")
def eyes_setup() -> Eyes:
    """Basic Eyes setup. It'll abort test if wasn't closed properly."""
    eyes = Eyes()
    eyes.configure.batch = BatchInfo("Demo Batch - Images - Python")
    yield eyes
    # If the test was aborted before eyes.close was called, ends the test as aborted.
    eyes.abort()


@pytest.fixture(name="ot_application", scope="function")
def ot_application() -> OtApplication:
    """Get OT application."""
    application: OtApplication = OtApplication()
    yield application
    application.stop()
