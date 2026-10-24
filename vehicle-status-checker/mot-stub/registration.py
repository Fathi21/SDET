import re


def check_registration(registration_number):
    # ab12cde should give AB12 CDE
    # AB12 CDE should give AB12 CDE
    # AB12CDEF should give None
    # 1234 ABC should give None
    # ' AB12CDE ' should give AB12 CDE (surrounding whitespace stripped)

    cleaned = registration_number.strip().replace(' ', '').upper()

    if not re.fullmatch(r'[A-Z]{2}[0-9]{2}[A-Z]{3}', cleaned):
        return None

    return f'{cleaned[:4]} {cleaned[4:]}'


if __name__ == "__main__":
    print(check_registration("ab12cde"))     # AB12 CDE
    print(check_registration("AB12 CDE"))    # AB12 CDE
    print(check_registration("AB12CDEF"))    # None
    print(check_registration("1234 ABC"))    # None
    print(check_registration("AB1 2CDE"))    # AB12 CDE
    print(check_registration(" AB12CDE "))   # AB12 CDE