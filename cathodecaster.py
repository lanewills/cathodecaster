from gpiozero import MCP3008, Button
from pysinewave import SineWave
import math

# Change these for different tunings
base_freq_low_E = 82.41
base_freq_A = 110
base_freq_D = 146.83
base_freq_G = 196
base_freq_B = 246.94
base_freq_E = 329.63


# Generate the frequencies for each string
freq_low_E = [base_freq_low_E * (2 ** (n / 12)) for n in range(20)]
freq_A = [base_freq_A * (2 ** (n / 12)) for n in range(20)]
freq_D = [base_freq_D * (2 ** (n / 12)) for n in range(20)]
freq_G = [base_freq_G * (2 ** (n / 12)) for n in range(20)]
freq_B = [base_freq_B * (2 ** (n / 12)) for n in range(20)]
freq_E = [base_freq_E * (2 ** (n / 12)) for n in range(20)]
activeOctave = 1

# The currently active frequencies for the two potentiometers
string_1 = freq_low_E
string_2 = freq_A

waveButton = Button(2)
octaveButton = Button(3)
stringButton = Button(4)
pot1 = MCP3008(0)
pot2 = MCP3008(7)

sinewave = SineWave(1, pitch=0, pitch_per_second=10000)
squarewave = SineWave(2, pitch=0, pitch_per_second=10000)
sawwave = SineWave(3, pitch=0, pitch_per_second=10000)
triwave = SineWave(4, pitch=0, pitch_per_second=10000)
current_wave = sinewave
active_wave = 1


# Function to cycle the waveform
def change_waveform():
    global current_wave
    global active_wave

    if active_wave == 1:
        current_wave = squarewave
        active_wave = 2
    elif active_wave == 2:
        current_wave = sawwave
        active_wave = 3
    elif active_wave == 3:
        current_wave = triwave
        active_wave = 4
    elif active_wave == 4:
        current_wave = sinewave
        active_wave = 1
    print(f"Waveform changed to {active_wave}")


# Increases the octave of the active strings, up to 4 octaves
def change_octave():
    global activeOctave
    global string_1
    global string_2

    if activeOctave < 5:
        activeOctave += 1
        string_1 = [x * 2 for x in string_1]
        string_2 = [x * 2 for x in string_2]
    else:
        activeOctave = 1
        string_1 = freq_low_E
        string_2 = freq_A
    print(f"Octave changed to {activeOctave}")


# Rotates the active strings, cycling through the 6 strings of a guitar
# For example, if the active strings are E and A, this will change them to A and D
def change_string():
    global string_1
    global string_2

    if string_1 == freq_low_E:
        string_1 = freq_A
        string_2 = freq_D
    elif string_1 == freq_A:
        string_1 = freq_D
        string_2 = freq_G
    elif string_1 == freq_D:
        string_1 = freq_G
        string_2 = freq_B
    elif string_1 == freq_G:
        string_1 = freq_B
        string_2 = freq_E
    elif string_1 == freq_B:
        string_1 = freq_E
        string_2 = freq_low_E
    elif string_1 == freq_E:
        string_1 = freq_low_E
        string_2 = freq_A
    print(f"Strings changed to {string_1[0]} and {string_2[0]}")


waveButton.when_pressed = change_waveform
octaveButton.when_pressed = change_octave
stringButton.when_pressed = change_string


def pot_to_freq(value, string):
    freq = 0

    if string == 1:
        # Potentiometers hang off the top a bit, so to compensate I have space reserved for root notes.
        if value <= 0.1:
            freq = string_1[0]
        elif value >= 1:
            freq = string_1[19]
        else:
            freq = string_1[int((value - 0.1) / 0.9 * (19)) + 1]
    elif string == 2:
        if value <= 0.1:
            freq = string_2[0]
        elif value >= 1:
            freq = string_2[19]
        else:
            freq = string_2[int((value - 0.1) / 0.9 * (19)) + 1]

    return freq


def main():
    while True:
        try:
            val1 = pot1.value
            val2 = pot2.value
            if val1 > 0.01:
                current_wave.play()
                freq = pot_to_freq(val1, 1)
                current_wave.set_frequency(freq)
                print(f"{val1} received from pot 1. playing frequency {freq}")
            elif val2 > 0.01:
                current_wave.play()
                freq = pot_to_freq(val2, 2)
                current_wave.set_frequency(freq)
                print(f"{val2} received from pot 2. playing frequency {freq}")
            else:
                current_wave.stop()

        except KeyboardInterrupt:
            print("keyboard interrupt detected, quitting.")
            exit()


main()
