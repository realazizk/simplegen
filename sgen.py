
import glob


def find_content(**kwargs):
    content_dir = kwargs.get('content_dir', 'content/')
    return glob.glob(content_dir)

