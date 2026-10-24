
from collections import Counter

from port_mapping import create_port_mapping, xor_bits
from simon_solver import run_simon
from simon_recovery import recover_secret, dot_product_mod2


SECRETS = ["001", "010", "011", "100", "101", "110", "111"]

print("\nQUANTUM PORT INSPECTOR - FINAL VALIDATION")
print("=" * 55)

passed = 0

for secret in SECRETS:
    try:
        # Test 1: Check the port mapping.
        mapping = create_port_mapping(secret)

        assert len(mapping) == 8
        assert len(set(mapping.values())) == 4

        output_counts = Counter(mapping.values())
        assert all(count == 2 for count in output_counts.values())

        # Test 2: Check the hidden XOR relationship.
        for x in mapping:
            partner = xor_bits(x, secret)
            assert mapping[x] == mapping[partner]

        # Test 3: Run the actual quantum circuit.
        circuit, counts = run_simon(secret, shots=2048)

        # Test 4: Recover the secret from measurements.
        recovered = recover_secret(counts)
        assert recovered == secret

        # Test 5: Check every measured equation.
        for y, frequency in counts.items():
            if frequency > 0:
                assert dot_product_mod2(y, recovered) == 0

        print(
            f"PASS | Secret={secret} | "
            f"Recovered={recovered} | "
            f"Outputs={len(output_counts)}"
        )
        passed += 1

    except Exception as error:
        print(f"FAIL | Secret={secret} | {error}")

print("=" * 55)
print(f"FINAL RESULT: {passed}/{len(SECRETS)} passed")

if passed == len(SECRETS):
    print("ALL VALIDATION CHECKS PASSED")
else:
    print("REVIEW FAILED TESTS BEFORE SUBMISSION")
