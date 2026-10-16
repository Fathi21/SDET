from datetime import date


def calculate_mot_status(first_registered: date, mot_expiry: date | None) -> str:
    today = date.today()

    three_years_on = first_registered.replace(year=first_registered.year + 3)
    if three_years_on > today:
        return "Not required"

    if mot_expiry is None:
        return "Unknown"  # PQ85 RST case: decision still pending

    if mot_expiry >= today:
        return "Valid"

    return "Expired"