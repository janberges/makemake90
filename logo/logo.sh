#!/bin/bash

w=19
h=11
in=2.54

pdflatex --interaction=batchmode logo

convert -density `perl -e "print 640 / ($w / $in)"` logo.pdf \
    -flatten PNG8:logo.png

convert -density `perl -e "print 640 / ($w / $in)"` logo.pdf \
    -background black -gravity center -extent 640x640 PNG8:logo_square.png

convert -density `perl -e "print 640 / ($h / $in)"` logo.pdf \
    -background black -gravity center -extent 1280x640 PNG8:logo_banner.png
