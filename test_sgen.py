import sgen
import os
import shutil


def setup_content():
    if os.path.exists(os.path.join(os.getcwd(), 'content_test')):
        shutil.rmtree(os.path.join(os.getcwd(), 'content_test'))

    os.makedirs(os.path.join(os.getcwd(), 'content_test'))

    for blog in [('blog1.md', 13), ('blog2.md', 12)]:
        with open(os.path.join(os.getcwd(), 'content_test', '%s' % blog[0]), 'w') as test_file:
            test_file.write("""Title: Blog1 lololo
Date: 12/12/2012 12:%i

# Article 1

Stuff

qsdsqdsqd

[Link](https://google.com/)
    """ % blog[1])


def cleanup_content():
    if os.path.exists(os.path.join(os.getcwd(), 'content_test')):
        shutil.rmtree(os.path.join(os.getcwd(), 'content_test'))


def test_get_files():
    setup_content()
    assert map(os.path.basename, sgen.find_content(
        content_dir='content_test'
    )) == ['blog1.md', 'blog2.md']
    cleanup_content()


def test_convert_markdown():
    setup_content()
    rv = sgen.compile_html(
        sgen.find_content(
            content_dir='content_test'
        )[0])
    html, meta_tags = rv
    assert 'title' in meta_tags
    assert 'date' in meta_tags
    assert html != ''
    cleanup_content()


def test_make_content():
    setup_content()
    rv = map(sgen.compile_html, sgen.find_content(content_dir='content_test'))
    articles = []
    for html, meta in rv:
        article = sgen.Article(
            html, meta['title'][-1], meta['date'][-1]
        )
        articles.append(article)
    assert articles[0].url == 'blog1-lololo'
    assert articles[1].url == 'blog1-lololo-2'
    assert articles[0].render_html() != ''
    cleanup_content()
