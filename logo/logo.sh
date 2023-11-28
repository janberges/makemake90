#!/bin/bash

w=19
h=11
in=2.54

pdflatex --interaction=batchmode makemake90

convert -density `perl -e "print 640 / ($w / $in)"` makemake90.pdf \
    -flatten PNG8:makemake90.png

convert -density `perl -e "print 640 / ($w / $in)"` makemake90.pdf \
    -background black -gravity center -extent 640x640 PNG8:makemake90_square.png

convert -density `perl -e "print 480 / ($h / $in)"` makemake90.pdf \
    -background black -gravity center -extent 1280x640 PNG8:makemake90_banner.png
