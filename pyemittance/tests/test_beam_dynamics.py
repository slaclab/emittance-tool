import pytest
import numpy as np

from pyemittance.beamdynamics import transferMatrixDrift66


@pytest.mark.parametrize("Ld", [(5)])
def test_transfer_matrix(Ld):

    result_array = transferMatrixDrift66(Ld)

    assert result_array.shape[0] == 6
    assert result_array.shape[1] == 6





