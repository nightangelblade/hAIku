from jinja2 import Environment, FileSystemLoader


class SiteGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("."))

    def generate_haiku_index(self, haikus: list):
        template = self.env.get_template("template.html")
        output = template.render(haikus=haikus)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(output)
