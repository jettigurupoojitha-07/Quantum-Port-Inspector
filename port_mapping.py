

from itertools import product


def xor_bits(a, b):
    """Calculate bitwise XOR of two binary strings."""
    return "".join(
        str(int(x) ^ int(y))
        for x, y in zip(a, b)
    )


def create_port_mapping(secret):
    """Create a two-to-one mapping using a hidden 3-bit string."""

    if len(secret) != 3 or any(bit not in "01" for bit in secret):
        raise ValueError("Secret must be a 3-bit binary string.")

    if secret == "000":
        raise ValueError("Secret must be nonzero.")

    mapping = {}
    output_labels = {}

    for bits in product("01", repeat=3):
        x = "".join(bits)
        partner = xor_bits(x, secret)
        pair = tuple(sorted([x, partner]))

        if pair not in output_labels:
            output_labels[pair] = f"OUT-{len(output_labels) + 1}"

        mapping[x] = output_labels[pair]

    return mapping


if __name__ == "__main__":
    test_secret = "101"
    mapping = create_port_mapping(test_secret)

    print("\nPORT-MAPPING SIMULATOR")
    print("=" * 35)
    print("Number of input ports:", len(mapping))
    print("Number of unique outputs:", len(set(mapping.values())))
    print("\nInput Port  |  Output Port")
    print("-" * 30)

    for port in sorted(mapping):
        print(f"    {port}     |  {mapping[port]}")

    counts = {}
    for output in mapping.values():
        counts[output] = counts.get(output, 0) + 1

    assert len(mapping) == 8
    assert len(counts) == 4
    assert all(count == 2 for count in counts.values())

    for x in mapping:
        partner = xor_bits(x, test_secret)
        assert mapping[x] == mapping[partner]

    print("\nSUCCESS: All 8 inputs are mapped.")
    print("SUCCESS: Each output has exactly 2 inputs.")
    print("SUCCESS: The hidden XOR relationship is valid.")
