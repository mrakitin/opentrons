import pytest
import os
from tests.opentrons.conftest import data_dir
from opentrons.hardware_control.g_code_parsing.protocol_runner import ProtocolRunner
from opentrons.hardware_control.g_code_parsing.g_code_program.supported_text_modes \
    import SupportedTextModes
from opentrons.hardware_control.emulation.settings import \
    Settings, SmoothieSettings, PipetteSettings

CONFIG = Settings(
    host='0.0.0.0',
    smoothie=SmoothieSettings(
        left=PipetteSettings(model='p20_single_v2.0', id='P20SV202020070101'),
        right=PipetteSettings(model='p20_single_v2.0', id='P20SV202020070101')
    )
)

PROTOCOL_PATH = os.path.join(
    data_dir(), 'g_code_validation_protocols', 'smoothie_protocol.py'
)


@pytest.fixture
def protocol_runner() -> ProtocolRunner:
    return ProtocolRunner(CONFIG)


async def test_watcher_command_list_is_cleared(protocol_runner: ProtocolRunner):
    """
    If everything is cleaning up correctly then 2 runs of the same protocol
    should return the same exact G-Code
    """
    with protocol_runner.run_protocol(PROTOCOL_PATH) as run_1:
        run_1_desc = run_1.get_text_explanation(SupportedTextModes.G_CODE)
    with protocol_runner.run_protocol(PROTOCOL_PATH) as run_2:
        run_2_desc = run_2.get_text_explanation(SupportedTextModes.G_CODE)

    assert run_1_desc == run_2_desc
