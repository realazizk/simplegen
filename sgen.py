
import glob
import os
import markdown
import htmlmin
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from sconfig import THEME_DIR

env = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(), THEME_DIR)))


class Article(object):
    URLS = {}

    def __init__(self, html, title, date, **kwargs):
        self.title = title
        self.html = html
        try:
            self.date = datetime.strptime(date, '%d/%m/%Y %H:%M')
        except ValueError:
            raise ValueError('Your date is not well structured')

        sep_title = self.urlizer(self.title)
        if sep_title in self.URLS:
            self.URLS[sep_title] += 1
            self.url = "%s-%i" % (sep_title, self.URLS[sep_title])
        else:
            self.URLS[sep_title] = 1
            self.url = sep_title

    @staticmethod
    def urlizer(title):
        return '-'.join(title.lower().split())

    def render_html(self):
        template = env.get_template('article.html')
        return template.render(
            article_content=self.html,
            article_title=self.title,
            article_date=self.date.strftime('%d/%m/%Y %H:%M')
        )


def find_content(**kwargs):
    content_dir = kwargs.get('content_dir', 'content/')
    return glob.glob(os.path.join(content_dir, '*'))


def compile_html(content_path):
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(
        open(content_path, 'r').read())

    return htmlmin.minify(html), md.Meta


