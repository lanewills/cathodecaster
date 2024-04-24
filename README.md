# cathodecaster
This repository holds the code for my CRT-driven guitar, which I nicknamed the Cathode Caster. Read on to see how it works and how to build one yourself.

## What you need
Here are some of the main components I used in my build:
* Raspberry Pi 4 w/ 32gb microSD
* 3.5mm to composite AV cable
* JVC TM-9U CRT TV
* 2x Spectra Symbol 500mm SoftPot
* MCP3008 ADC
* A breadboard, along with a few jumper cables and 10k resistors
* A fretless guitar neck, and other bits of hardware for attaching it to the CRT body

## How to use
Make sure you have the requirements installed, then you can run it like any other Python script with...

```python3 cathodecaster.py```

In my implementation, I added this to my .bashrc and disabled GUI boot so it's running first thing after boot.

## How it works
I tried to make the script as efficient as possible, since this is an instrument and needs to be as responsive as possible.
Upon initalization, frequencies for both strings are computed and stored in arrays. The root note frequency can be customized by changing the number where noted at the top of the script.
After this, the MCP3008 constantly polls the potentiometer, and any value above 0.01 will trigger a note.

