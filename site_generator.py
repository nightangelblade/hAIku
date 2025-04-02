from jinja2 import Environment, FileSystemLoader


class SiteGenerator:
    def __init__(self, haikus: list):
        self.env = Environment(loader=FileSystemLoader("."))
        self.haikus = haikus

    def generate(self):
        template = self.env.get_template("template.html")
        output = template.render(haikus=self.haikus)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(output)
