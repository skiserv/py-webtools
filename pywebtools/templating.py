from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(
    directory="templates",
    extensions={"jinja_markdown.MarkdownExtension"},
)
