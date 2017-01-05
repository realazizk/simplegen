import sys
import glob
import os
sys.path.append(os.getcwd())
import markdown # noqa
import htmlmin # noqa
from datetime import datetime # noqa
from jinja2 import Environment, FileSystemLoader # noqa
from sconfig import THEME_DIR # noqa
from colorama import init as colorama_init, Fore # noqa
from math import ceil # noqa
import shutil # noqa


colorama_init(autoreset=True)

try:
    # dirty but needed to register to the environment scope
    from sconfig import * # noqa
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
    loader=FileSystemLoader(THEME_DIR))

# add the global variable scope to the environment scope
env.globals.update(globals())


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
        """
        Returns the number of pages.
        """
        return int(ceil(len(self.articles) / float(self.per_page)))

    def has_prev(self):
        """
        Does a curr_page have a previous page?
        """
        return self.curr_page > 1

    def has_next(self):
        """
        Does a curr_page have a next page?
        """
        return self.curr_page < self.pages()

    def page_content(self):
        """
        Returns the content that needs to be in some curr_page
        """
        return self.articles[(self.curr_page - 1) * self.per_page:
                             self.curr_page * self.per_page]

    def next(self):
        """
        Returns the name of the next page.
        """
        if self.has_next():
            return str(self.curr_page + 1)

    def previous(self):
        """
        Returns the name of the previous page.
        """
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
        # TODO: can get much better perfomance by just keeping the list of articles sorted
        # sort by date
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
        self.date = date

        # sharing the URLS variable between all article instances and
        # saving all maked slugs, if it already exists just add the number
        # simple mechanism but it works
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
        """
        This just a fancy name for a simple slug method.

        Keyword Arguments:
        title -- the actual title to make a slug
        """
        return '-'.join(title.lower().split())

    def render_html(self):
        # TODO: Change this hardcoded article file name.
        template = env.get_template('article.html')
        return template.render(
            article_content=self.html,
            article_title=self.title,
            article_date=self.date.strftime('%d/%m/%Y %H:%M'))


def find_content(content_dir):
    """
    Returns all markdown files.

    Keyword Arguments:
    content_dir -- the path of the content to make.
    """

    return sorted(glob.glob(os.path.join(content_dir, '*.md')))


def compile_html(content_path):
    """
    Actually compiles the markdown into html files and minfies them.
    Returns a tuple of minfied html and the markdown metadata.

    Keyword Arguments:
    content_path -- the path of the content to make.
    """

    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(open(content_path, 'r').read())

    return htmlmin.minify(html), md.Meta


def remove_it(nodename):
    """
    Removes a nodename, if it's a file it justs removes it,
    if it's a directory it recursively deletes it.

    Keyword Arguments:
    nodename -- the node name
    """

    try:
        os.unlink(nodename)
    except OSError:
        shutil.rmtree(nodename)


def make():
    """
    Makes the stuff baby :)
    """

    if not os.path.exists(output_dir):
        print('[*] Making %s.' % output_dir)
        os.makedirs(output_dir)

    blog = Blog(output_dir)

    print(Fore.YELLOW + '[*] Cleaning output dir.')

    if os.path.exists(output_dir):
        for node in glob.glob(os.path.join(output_dir, '*')):
            remove_it(node)

    print(Fore.YELLOW + '[*] Buidling %i page.' % len(find_content(content_dir=content_dir)))

    for content in find_content(content_dir=content_dir):
        html_content, meta_content = compile_html(content)
        article = Article(
            html_content,
            title=meta_content['title'][0],
            date=meta_content['date'][0],
            output_dir=output_dir)

        article.save_page()
        blog.add_article(article)

    print(Fore.YELLOW + '[*] Linking the index.')
    blog.save_page()

    if os.path.exists(os.path.join(THEME_DIR, 'assets')):
        print(Fore.YELLOW + '[*] Copying static files.')
        shutil.copytree(os.path.join(THEME_DIR, 'assets'),
                        os.path.join(output_dir, 'assets'))
