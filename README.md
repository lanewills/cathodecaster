# cathodecaster
This repository holds the code for my CRT-driven guitar, which I nicknamed the Cathode Caster. Read on to see how it works and how to build one yourself.

## What you need
Here are some of the main components I used in my build:
* Raspberry Pi 4 w/ 32gb microSD
* 3.5mm to composite AV cable
* JVC TM-9U(A) CRT TV
* 2x Spectra Symbol 500mm SoftPot
* MCP3008 ADC
* A breadboard, along with a few jumper cables and 10k resistors
* Three buttons
* A fretless guitar neck, and other bits of hardware for attaching it to the CRT body
* A guitar pickup, hooked up to an amplifier

## How to run
Make sure you have the requirements installed, then you can run it like any other Python script with...

```python3 cathodecaster.py```

In my implementation, I added this to my .bashrc and disabled GUI boot, so it's running first thing after boot (just hit ctrl+c to regain control, if needed).

## My build process

Here's a breif overview on how everything is set up:
* The two SoftPot potentiometers are being read by the MCP3008 channels 0 and 7, with a 10k resistor in between to prevent "floating".
* The MCP3008 is connected to the RPi as shown in [this official tutorial](https://projects.raspberrypi.org/en/projects/physical-computing/13).
* The waveform, octave, and string buttons are connected to GPIO 2, 3, and 4, respectively.
* The 3.5mm to composite AV cable is connected to the RPi 3.5mm jack, and the red or white composite audio cables are connected to the CRT video input

As for physical assembly, I used a right angle bracket and a few wood screws for the guitar neck. for the CRT, I was able to remove the enclosure and drill holes for screws. I suppose the benefit of using this larger, less consumer-focused CRT is that the case isn't some weird and difficult shape to work with. The breadboard and RPi are stuck on behind the neck with adhesive and command strips!

For my pickup, the two wires are rather haphazardly soldered onto a 3.5mm jack, which doesn't look the greatest but it works!

## How it works
I tried to make the script as efficient as possible, since this is an instrument and needs to be as responsive as possible.

Upon initalization, base frequencies for all 6 strings are computed and stored in arrays. The root note frequencies can be customized by changing the number where noted at the top of the script.

After this, the MCP3008 constantly polls the potentiometers, and any value above 0.01 will trigger a note. In an effort to make this device more musically usable, the potentiometers are divided up into different notes, as opposed to a direct position/frequency conversion which essentially resulted in a fretless guitar. I also reserved any value <= 0.1 on the potentiometers for the root note, since they hang off the top of the neck a bit and I wanted to make sure the root note was playable. Wouldn't be a personal project without some degree of jankiness.

Now... how do we get audio? Great question that took me far too long to find an answer to. I tried fiddling around with various Python audio libraries but I struggled endlessly to find a solution that would just let me glide between different frequencies on simple wave types. Enter PySineWave. This library was a godsend since it let me set an exact frequency, and it glides between them at whatever rate you specify. So now, all I have to do is poll the potentiometer, get the corresponding frequency in the pre-compued array, and set the sine wave's frequency. I also made a fork of the library that lets me generate sine, square, saw, and triangle waves so I can cycle between them with the waveform button and get different tones.

Speaking of buttons, there are three of them that expand the usage of the Cathode Caster. The GPIO 2 button cycles between waveform types, 1 being sine, 2 square, 3 saw, and 4 triangle. GPIO 3 button changes octaves. 1 is the base octave, and it can go up to octave 5. GPIO 4 button is more experimental, but it swaps guitar strings. For example, the default strings are low E and A, but hitting the button will make them A and D, and again will make them D and G, and so on. It currently doesn't work unless you're on the base octave.

Now, how do we *actually* get audio? Using the 3.5mm to composite cable, all you have to do is hook up one of the audio cables to the video input on the CRT. It shows more/less lines for higher/lower frequencies, respectively. Hold your pickup close to the screen, and you will hear the frequency that's currently playing. How does this work? I have no idea, it just does. Plug your pickup into a pedal for best results (Chroma Console is a fantastic companion)! The cool thing about using a Raspberry Pi for this rather than an Arduino, is that if you have composite output enabled, you can swap the audio/video cable and the CRT works as some cool visuals when not in use.

And that's pretty much it! I still have a few ideas for features I want to implement, and this repo will be updated if I add any of these features.

## Next Steps
### Known issues:
* Strings will not change if the base octave is not selected (I know this is possible but I just don't feel like thinking about the logic at the moment)

### A couple extra features I want to add in the future:
* Fretless mode switch
* Safe shutdown button

### And a few things I would do differently if I were to build another one:
* Use a smaller CRT and add neck strap screws
* Use ThinPot potentiometers for more strings
* See if tapping into the CRT power supply for the RPi is possible to remove the need for two power cables
