.PHONY: all clean

w = 19
h = 11
in = 2.54

all: makemake90.png makemake90_square.png makemake90_banner.png

%.pdf: %.tex
	pdflatex --interaction=batchmode $*

makemake90.png: makemake90.pdf
	convert -density `perl -e "print 640 / ($(w) / $(in))"` $< \
        -background black -flatten PNG8:$@

makemake90_square.png: makemake90.pdf
	convert -density `perl -e "print 640 / ($(w) / $(in))"` $< \
        -background black -gravity center -extent 640x640 PNG8:$@

makemake90_banner.png: makemake90.pdf
	convert -density `perl -e "print 480 / ($(h) / $(in))"` $< \
        -background black -gravity center -extent 1280x640 PNG8:$@

clean:
	rm -f *.aux *.log *.pdf *.png
