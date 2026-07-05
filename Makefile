.PHONY: dev build clean

HUGO_CACHEDIR ?= $(CURDIR)/resources/_cache
PORT ?= 1313

dev:
	HUGO_CACHEDIR=$(HUGO_CACHEDIR) hugo server -D --port $(PORT) --bind 127.0.0.1

build:
	HUGO_CACHEDIR=$(HUGO_CACHEDIR) hugo --gc --minify

clean:
	rm -rf public resources .hugo_build.lock
