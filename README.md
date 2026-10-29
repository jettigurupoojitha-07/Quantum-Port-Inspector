## Theoretical Solution and Mathematical Derivation

### 1. Simon's Problem

Let the hidden secret be a nonzero binary string \(s\in\{0,1\}^3\). The port-mapping function \(f\) follows Simon's promise:

\[
f(x)=f(x\oplus s)
\]

where \(\oplus\) represents bitwise XOR. Each output corresponds to exactly two input strings, \(x\) and \(x\oplus s\).

For three-bit inputs, there are \(2^3=8\) possible inputs. Therefore, the mapping contains four distinct output groups, each containing two inputs.

### 2. Quantum Algorithm

Simon's Algorithm uses a quantum circuit to obtain information about the hidden secret.

1. Initialize three input qubits and three output qubits.
2. Apply Hadamard gates to the input qubits to create a superposition of input states.
3. Apply the oracle that implements the promised port-mapping relationship.
4. Apply Hadamard gates to the input register again.
5. Measure the input register to obtain a binary string \(y\).
6. Repeat the measurements and use classical post-processing to recover the secret.

### 3. Mathematical Derivation

The measurement results satisfy the following parity equation:

\[
y\cdot s=0\pmod 2
\]

For three-bit strings, this means:

\[
y_1s_1\oplus y_2s_2\oplus y_3s_3=0
\]

Each measurement produces a linear equation over the binary field \(\mathbb{F}_2\). Multiple independent equations can be combined to identify the unknown secret.

### 4. Worked Example

Consider the secret string:

\[
s=101
\]

The parity condition becomes:

\[
y_1\oplus y_3=0
\]

Therefore, the first and third bits of each valid measurement must be equal.

The possible measurement strings satisfying this condition are:

\[
000,\;010,\;101,\;111
\]

For example:

- \(000\cdot101=0\pmod2\)
- \(010\cdot101=0\pmod2\)
- \(101\cdot101=0\pmod2\)
- \(111\cdot101=0\pmod2\)

The classical recovery stage checks candidate nonzero secrets against the collected equations. When the equations uniquely determine the secret, the algorithm recovers \(s=101\).

### 5. Expected Results

For a valid three-bit Simon oracle:

- There are eight input strings and four output groups.
- Each output group contains two inputs related by XOR with the secret.
- Every valid measured string satisfies \(y\cdot s=0\pmod2\).
- Sufficient independent equations allow the hidden secret to be recovered.

The expected secret must match the secret used to construct the simulated oracle.

## Quantum Simulation and Verification

The project implements the algorithm using Python, Qiskit, and Qiskit Aer. The Streamlit dashboard displays the port mapping, quantum measurement frequencies, circuit, recovered secret, and orthogonality verification.

The `verify_project.py` validation script checks all seven possible nonzero three-bit secrets. The recorded test result was **7/7 passed**, confirming that the simulated recovery matched the selected secret in every tested case.

The simulation runs on a classical computer and demonstrates the algorithm's mathematical behavior; it is not a test on physical quantum hardware.
