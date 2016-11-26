import glob
import os
import markdown
import htmlmin
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from sconfig import THEME_DIR
from colorama import init as colorama_init, Fore
from math import ceil
import shutil


colorama_init(autoreset=True)

try:
    from sconfig import *
except ImportError:
    pass


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

try:
    from sconfig import PAGINATOR_MAX
    per_page = PAGINATOR_MAX
except ImportError:
    per_page = 20

    
env = Environment(
    loader=FileSystemLoader(os.path.join(os.getcwd(), THEME_DIR)))

env.globals = dict(env.globals.items() + globals().items())


class Blogger(object):
    def render_html(self):
        """
        Override this method
        """

    def save_page(self):
        with open(os.path.join(self.output_dir, self.page_url), 'w') as myfile:
            myfile.write(self.render_html())


class Paginator(object):
    def __init__(self, curr_page, articles, per_page):
        self.curr_page = curr_page
        self.articles = articles
        self.per_page = per_page

    def pages(self):
        return int(ceil(len(self.articles) / float(self.per_page)))

    def has_prev(self):
        return self.curr_page > 1

    def has_next(self):
        return self.curr_page < self.pages()

    def page_content(self):
        return self.articles[(self.curr_page - 1) * self.per_page:
                             self.curr_page * self.per_page]

    def next(self):
        if self.has_next():
            return str(self.curr_page + 1)

    def previous(self):
        if self.has_prev():
            if self.curr_page == 2:
                return ''
            return str(self.curr_page - 1)


class Blog(Blogger):
    ARTICLES = []
    page_url = 'index.html'

    def __init__(self, output_dir):
        self.output_dir = output_dir

    def add_article(self, article):
        self.ARTICLES = sorted(self.ARTICLES + [article], key=lambda x: x.date)

    def render_html(self, paginator):
        template = env.get_template('index.html')
        return template.render(paginator=paginator)

    def save_page(self):
        self.ARTICLES = self.ARTICLES[::-1]
        for page in range(1,
                          int(ceil(len(self.ARTICLES) / float(per_page))) + 1):
            paginator = Paginator(page, self.ARTICLES, per_page)
            if (page != 1):
                self.page_url = 'index%i.html' % page
            with open(os.path.join(self.output_dir, self.page_url),
                      'w') as myfile:
                myfile.write(self.render_html(paginator))


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
            article_date=self.date.strftime('%d/%m/%Y %H:%M'))


def find_content(**kwargs):
    content_dir = kwargs.get('content_dir', 'content/')
    # returns all markdown files.
    return sorted(glob.glob(os.path.join(content_dir, '*.md')))


def compile_html(content_path):
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(open(content_path, 'r').read())

    return htmlmin.minify(html), md.Meta


if not os.path.exists(os.path.join(os.getcwd(), output_dir)):
    print '[*] Making %s.' % output_dir
    os.makedirs(os.path.join(os.getcwd(), output_dir))

blog = Blog(output_dir)


print Fore.YELLOW + '[*] Cleaning output dir.'

if os.path.exists(os.path.join(os.getcwd(), output_dir)):
    shutil.rmtree(os.path.join(os.getcwd(), output_dir))
    os.mkdir(os.path.join(os.getcwd(), output_dir))

print Fore.YELLOW + '[*] Buidling content.'

for content in find_content(content_dir='content'):
    html_content, meta_content = compile_html(content)
    article = Article(
        html_content,
        title=meta_content['title'][0],
        date=meta_content['date'][0],
        output_dir=output_dir)

    article.save_page()
    blog.add_article(article)

print Fore.YELLOW + '[*] Linking the index.'
blog.save_page()

if os.path.exists(os.path.join(os.getcwd(), THEME_DIR, 'assets')):
    print Fore.YELLOW + '[*] Copying static files.'
    shutil.copytree(os.path.join(os.getcwd(), THEME_DIR, 'assets'),
                    os.path.join(os.getcwd(), output_dir, 'assets'))

