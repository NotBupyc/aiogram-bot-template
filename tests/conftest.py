import asyncio
import sys
from asyncio import AbstractEventLoop
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent))


@pytest.fixture()
def event_loop() -> AbstractEventLoop:
    """Fixture for event loop."""
    return asyncio.new_event_loop()
