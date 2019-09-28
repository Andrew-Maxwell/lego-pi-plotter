# lego pi plotter

![Plotter overview](https://i.imgur.com/kPqg3fG.jpg)

During 2018 spring break, I built a simple plotter out of Lego, controlled by a raspberry pi. The mechanism had three axes: Rotate the paper, slide the paper linearly, and raise and lower the pen. Although the motors were not stepper motors and I didn’t have any sensors to record the position of each axis, I managed to achieve a usable level of precision by gearing the motors down and driving them in predefined “steps” which moved the pen a known distance.

![Raspberry pi](https://i.imgur.com/1KtHwle.jpg)

Instead of an NXT (lego controller), I used a Raspberry Pi model B (1st gen) with Pi cobbler, breadboard, and two L293D motor controllers connected to three lego power functions motor connectors. The motors ran off a USB power supply.

![Plotter overview 2](https://i.imgur.com/gxc3ykK.jpg)

I chose a somewhat odd design to fit with the parts I already had. Another design using more parts could have been simpler and more precise. The “R” axis is linear, and works by using wheels (center) to slide a flat work surface back and forth along a rail. The “T” (theta) axis uses a single drive wheel (far left) to rotate that rail around a pivot point. The “Z” axis uses a linear actuator (far right) and a lever to raise and lower the pen.

![T axis detail](https://i.imgur.com/1KVwR4H.jpg)

The T axis motor close up. The worm gear makes for slow movement, allowing for greater precision. The yellow T-shaped piece acts as a stop.

![R axis detail](https://i.imgur.com/V4x35t7.jpg)

The R axis with the work surface removed. The single wheel on the far side of the rail is the drive wheel, while the three on the near side just serve to keep the work surface balanced. Sandpaper taped to the bottom helps to prevent the drive wheel from slipping.

![Z axis detail](https://i.imgur.com/4GT9boB.jpg)

The Z axis uses a linear actuator to precisely raise and lower the pen. I overbuilt this part because I hoped to use the project for milling and/or 3D printing, but milling didn’t work and I didn't have time to try 3D printing.

![Drift test](https://i.imgur.com/Kv6h4qk.png)

Drift was down to about 1mm drift for every 10cm of line in the best case, after careful calibration. (The square above is about 3cm on a side.) In the other photos, the drift was much worse because I didn't take the time to calibrate it properly for those tests.

Here’s the plotter in action. In real time, it took about 4 minutes to draw a smiley face:
[Plotter demo video](https://youtu.be/e8Liu4fvG38)
