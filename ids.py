import json


def generate_cas_numbers(start=1, end=1000):
    cas_numbers = []
    for x in range(start, end + 1):
        for y in range(100):
            x_str = str(x)
            y_str = f"{y:02}"

            base = x_str + y_str

            check_sum = 0
            for i, digit in enumerate(reversed(base)):
                check_sum += int(digit) * (i + 1)
            check_digit = check_sum % 10

            cas_number = f"{x_str}-{y_str}-{check_digit}"
            cas_numbers.append(cas_number)

        if x % 10000 == 0:
            print(f"Generated {x} CAS numbers")
    return cas_numbers


if __name__ == "__main__":
    start_sequence = 5000
    end_sequence = 10000
    generated_cas_numbers = generate_cas_numbers(
        start=start_sequence, end=end_sequence)

    with open('list2.json', 'w') as f:
        json.dump(generated_cas_numbers, f)

    print(f"Generated {len(generated_cas_numbers)} CAS numbers")
