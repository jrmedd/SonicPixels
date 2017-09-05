## About

[Micro:bit](http://microbit.org/) and [Max](https://cycling74.com) frameworks for triggering multiple speakers in a grid arrangment. Massively WIP!

Ultimately, this wants to be an easy way of taking OSC/MIDI messages from other software, using Max as a middleware to send serial messages to a [MicroPython](https://github.com/bbcmicrobit/micropython) program running on the micro:bit.

If you want to test the sketches currently here you'll need TouchOSC and Max or Max runtime. You can edit the serial port used by Max by ctrl/cmd+F to find the [serial] object in [sonicPixels.maxpat](https://github.com/jrmedd/SonicPixels/blob/master/sonicPixels.maxpat). You'll need to upload [serialFromUSB.py](https://github.com/jrmedd/SonicPixels/blob/master/serialFromUSB.py) to your micro:bit, and use the [microBitTouchOSC.touchosc](https://github.com/jrmedd/SonicPixels/blob/master/microBitTouchOSC.touchosc) template.

## Overview

_From the original pitch written up by [Cornbrook Creative](http://cornbrookcreative.uk/) and [Noise Orchestra](https://noiseorchestra.org/) for [Manchester Science Festival](http://www.manchestersciencefestival.com/):_

Imagine being a listener at the heart of a dynamic dawn chorus of bird song, the urban soundscape of Manchester City Centre, or the sounds of the Solar System as recorded by NASA’s Voyager missions.

What if these sonic experiences were created not through the conventional mediums of surround sound, ambisonics, complex signal processing and effects - but rather through a matrix of multiple remote-controlled mini speakers arranged in a regular grid - like pixels on a screen.

Like pixels on a screen, this bespoke audio delivery system would allow us to ‘draw’, ‘paint’ and ‘animate’ with sound - to create sonic equivalents of brightness, hue and dynamic texture - not via a carefully pre-arranged multichannel audio composition - but through remote, real-time, algorithmic manipulation of each speaker - each ‘sonic pixel’ - within the grid.

## So far...

...I'm successfully communicating with multiple Micro:bits using OSC messages, via a Max patch and radio:

![OSC to micro:bit demo](https://github.com/jrmedd/SonicPixels/blob/master/docs/in_action.gif?raw=true)

...and I'm now talking to multiple micro:bits on a grid:

![OSC to micro:bit grid](https://github.com/jrmedd/SonicPixels/blob/master/docs/grid_bits.gif?raw=true)

...and I'm creating a better custom interface for doing OSC:

![HTML OSC interface](https://github.com/jrmedd/SonicPixels/blob/master/docs/SP_iPad.gif?raw=true)
