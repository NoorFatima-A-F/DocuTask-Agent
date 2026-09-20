"""
Tests for Platform Module System and 9-State Lifecycle.
"""

import pytest
import asyncio
from app.platform.modules.manager import ModuleManager
from app.platform.modules.models import ModuleState
from app.platform.kernel.metadata import ModuleMetadata
from app.platform.kernel.versioning import SemanticVersion
from app.platform.kernel.exceptions import ModuleLoadException


class SampleModule:
    def __init__(self):
        self.metadata = ModuleMetadata(
            name="sample_module",
            version=SemanticVersion(1, 0, 0),
            dependencies=[],
            capabilities=["test.capability"],
        )
        self.initialized = False
        self.started = False
        self.stopped = False

    async def initialize(self, context=None):
        self.initialized = True

    async def start(self):
        self.started = True

    async def stop(self):
        self.stopped = True


class DependentModule:
    def __init__(self):
        self.metadata = ModuleMetadata(
            name="dependent_module",
            version=SemanticVersion(1, 0, 0),
            dependencies=["sample_module"],
        )


def test_module_registration_and_lifecycle():
    manager = ModuleManager()
    record = manager.register_module(SampleModule)

    assert record.name == "sample_module"
    assert record.state == ModuleState.REGISTERED

    # Initialize
    asyncio.run(manager.initialize_module("sample_module"))
    assert record.state == ModuleState.INITIALIZED
    assert record.instance.initialized is True

    # Start
    asyncio.run(manager.start_module("sample_module"))
    assert record.state == ModuleState.RUNNING
    assert record.instance.started is True

    # Stop
    asyncio.run(manager.stop_module("sample_module"))
    assert record.state == ModuleState.STOPPED
    assert record.instance.stopped is True


def test_dependent_module_fails_if_dep_not_ready():
    manager = ModuleManager()
    manager.register_module(DependentModule)

    with pytest.raises(ModuleLoadException) as exc_info:
        asyncio.run(manager.initialize_module("dependent_module"))

    assert "depends on 'sample_module' which is not ready" in str(exc_info.value)
