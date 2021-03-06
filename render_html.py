import os
from datetime import datetime
import mistune
import pygments.formatters
import pygments.lexers
import pygments.style
import pygments.styles
import pygments.token
from pygments.styles.friendly import FriendlyStyle


POSTS_DIR = os.path.join(os.path.dirname(__file__), 'posts')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'html')

POST_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>

    <body>
        <h1><strong>{title}</strong></h1>
        <ul>
            <li><a href="./index.html">Home</a></li>
            <li><a href="https://github.com/Zaab1t">Github</a></li>
            <li><a href="https://i.redd.it/bka1gb843z7z.jpg">Linkedin</a></li>
            <li><a href="https://www.reddit.com/domain/blog.bordum.dk/">Discussion</a></li>
        </ul>
        <main role="main">
            <article class="content">
            {content}
            </article>
        </main>
    </body>

    <footer>
        <hr>
        <p>&copy; {year} Carl Bordum Hansen</p>
        <p>Contact: <img src="./email.svg"></p>
    </footer>
</html>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Carl Bordum Hansen</title>
    </head>
    <body>
        {links}
    </body>
</html>
"""


class PostRenderer(mistune.Renderer):
    def __init__(self):
        super().__init__()
        self.pygments_style = FriendlyStyle
        self.title = None  # will be set by header

    def header(self, text, level, raw):
        """Because I need the title."""
        if level == 1:
            self.title = text
            return ''  # because the <h1> is already in tempalte
        return super().header(text, level, raw)

    def block_code(self, code, lang=None):
        formatter = pygments.formatters.HtmlFormatter(
            style=self.pygments_style, noclasses=True)
        if lang == 'python':
            if code.startswith('>>> '):
                lexer = pygments.lexers.PythonConsoleLexer(python3=True)
            else:
                lexer = pygments.lexers.Python3Lexer()
        else:
            lexer = pygments.lexers.find_lexer_class_by_name(lang)()
        return pygments.highlight(code, lexer, formatter)


def main():
    renderer = PostRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    markdown_posts = {}
    titles = {}

    for post in os.listdir(POSTS_DIR):
        with open(POSTS_DIR + '/' + post) as f:
            markdown_posts[post] = f.read()

    year = datetime.utcnow().year
    for filename, content in markdown_posts.items():
        with open(OUTPUT_DIR + '/' + filename + '.html', 'w+') as f:
            post = markdown(content)
            titles[filename] = renderer.title
            html = POST_TEMPLATE.format(
                title=renderer.title,
                content=post,
                year=year,    
            )
            f.write(html)

    with open(OUTPUT_DIR + '/' + 'index' + '.html', 'w+') as f:
        links = ['<p><a href="{}.html">{}</a></p>'.format(
            filename, title) for filename, title in titles.items()]
        f.write(INDEX_TEMPLATE.format(links=''.join(links)))


if __name__ == '__main__':
    main()
