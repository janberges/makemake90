#!/usr/bin/env python3

import numpy as np
import storylines
import sys

black = np.array([0x00, 0x00, 0x00])
white = np.array([0xff, 0xff, 0xff])
orange = np.array([0xff, 0xa5, 0x00])

N = 9

shades = (
    np.linspace(black, white, N),
    np.linspace(black, orange, N),
    np.linspace(white, orange, N))

colors = set(tuple(color) for shade in shades for color in shade)

image = np.array(storylines.load(sys.argv[1]))[:, :, :3]

for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        for shade in shades:
            n = shade[-1] - shade[0]
            n /= np.linalg.norm(n)

            d = image[y, x] - shade[0]

            if np.linalg.norm(d - np.dot(d, n) * n) < 1:
                image[y, x] = min(shade,
                    key=lambda c: np.linalg.norm(c - image[y, x]))
                break
        else:
            image[y, x] = min(colors,
                key=lambda c: np.linalg.norm(c - image[y, x]))

storylines.save(sys.argv[2], image)
