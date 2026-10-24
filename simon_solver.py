
from itertools import product

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def dot_mod2(a, b):
    """Binary dot product, calculated modulo 2."""
    return sum(
        int(x) * int(y) for x, y in zip(a, b)
    ) % 2


def build_simon_circuit(secret):
    """
    Build Simon's circuit for any nonzero 3-bit secret.

    The oracle implements a linear function with kernel
    {000, secret}, so each output has exactly two inputs.
    """
    if (
        len(secret) != 3
        or any(bit not in "01" for bit in secret)
        or secret == "000"
    ):
        raise ValueError("Secret must be a nonzero 3-bit string.")

    # Find two independent binary vectors orthogonal to secret.
    vectors = [
        "".join(bits)
        for bits in product("01", repeat=3)
        if "".join(bits) != "000"
        and dot_mod2("".join(bits), secret) == 0
    ]

    rows = None
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            a, b = vectors[i], vectors[j]

            # Distinct nonzero binary vectors are independent
            # when neither equals the other.
            if a != b:
                rows = [a, b]
                break
        if rows is not None:
            break

    if rows is None:
        raise RuntimeError("Could not construct oracle.")

    # Three input qubits, three output qubits, three measurements.
    qc = QuantumCircuit(6, 3)

    # Step 1: Superposition of all eight inputs.
    qc.h([0, 1, 2])

    # Step 2: Reversible oracle.
    # Qiskit qubit 0 represents the rightmost bit of a
    # conventional 3-bit string, so use secret[row] in reverse.
    for output_index, row in enumerate(rows):
        for input_qubit in range(3):
            if row[2 - input_qubit] == "1":
                qc.cx(input_qubit, 3 + output_index)

    # Step 3: Interference on the input register.
    qc.h([0, 1, 2])

    # Step 4: Measure the input register.
    qc.measure([0, 1, 2], [0, 1, 2])

    return qc


def run_simon(secret, shots=1024):
    """Run the circuit on the local quantum simulator."""
    circuit = build_simon_circuit(secret)
    simulator = AerSimulator()
    compiled = transpile(circuit, simulator)

    result = simulator.run(
        compiled,
        shots=shots
    ).result()

    return circuit, result.get_counts()


if __name__ == "__main__":
    secret = input(
        "Enter a nonzero 3-bit secret (for example, 101): "
    ).strip()

    circuit, counts = run_simon(secret)

    print("\nSIMON QUANTUM CIRCUIT")
    print(circuit.draw(output="text"))

    print("\nMEASUREMENT COUNTS")
    for bitstring, frequency in sorted(counts.items()):
        print(f"{bitstring}: {frequency}")

    print("\nOrthogonality check:")
    for y in counts:
        value = dot_mod2(y, secret)
        print(f"y={y}: y · s mod 2 = {value}")
        assert value == 0

    print("\nSUCCESS: All measured strings satisfy the constraint.")
