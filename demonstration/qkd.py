from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import random


def generate_quantum_key(length: int = 8) -> str:
    
    simulator = AerSimulator()


    max_attempts = 10
    for attempt in range(max_attempts):
        # Alice randomly picks bits and bases
        alice_bits  = [random.randint(0, 1) for _ in range(length)]
        alice_bases = [random.randint(0, 1) for _ in range(length)]

        # Bob randomly picks measurement bases
        #two types of bases: 0 for rectilinear (|0⟩, |1⟩) and 1 for diagonal (|+⟩, |*⟩)
        bob_bases = [random.randint(0, 1) for _ in range(length)]

        key = []

        for i in range(length):
            qc = QuantumCircuit(1, 1)

            # Encode Alice's bit
            if alice_bits[i] == 1:
                qc.x(0)  # Flip qubit to |1⟩

            # Apply Alice's basis (Hadamard for diagonal basis)
            if alice_bases[i] == 1:
                qc.h(0)

            # Apply Bob's measurement basis
            if bob_bases[i] == 1:
                qc.h(0)

            qc.measure(0, 0)

            # Run the circuit on the simulator
            compiled = transpile(qc, simulator)
            result   = simulator.run(compiled, shots=1).result()

            measured_bit = int(list(result.get_counts().keys())[0])

            # Sift key: keep only bits where bases matched
            if alice_bases[i] == bob_bases[i]:
                key.append(str(measured_bit))

        if key:  # Non-empty sifted key — success
            return ''.join(key)

    raise RuntimeError(
        f"Failed to generate a non-empty quantum key after {max_attempts} attempts. "
        "Try increasing the 'length' parameter."
    )
