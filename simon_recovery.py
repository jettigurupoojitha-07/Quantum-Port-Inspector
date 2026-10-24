

from itertools import product


def dot_product_mod2(y, s):
    """Calculate y · s modulo 2."""
    return sum(
        int(a) * int(b) for a, b in zip(y, s)
    ) % 2


def recover_secret(measurement_counts):
    """
    Recover the unique nonzero secret consistent with
    all measured bitstrings.
    """
    measurements = [
        y for y, count in measurement_counts.items()
        if count > 0 and any(bit == "1" for bit in y)
    ]

    candidates = [
        "".join(bits)
        for bits in product("01", repeat=3)
        if "".join(bits) != "000"
    ]

    solutions = [
        secret for secret in candidates
        if all(
            dot_product_mod2(y, secret) == 0
            for y in measurements
        )
    ]

    if len(solutions) != 1:
        raise ValueError(
            f"Secret is not uniquely determined. "
            f"Remaining candidates: {solutions}"
        )

    return solutions[0]


if __name__ == "__main__":
    from simon_solver import run_simon

    # The secret is used only to construct the hidden oracle.
    # The recovery function receives only measured counts.
    test_secret = input(
        "Enter the secret used by the oracle (e.g. 110): "
    ).strip()

    _, counts = run_simon(test_secret, shots=1024)

    print("\nQuantum measurement counts:", counts)

    try:
        recovered = recover_secret(counts)
        print("Recovered secret:", recovered)

        for y in counts:
            result = dot_product_mod2(y, recovered)
            print(f"y={y}: y · s mod 2 = {result}")

        print("\nSUCCESS: Secret recovered from measurements.")
    except ValueError as error:
        print("\nMore independent measurements are needed.")
        print(error)
