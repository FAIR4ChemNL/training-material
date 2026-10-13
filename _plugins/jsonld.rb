# Writes a JSON-LD file next to the HTML output of each page that has a
# trainingMaterial YAML header: materials/1.md -> _site/materials/1.json.
# The files only exist in the generated site, not in the source.
require "json"

module FAIR4ChemNL
  class JsonLdFile < Jekyll::StaticFile
    def initialize(site, dir, name, data)
      super(site, site.source, dir, name)
      @data = data
    end

    def modified?
      true
    end

    def write(dest)
      path = destination(dest)
      FileUtils.mkdir_p(File.dirname(path))
      File.write(path, JSON.pretty_generate(@data) + "\n")
      true
    end
  end

  class JsonLdGenerator < Jekyll::Generator
    safe true

    def generate(site)
      site.pages.each do |page|
        data = page.data["trainingMaterial"]
        next unless data

        dir = File.dirname(page.path)
        name = File.basename(page.path, ".*") + ".json"
        site.static_files << JsonLdFile.new(site, dir, name, data)
        page.data["jsonld_url"] = "/#{File.join(dir, name)}"
      end
    end
  end
end
