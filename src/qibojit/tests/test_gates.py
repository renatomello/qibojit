import pytest
import numpy as np
from qibo import gates
from qibo.backends import NumpyBackend
from qibojit.tests.utils import qubits_tensor, random_complex, random_state, random_unitary, set_precision

ATOL = {"complex64": 1e-5, "complex128": 1e-10}


@pytest.mark.parametrize(("nqubits", "target", "controls"),
                         [(5, 4, []), (4, 2, []), (3, 0, []), (8, 5, []),
                          (3, 0, [1, 2]), (4, 3, [0, 1, 2]),
                          (5, 3, [1]), (5, 2, [1, 4]), (6, 3, [0, 2, 5]),
                          (6, 3, [0, 2, 4, 5])])
def test_apply_gate(backend, nqubits, target, controls, dtype):
    state = random_state(nqubits, dtype=dtype)
    matrix = random_unitary(1, dtype=dtype)
    gate = gates.Unitary(matrix, target).controlled_by(*controls)

    tbackend = NumpyBackend()
    set_precision(dtype, backend, tbackend)
    target_state = tbackend.apply_gate(gate, np.copy(state), nqubits)
    state = backend.apply_gate(gate, np.copy(state), nqubits)
    backend.assert_allclose(state, target_state, atol=ATOL.get(dtype))


@pytest.mark.parametrize(("nqubits", "target"), [(4, 1), (6, 5)])
@pytest.mark.parametrize("use_qubits", [False, True])
def test_one_qubit_base(backend, nqubits, target, use_qubits, dtype):
    state = random_state(nqubits, dtype=dtype)
    matrix = random_complex((2, 2), dtype=dtype)
    gate = gates.Unitary(matrix, target)

    tbackend = NumpyBackend()
    set_precision(dtype, backend, tbackend)
    target_state = tbackend.apply_gate(gate, np.copy(state), nqubits)
    qubits = qubits_tensor(nqubits, [target]) if use_qubits else None
    state = backend.one_qubit_base(state, nqubits, target, "apply_gate", matrix, qubits)
    backend.assert_allclose(state, target_state, atol=ATOL.get(dtype))


@pytest.mark.parametrize(("nqubits", "target", "controls"),
                         [(3, 0, []), (4, 3, []), (5, 2, []), (3, 1, []),
                          (3, 0, [1]), (4, 3, [0, 1]), (5, 2, [1, 3, 4])])
@pytest.mark.parametrize("pauli", ["X", "Y", "Z"])
def test_apply_pauli_gate(backend, nqubits, target, pauli, controls, dtype):
    state = random_state(nqubits, dtype=dtype)
    gate = getattr(gates, pauli)
    gate = gate(target).controlled_by(*controls)

    tbackend = NumpyBackend()
    set_precision(dtype, backend, tbackend)
    target_state = tbackend.apply_gate(gate, np.copy(state), nqubits)
    state = backend.apply_gate(gate, np.copy(state), nqubits)
    backend.assert_allclose(state, target_state, atol=ATOL.get(dtype))


@pytest.mark.parametrize(("nqubits", "target", "controls"),
                         [(3, 0, []), (3, 2, [1]),
                          (3, 2, [0, 1]), (6, 1, [0, 2, 4])])
def test_apply_zpow_gate(backend, nqubits, target, controls, dtype):
    state = random_state(nqubits, dtype=dtype)
    theta = 0.1234
    gate = gates.U1(target, theta=theta).controlled_by(*controls)

    tbackend = NumpyBackend()
    set_precision(dtype, backend, tbackend)
    target_state = tbackend.apply_gate(gate, np.copy(state), nqubits)
    state = backend.apply_gate(gate, np.copy(state), nqubits)
    backend.assert_allclose(state, target_state, atol=ATOL.get(dtype))


@pytest.mark.parametrize(("nqubits", "targets", "controls"),
                         [(5, [3, 4], []), (4, [2, 0], []), (2, [0, 1], []),
                          (8, [6, 3], []), (3, [0, 1], [2]), (4, [1, 3], [0]),
                          (5, [2, 3], [1, 4]), (5, [3, 1], [0, 2]),
                          (6, [2, 5], [0, 1, 3, 4])])
def test_apply_two_qubit_gate(backend, nqubits, targets, controls, dtype):
    state = random_state(nqubits, dtype=dtype)
    matrix = random_unitary(2, dtype=dtype)
    gate = gates.Unitary(matrix, *targets).controlled_by(*controls)

    tbackend = NumpyBackend()
    set_precision(dtype, backend, tbackend)
    target_state = tbackend.apply_gate(gate, np.copy(state), nqubits)
    state = backend.apply_gate(gate, np.copy(state), nqubits)
    backend.assert_allclose(state, target_state, atol=ATOL.get(dtype))


@pytest.mark.parametrize(("nqubits", "targets"), [(5, [3, 4]), (4, [2, 0])])
@pytest.mark.parametrize("use_qubits", [False, True])
def test_apply_two_qubit_base(backend, nqubits, targets, use_qubits, dtype):
    state = random_state(nqubits, dtype=dtype)
    matrix = random_complex((4, 4), dtype=dtype)
    gate = gates.Unitary(matrix, *targets)
    
    tbackend = NumpyBackend()
    set_precision(dtype, backend, tbackend)
    target_state = tbackend.apply_gate(gate, np.copy(state), nqubits)
    qubits = qubits_tensor(nqubits, targets) if use_qubits else None
    state = backend.two_qubit_base(state, nqubits, targets[0], targets[1], "apply_two_qubit_gate", matrix, qubits)
    backend.assert_allclose(state, target_state, atol=ATOL.get(dtype))


@pytest.mark.parametrize(("nqubits", "targets", "controls"),
                         [(2, [0, 1], []), (3, [0, 2], []), (4, [1, 3], []),
                          (3, [1, 2], [0]), (4, [0, 2], [1]), (4, [2, 3], [0]),
                          (5, [3, 4], [1, 2]), (6, [1, 4], [0, 2, 5])])
def test_apply_swap(backend, nqubits, targets, controls, dtype):
    state = random_state(nqubits, dtype=dtype)
    gate = gates.SWAP(*targets).controlled_by(*controls)

    tbackend = NumpyBackend()
    set_precision(dtype, backend, tbackend)
    target_state = tbackend.apply_gate(gate, np.copy(state), nqubits)
    state = backend.apply_gate(gate, np.copy(state), nqubits)
    backend.assert_allclose(state, target_state, atol=ATOL.get(dtype))


@pytest.mark.parametrize(("nqubits", "targets", "controls"),
                         [(3, [0, 1], []), (4, [2, 0], []), (3, [1, 2], [0]),
                          (4, [0, 1], [2]), (5, [0, 1], [2]), (5, [3, 4], [2]),
                          (4, [0, 3], [1]), (4, [3, 2], [0]), (5, [1, 4], [2]),
                          (6, [1, 3], [0, 4]), (6, [5, 0], [1, 2, 3])])
def test_apply_fsim(backend, nqubits, targets, controls, dtype):
    state = random_state(nqubits, dtype=dtype)
    matrix = random_complex((2, 2), dtype=dtype)
    phi = 0.4321
    gate = gates.GeneralizedfSim(*targets, matrix, phi).controlled_by(*controls)

    tbackend = NumpyBackend()
    set_precision(dtype, backend, tbackend)
    target_state = tbackend.apply_gate(gate, np.copy(state), nqubits)
    state = backend.apply_gate(gate, np.copy(state), nqubits)
    backend.assert_allclose(state, target_state, atol=ATOL.get(dtype))


# TODO: Re-enable tests
@pytest.mark.parametrize(("nqubits", "targets", "controls"),
                         [(3, [0, 1, 2], []), (4, [2, 1, 3], []),
                          (5, [0, 2, 3], []), (8, [2, 6, 3], []),
                          (5, [0, 2, 3, 4], []), (8, [0, 4, 2, 5, 7], []),
                          (7, [0, 2, 4, 3, 6, 5], []), (8, [0, 4, 2, 3, 5, 7, 1], []),
                          (4, [2, 1, 3], [0]), (5, [0, 2, 3], [1]),
                          (8, [2, 6, 3], [4, 7]), (5, [0, 2, 3, 4], [1]),
                          (8, [0, 4, 2, 5, 7], [1, 3]),
                          (10, [0, 4, 2, 5, 9], [1, 3, 7, 8]),
                          #(22, [10, 8, 13], []), (22, [11, 20, 13, 4], []),
                          #(22, [12, 14, 2, 5, 17], []), (22, [0, 12, 4, 3, 16, 21], []),
                          #(22, [0, 14, 20, 13, 5, 17, 21], []),
                          #(22, [12, 17, 3], [10]), (22, [21, 6, 13], [14, 7]),
                          #(22, [0, 20, 3, 14], [1]),
                          #(22, [0, 4, 20, 5, 17], [10, 3]),
                          #(22, [10, 20, 4, 3, 16, 5], [12, 19, 15])
                          ])
def test_apply_multiqubit_gate(backend, nqubits, targets, controls, dtype):
    state = random_state(nqubits, dtype=dtype)
    rank = 2 ** len(targets)
    matrix = random_complex((rank, rank), dtype=dtype)
    gate = gates.Unitary(matrix, *targets).controlled_by(*controls)
    
    tbackend = NumpyBackend()
    set_precision(dtype, backend, tbackend)
    target_state = tbackend.apply_gate(gate, np.copy(state), nqubits)
    state = backend.apply_gate(gate, np.copy(state), nqubits)
    backend.assert_allclose(state, target_state, atol=ATOL.get(dtype))


@pytest.mark.parametrize("gatename", ["H", "X", "Z"])
@pytest.mark.parametrize("density_matrix", [False, True])
def test_gates_on_circuit(backend, gatename, density_matrix):
    from qibo.models import Circuit
    if density_matrix:
        state = random_complex((2, 2))
        state = state + np.conj(state.T)
    else:
        state = random_state(1)

    c = Circuit(1, density_matrix=density_matrix)
    c.add(getattr(gates, gatename)(0))
    
    tbackend = NumpyBackend()
    target_state = tbackend.execute_circuit(c, np.copy(state))
    final_state = backend.execute_circuit(c, np.copy(state))
    backend.assert_allclose(final_state, target_state)


@pytest.mark.parametrize("gatename", ["H", "X", "Z"])
def test_density_matrix_half_calls(backend, gatename):
    state = random_complex((8, 8))
    state = state + np.conj(state.T)
    gate = getattr(gates, gatename)(1)
    
    tbackend = NumpyBackend()
    target_state = tbackend.apply_gate_half_density_matrix(gate, np.copy(state), 3)
    final_state = backend.apply_gate_half_density_matrix(gate, np.copy(state), 3)
    backend.assert_allclose(final_state, target_state)
