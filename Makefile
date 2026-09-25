# Use the virtual environment in venv/ if it exists (see README.md)
PYTHON ?= $(if $(wildcard venv/bin/python),venv/bin/python,python3)

SOURCES := $(filter-out %/index.md,$(wildcard events/*.md materials/*.md))
SCRIPT := scripts/update_indexes.py

.PHONY: all force

# Regenerates sitemap.xml, events/index.md, materials/index.md, keywords/
# and _data/keywords.json
# when any event or material page (or the script) has changed.
all: sitemap.xml

sitemap.xml events/index.md materials/index.md keywords/index.md _data/keywords.json &: $(SOURCES) $(SCRIPT)
	$(PYTHON) $(SCRIPT)

# Regenerate unconditionally
force:
	$(PYTHON) $(SCRIPT)
