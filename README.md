# Software Development and Testing Newsletter
Monthly (more or less!) newsletter of software testing and development topics.

See all issues online here: **[https://swtest.workshopmultimedia.com/](https://swtest.workshopmultimedia.com/)**

## Process for generating newsletter
Each monthly newsletter is generated from a custom Python static generator script using a [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/) template. The various sections of the newsletter are contained in individual [YAML](https://github.com/yaml/pyyaml/) files in `/data` subdirectory with this structure:
```yaml
- type:
  title:
  url:
  content: |
```
These are formatted, including converting the `content` dictionary item from Markdown to HTML via the Python [Markdown](https://github.com/Python-Markdown/markdown) library.

After each of the sections has been processed, they are sent to a master template (`/templates/base.html`) for rendering via Jinja and the final rendered version is saved as an HTML file ready for distribution.