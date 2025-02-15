# Copyright 2020–2021 Cirq on IQM developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the circuit optimization passes.
"""
# pylint: disable=no-self-use

import cirq
from cirq import ops, optimizers
import pytest

from cirq_iqm.iqm_device import MergeOneParameterGroupGates

tol = 1e-10  # numerical tolerance


class TestGateOptimization:
    """Test various circuit optimization techniques."""

    @pytest.mark.parametrize('family', [
        ops.ZZPowGate,
        ops.ISwapPowGate,
    ])
    @pytest.mark.parametrize('a, b', [(0, 0.3), (-0.5, 0.5), (1.0, 2.0), (0.1, -4.1)])
    def test_gate_merging(self, family, a, b):
        """Merging one-parameter group gates."""

        q0, q1 = cirq.NamedQubit('q0'), cirq.NamedQubit('q1')

        c = cirq.Circuit()
        c.append([
            family(exponent=a)(q0, q1),
            family(exponent=b)(q0, q1),
        ])

        MergeOneParameterGroupGates().optimize_circuit(c)
        cirq.optimizers.DropEmptyMoments().optimize_circuit(c)

        if abs((a + b) % MergeOneParameterGroupGates.PERIOD) < 1e-10:
            # the gates have canceled each other out
            assert len(c) == 0
        else:
            # the gates have been merged
            assert len(c) == 1
            expected = MergeOneParameterGroupGates._normalize_par(a + b)
            assert c[0].operations[0].gate.exponent == pytest.approx(expected, abs=tol)


    @pytest.mark.parametrize('family, ex', [
        (cirq.ops.CZPowGate, 0.2),  # diagonal
        (ops.ISwapPowGate, 1),      # swaplike with Rz when ex is an odd integer
        (ops.ISwapPowGate, 3),
        pytest.param(
            ops.ISwapPowGate, 0.6,
            marks=pytest.mark.xfail(strict=True)
        ),
        # diagonal, but currently do not work with EjectZ
        pytest.param(
            ops.ZZPowGate, 0.37,
            marks=pytest.mark.xfail(strict=True, reason='Implementation missing in Cirq.')
        ),
        pytest.param(
            ops.ISwapPowGate, 2,
            marks=pytest.mark.xfail(strict=True, reason='Implementation missing in Cirq.')
        ),
    ])
    def test_eject_z(self, family, ex):
        """Commuting z rotations towards the end of the circuit."""

        q0, q1 = cirq.NamedQubit('q0'), cirq.NamedQubit('q1')

        c = cirq.Circuit()
        c.append([
            cirq.ZPowGate(exponent=0.3)(q0),
            cirq.ZPowGate(exponent=0.8)(q1),
            family(exponent=ex)(q0, q1),
            cirq.MeasurementGate(1)(q0),
            cirq.MeasurementGate(1)(q1),
        ])

        optimizers.EjectZ().optimize_circuit(c)
        cirq.optimizers.DropEmptyMoments().optimize_circuit(c)

        # the ZPowGates have been commuted and canceled
        assert len(c) == 2
