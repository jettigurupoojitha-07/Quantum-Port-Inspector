# Quantum Port Inspector
### Quantum Port-Mapping Anomaly Detection Using Simon's Algorithm

## Overview
Quantum Port Inspector is an educational project that demonstrates how Simon's Algorithm can identify a hidden binary relationship in a port-mapping system. The project combines quantum circuit simulation, classical post-processing, and an interactive Streamlit dashboard.

## Problem Statement
A network switch maps 3-bit input ports to output labels under a hidden relationship. Each output corresponds to two inputs, and the paired inputs differ by the same unknown nonzero binary string, called the **secret string**.

The objective is to recover this secret using Simon's Algorithm and verify the measurement condition:

\[
y \cdot s = 0 \pmod 2
\]

where `y` is a measured bitstring and `s` is the hidden secret.

## Objectives
- Simulate a port-mapping function with a hidden binary relationship.
- Implement Simon's quantum algorithm using Qiskit.
- Recover the secret using classical post-processing.
- Verify the orthogonality condition for measurement results.
- Display results through an interactive Streamlit dashboard.

## Technologies Used
- Python
- Qiskit
- Qiskit Aer
- Streamlit
- NumPy
- Pandas
- Plotly

## Project Features
- Interactive secret-string selection.
- Configurable quantum measurement shots.
- Port-mapping table with 8 inputs and 4 output labels.
- Quantum measurement histogram.
- Secret recovery and orthogonality verification.
- Classical post-processing explanation.
- CSV report export.
- Automated validation for all 7 possible nonzero 3-bit secrets.

## Project Structure
```text
PortMappingSimon/
├── app.py
├── port_mapping.py
├── simon_solver.py
├── simon_recovery.py
├── test_simon.py
├── verify_project.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Execution

### 1. Clone the repository
```bash
git clone https://github.com/jettigurupoojitha-07/Quantum-Port-Inspector.git
cd Quantum-Port-Inspector
```

### 2. Create a virtual environment
```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 5. Run the dashboard
```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Validation and Results
The final validation script checks all 7 possible nonzero 3-bit secrets.

The validation checks include:
- 8 input combinations and 4 distinct output labels.
- Each output label occurs exactly twice.
- Inputs related by XOR with the secret share the same output.
- Simon's Algorithm recovers the selected secret.
- Measured bitstrings satisfy the orthogonality condition.

**Recorded validation result: 7/7 secrets passed.**

This result was obtained using the project's local quantum-circuit simulation.

## Limitations
- The quantum circuit is simulated on a classical computer using Qiskit Aer.
- Results depend on the chosen oracle and the Simon promise.
- This educational simulation does not connect to or inspect a real network switch.

## Future Enhancements
- Add a comparison of quantum and classical query counts.
- Improve report export and dashboard visualizations.
- Deploy the dashboard so users can access it online.

## Author
**GitHub:** [jettigurupoojitha-07](https://github.com/jettigurupoojitha-07)

## License
This project is intended for educational and academic demonstration.
