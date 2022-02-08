# Standard Libraries
from datetime import datetime
import logging
import os
from pprint import (pprint, pformat)
import sys

# Third-Party Libraries
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, Template
from markdown import markdown
import yaml

# Local Libraries

LOG = logging.Logger(name=__name__, level=logging.INFO)

TEMPLATE_FILE_NAME = "base.html"
DOCUMENT_SECTIONS = [
    "quotes",
    "development",
    "testing",
    "tutorials",
    "career",
    "plom",
    "fbom",
    "telecom",
    "utilities",
    "tips",
    "fun"
]


class Newsletter(object):
    """
    Class to build monthly Software Testing and Development
    Newsletter from Jinja template and YAML data files for each
    newsletter section.
    """

    def __init__(self, log_level=logging.INFO):
        self.home_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.home_dir, "data")

        # Configure logging
        LOG.setLevel(log_level)
        str_handler = logging.StreamHandler(stream=sys.stderr)
        file_handler = logging.FileHandler(filename=os.path.join(
            self.home_dir, "{fn}.log".format(fn=__name__)))
        LOG.addHandler(str_handler)
        LOG.addHandler(file_handler)

    def build_newsletter(self):
        """
        Main method to drive newsletter creation process.
        """
        env = Environment(loader=FileSystemLoader(os.path.join(
            self.home_dir, "templates")))
        try:
            template = env.get_template(name=TEMPLATE_FILE_NAME)
        except TemplateNotFound:
            msg = "Unable to find template file '{tf}'!".format(
                tf=TEMPLATE_FILE_NAME)
            LOG.error(msg)
            raise

        # Get data from YAML files for each section.
        data = self.get_data_from_files()

        # Construct top-level template data.
        utcnow = datetime.utcnow()
        data["date"] = utcnow.isoformat("T", "seconds")
        data["newsletter_month"] = utcnow.strftime("%B %Y")

        # Render Jinja template using data.
        rendered_template = template.render(data=data)
        LOG.info("Rendered template output:\n{t}".format(t=rendered_template))

        # Save the newsletter to HTML file.
        newsletter_filename = "{fn}.html".format(
            fn=os.path.join(self.home_dir,
            str(utcnow.strftime("%b%Y")).lower()))
        with open(file=newsletter_filename, mode="w", encoding="utf-8") as html_file:
            html_file.write(rendered_template)
        LOG.info("Newsletter saved to '{f}'.".format(f=newsletter_filename))

    def get_data_from_files(self):
        template_data = dict()

        for section in DOCUMENT_SECTIONS:
            file = os.path.join(self.data_dir, "{s}.yaml".format(s=section))
            template_data[section] = list()
            with open(file, "r") as yaml_file:
                # Load list of dictionaries from YAML file.
                input_data = yaml.safe_load(yaml_file) # yaml.safe_load_all(yaml_file)
                for item in input_data:
                    # If the item contains data, proceed with processing.
                    if item["type"] and item.get("active", True):
                        template_data[section].append(self.parse_input(item))

        return (template_data)

    def parse_input(self, input):
        item = dict()
        # If input is a "Quote"...
        if input["type"].lower() in ["quote"]:
            item["body"] = markdown(input["content"])
            return (item)

        title_template = "{t}"
        # If input is an "Article"...
        if input["type"].lower() in ["article"]:
            title_template = "Article: {t}"
        # Or "Tutorial/Reference"...
        elif ("tutorial" in input["type"].lower()
            or "reference" in input["type"].lower()):
            title_template = input["type"] + ": {t}"

        item["title"] = title_template.format(t=str(input["title"]).strip())
        item["body"] = markdown(input["content"]).replace("<p>", "").replace("</p>", "")
        item["link"] = markdown("[{u}]({u})".format(u=input["url"])).replace("<p>", "").replace("</p>", "")

        return (item)

def main():
    nl = Newsletter()
    nl.build_newsletter()

if __name__ == "__main__":
    main()