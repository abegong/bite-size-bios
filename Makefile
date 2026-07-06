.PHONY: dev build clean

SITE_DIR ?= site
HUGO_CACHEDIR ?= $(CURDIR)/$(SITE_DIR)/resources/_cache
PORT ?= 1313

dev:
	cd $(SITE_DIR) && PATH="./node_modules/.bin:$$PATH" HUGO_CACHEDIR=$(HUGO_CACHEDIR) hugo server -D --port $(PORT) --bind 127.0.0.1

build:
	cd $(SITE_DIR) && PATH="./node_modules/.bin:$$PATH" HUGO_CACHEDIR=$(HUGO_CACHEDIR) hugo --gc --minify --cleanDestinationDir && PATH="./node_modules/.bin:$$PATH" pagefind --site public

clean:
	rm -rf $(SITE_DIR)/public $(SITE_DIR)/resources $(SITE_DIR)/hugo_stats.json $(SITE_DIR)/.hugo_build.lock
	rm -rf public resources hugo_stats.json .hugo_build.lock
