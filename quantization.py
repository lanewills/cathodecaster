import math
# This module contains a function that quantizes a frequency to the nearest note in the 12-tone equal temperament scale.


def quantize(freq):
    # Reference frequency for A4
    a4 = 440

    # Calculate the exact number of semitones relative to A4
    exact_n = 12 * math.log2(freq / a4)
    # Use the ceiling function to always round up unless the frequency is exact
    n = math.ceil(exact_n) if exact_n != round(exact_n) else round(exact_n)
    # Calculate the frequency of the nearest note
    nearest_freq = a4 * (2 ** (n / 12))

    return nearest_freq
