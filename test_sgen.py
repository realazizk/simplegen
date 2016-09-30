import sgen


def setup_content():
    import os
    import shutil

    if os.path.exists(os.path.join(os.getcwd(), 'content_test')):
        shutil.rmtree(os.path.join(os.getcwd(), 'content_test'))

    os.makedirs(os.path.join(os.getcwd(), 'content_test'))

    for blog in ['blog1.md', 'blog2.md']:
        with open(os.path.join(os.getcwd(), 'content_test', '%s.md' % blog), 'w') as test_file:
            test_file.write("""Title: Blog1
    Date: 12/12/2012 12:12

    # Article 1

    Stuff

    qsdsqdsqd

    [Link](https://google.com/)
    """)


def test_get_files():
    setup_content()
    assert sgen.find_content(
        'content_test'
    ) == ['blog1.md', 'blog2.md']