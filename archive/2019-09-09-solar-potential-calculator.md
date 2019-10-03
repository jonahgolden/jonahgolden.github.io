---
layout: post
title: Calculate Solar Panel Potential in Python
---


This post will walk through the code and associated math for generating energy predictions for solar panel installations anywhere in the world, including an average power output graph.  For the final script go here, for the jupyter notebook, go here.

### The Power and Energy Equations
The difference between power and energy: 

How much electrical *__power__* can we expect the panels to generate at any given moment?

$P = A \times E \times SI$
* **P** = Power $(W)$
* **A** = Area of Panels $(m^2)$
* **E** = Solar Panel Efficiency (Typically between 0.15 and 0.20), the ratio of solar power turned into electricity.
* **S** = Solar Irradiance $(\frac{W}{m^2})$, the power per area received from the sun.

How much total *__energy__* can we expect the panels to generate over a given period of time?

$E = P \times T$

($L_☉$)



The sun emits a fairly consistent amount of power outwards in all directions.  The amount of power it emits is called solar luminosity (abbreviated as L0 ) and is equal to 3.9×〖10〗^26 watts.  Solar luminosity is emitted in all directions, and for the purposed of this project, it is necessary to determine the power per area that is transmitted from the sun to the Earth.  First, it is useful to picture a giant sphere that surrounds the sun.  This imaginary sphere is the perfect size so that Earth is on its surface.  If we divide the solar luminosity by the surface area of this sphere (in square meters), then we will be able to know the power per square meter that the sun gives to Earth.  The radius of this sphere is equal to the distance of Earth from the sun (1.5×〖10〗^11 m) plus the radius of the sun (6.96×〖10〗^8 m).  Therefore, the radius of the imaginary sphere is 1.50696×〖10〗^11 m.  Surface area (SA) is equal to 4πr^2, so:

$$ SA=4πr^2=4π (1.50696 *10^{11} )^2=2.853732844*10^{23} m^2 $$

### Quest Installation Specs:
#### Panels
Number of panels: 16
Efficiency: 18.7%, at least 89.6% of initial performance after 25 years
Dimensions: 1016mm by 1686 mm
Position: 3 , 8
UID: 503000006535-1
Orientation: vertical
Module name: LG NeON
Module company: LG
Module model: NeON 320
Module type: MONO
STC power: 320


