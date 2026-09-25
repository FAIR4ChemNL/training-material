# Contributing

## Technology

This website contains of one page for each event and each training material. Each page contains a mix
of YAML and human-targeted content, mostly just replication of what is in the YAML.

The YAML at the top of each page looks like this:

```yaml
---
layout: default

trainingMaterial:
  "@context": http://schema.org/
  "@type": LearningResource
  "http://purl.org/dc/terms/conformsTo":
    - "@id": "https://bioschemas.org/profiles/TrainingMaterial/1.0-RELEASE"
      "@type": "CreativeWork"
  "@id": https://w3id.org/faircookbook/FCB034
  description: "Like a software license, a data license governs what someone else can do with data that you create or own and that you make accessible to others through, for example, a data repository. Data licenses vary based on different criteria, such as: attribution to original owner; permission to redistribute or modify original; and, inclusion of the same license with derivatives or redistributions. This cookbook recipe will discuss these topics."
  name: Data licenses
  keywords: license
  license: CC-BY 4.0
  url: https://w3id.org/faircookbook/FCB034
---
```

The `keywords` are a comma-separated list (e.g. `keywords: "identifiers, cheminformatics"`) and are used
to create one page per keyword in the [keywords/](keywords/) folder, listing all events and materials
with that keyword. Keywords are matched case-insensitively, so preferably reuse existing keywords
(see [keywords/](keywords/)) rather than introducing new spellings. The keywords and their
frequencies are also written to `_data/keywords.json`, which is used for the keyword cloud
on the front page of the website (see `_includes/keyword-cloud.html`).

The content is converted into the default GitHub Pages content and a bit of Jekyll customization into a webpage.

The extraction of the auto-generated JSON-LD can be tested with
the [schema.org validator](https://validator.schema.org/).

## Adding a new event or material

1. Create a new page with the next free number in the `events/` or `materials/` folder, e.g. `materials/51.md`.
   The easiest way is to copy an existing page and edit it.
2. Fill in the YAML header. For a material, use `"@type": LearningResource` (see the example above);
   for an event, use `"@type": Event`:

   ```yaml
   ---
   layout: default

   trainingMaterial:
     "@context": http://schema.org/
     "@type": Event
     "@id": https://www.nwo.nl/en/meetings/nwo-life2026
     description: "NWO Life is an annual scientific conference for Life scientists that offers inspiration in several ways: enjoy sessions..."
     name: "NWO Life2026"
     url: https://www.nwo.nl/en/meetings/nwo-life2026
   ---
   ```

   The `name` is required: it is used as the title in the index pages. The `keywords` are optional,
   but recommended (see above).
3. Below the YAML header, add the human-readable content: a title, a list with the URL
   (as a Markdown link, e.g. `* URL: [https://example.org/](https://example.org/)`),
   for events also the `When:` and `Where:`, and the description.
4. Update [sitemap.xml](sitemap.xml), [events/index.md](events/index.md), [materials/index.md](materials/index.md)
   and the keyword pages in [keywords/](keywords/) by running:

   ```shell
   make
   ```

   This runs [scripts/update_indexes.py](scripts/update_indexes.py), which creates these files
   from the YAML headers of all pages. The `keywords/` folder is fully generated, so do not edit
   the files in it by hand. It needs Python 3 with [PyYAML](https://pypi.org/project/PyYAML/),
   see [Setting up Python](#setting-up-python) below. Use `make force` to regenerate the files even if
   no page changed, or `make PYTHON=/path/to/python` to use a specific Python.
5. Commit the new page together with the updated index files, keyword pages and sitemap.

## Setting up Python

The script needs Python 3 and the packages listed in [requirements.txt](requirements.txt).
The easiest is to install these in a virtual environment in the `venv` folder of this repository
(which is ignored by git). This only has to be done once:

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

When the `venv` folder exists, `make` automatically uses the Python in it, so there is no need
to activate the virtual environment.
