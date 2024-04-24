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
* A guitar pickup, hooked up to an amplifier

## How to use
Make sure you have the requirements installed, then you can run it like any other Python script with...

```python3 cathodecaster.py```

In my implementation, I added this to my .bashrc and disabled GUI boot so it's running first thing after boot (just hit ctrl+c to regain control, if needed).

## How it works
I tried to make the script as efficient as possible, since this is an instrument and needs to be as responsive as possible.

Upon initalization, frequencies for both strings are computed and stored in arrays. The root note frequency can be customized by changing the number where noted at the top of the script.

After this, the MCP3008 constantly polls the potentiometers, and any value above 0.01 will trigger a note. In an effort to make this device more musically usable, the potentiometers are divided up into different notes, as opposed to a direct position/frequency conversion which essentially resulted in a fretless guitar. I also reserved any value <= 0.1 on the potentiometers for the root note, since they hang off the top of the neck a bit and I wanted to make sure the root note was playable. Wouldn't be a personal project without some degree of jankiness.

Now... how do we get audio? Great question that took me far too long to find an answer to. I tried fiddling around with various Python audio libraries but I struggled endlessly to find a solution that would just let me glide between different frequencies on simple wave types. Enter PySineWave. This library was a godsend since it let me set an exact frequency, and it glides between them at whatever rate you specify. So now, all I have to do is poll the potentiometer, get the corresponding frequency in the pre-compued array, and set the sine wave's frequency. I also made a fork of the library that instead generates square waves for a bit more of a crunchy sound.

Now, how do we *actually* get audio? Using the 3.5mm to composite cable, all you have to do is hook up one of the audio cables to the video input on the CRT. It shows more/less lines for higher/lower frequencies, respectively. Hold your pickup close to the screen, and you will hear the frequency that's currently playing. How does this work? I have no idea, it just does. The cool thing about using a Raspberry Pi for this rather than an Arduino, is that if you have composite output enabled, you can swap the audio/video cable and the CRT works as some cool visuals when not in use.

And that's pretty much it! I still have a few ideas for features I want to implement, and this repo will be updated if I add any of these features.

## Next Steps
A couple extra features I want to add in the future:
* Octave switching
* Waveform switching
* Fretless mode switch
* Safe shutdown button
