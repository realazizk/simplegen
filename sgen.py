
import glob
import os
import markdown
import htmlmin
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from sconfig import THEME_DIR
from colorama import init as colorama_init, Fore

colorama_init(autoreset=True)

try:
    from sconfig import OUTPUT_DIR
    output_dir = OUTPUT_DIR
except ImportError:
    output_dir = 'output/'

try:
    from sconfig import CONTENT_DIR
    content_dir = CONTENT_DIR
except ImportError:
    content_dir = 'content/'


env = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(),
                                                       THEME_DIR)))


class Blogger(object):

    def render_html(self):
        """
        Override this method
        """

    def save_page(self):
        with open(os.path.join(self.output_dir, self.page_url), 'w') as myfile:
            myfile.write(self.render_html())


class Blog(Blogger):
    ARTICLES = []
    page_url = 'index.html'

    def __init__(self, output_dir):
        self.output_dir = output_dir

    def add_article(self, article):
        self.ARTICLES = sorted(self.ARTICLES + [article], key=lambda x: x.date)

    def render_html(self):
        template = env.get_template('index.html')
        return template.render(
            articles=self.ARTICLES[::-1]
        )


class Article(Blogger):
    URLS = {}

    def __init__(self, html, title, date, output_dir, **kwargs):
        self.output_dir = output_dir
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
        self.page_url = self.url + '.html'

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
    return sorted(glob.glob(os.path.join(content_dir, '*')))


def compile_html(content_path):
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(
        open(content_path, 'r').read())

    return htmlmin.minify(html), md.Meta


if not os.path.exists(os.path.join(os.getcwd(), output_dir)):
    print '[*] Making %s.' % output_dir
    os.makedirs(os.path.join(os.getcwd(), output_dir))

blog = Blog(output_dir)

print Fore.CYAN + '[*] Buidling content.'

for content in find_content(content_dir='content'):
    html_content, meta_content = compile_html(
        content
    )
    article = Article(html_content, title=meta_content['title'][0],
                      date=meta_content['date'][0], output_dir=output_dir)

    article.save_page()
    blog.add_article(article)

print '[*] Linking the index.'
blog.save_page()
