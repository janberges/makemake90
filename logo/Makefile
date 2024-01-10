.PHONY: all clean

all: makemake90.pdf makemake90.png makemake90_square.png makemake90_banner.png

%.pdf: %.tex
	pdflatex --interaction=batchmode $*

makemake90.png: makemake90.svg
	inkscape -w 380 -b white -o $@ $<
	python3 optimize.py $@ $@

makemake90_square.png: makemake90.png
	convert $< -background black -gravity center -extent 380x380 $@

makemake90_banner.png: makemake90.png
	convert $< -background black -gravity center -extent 1280x640 $@

clean:
	rm -f *.aux *.log *.pdf *_*.png
