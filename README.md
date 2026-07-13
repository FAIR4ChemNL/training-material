# FAIR4ChemNL selected events and training materials

Inventory of events training material for FAIR in Chemistry.

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

The content is converted into the default GitHub Pages content and a bit of Jekyll customization into a webpage.

## Taxila.nl

In combination with the [sitemap.xml](sitemap.xml), each page can be indexed by [Taxila.nl](https://taxila.nl/collections/fair4chemnl).
