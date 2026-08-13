def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(value, maximum))


def binary_score(condition):
    return 100 if condition else 0


def range_score(value, minimum, ideal_min, ideal_max, maximum):
    """
    Convert a numeric feature into a 0-100 score.

    Best score is achieved inside the ideal range.
    """

    if value <= minimum:
        return 0

    if ideal_min <= value <= ideal_max:
        return 100

    if value < ideal_min:
        return (
            (value - minimum)
            / (ideal_min - minimum)
        ) * 100

    if value > ideal_max:
        return max(
            0,
            (
                (maximum - value)
                / (maximum - ideal_max)
            ) * 100
        )

    return 0