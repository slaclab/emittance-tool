from pyemittance import h5_storage
import os
import pytest


@pytest.fixture
def rootdir():
    return os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def example_data(rootdir):
    return h5_storage.loadH5Recursive(f"{rootdir}/data/20210531_180547_EmittanceTool.h5")