
from simon_solver import run_simon
from simon_recovery import recover_secret, dot_product_mod2
from port_mapping import create_port_mapping, xor_bits


SECRETS = [
    "001", "010", "011", "100", "101", "110", "111"
]


def test_secret(secret):
    # Run the actual quantum circuit.
    circuit, counts = run_simon(secret, shots=2048)

    # Recover the secret using measurement results only.
    recovered = recover_secret(counts)

    # Verify recovery.
    assert recovered == secret, (
        f"Expected {secret}, recovered {recovered}"
    )

    # Verify the orthogonality condition.
    for y, count in counts.items():
        if count > 0:
            assert dot_product_mod2(y, recovered) == 0, (
                f"Invalid measurement {y} for secret {recovered}"
            )

    # Verify the two-to-one port mapping.
    mapping = create_port_mapping(secret)

    assert len(mapping) == 8
    assert len(set(mapping.values())) == 4

    for x in mapping:
        partner = xor_bits(x, secret)
        assert mapping[x] == mapping[partner]

    return recovered, sum(counts.values())


if __name__ == "__main__":
    print("\nSIMON'S ALGORITHM - VALIDATION SUITE")
    print("=" * 48)

    passed = 0

    for secret in SECRETS:
        try:
            recovered, shots = test_secret(secret)

            print(
                f"PASS | Secret: {secret} | "
                f"Recovered: {recovered} | Shots: {shots}"
            )
            passed += 1

        except Exception as error:
            print(f"FAIL | Secret: {secret} | {error}")

    print("=" * 48)
    print(f"Result: {passed}/{len(SECRETS)} tests passed")

    if passed == len(SECRETS):
        print("ALL TESTS PASSED")
    else:
        print("VALIDATION NEEDS ATTENTION")
