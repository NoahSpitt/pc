import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shell_sim import VirtualFileSystem


def test_ls_and_cd():
    fs = VirtualFileSystem()
    fs.mkdir('dir')
    fs.touch('dir/file.txt')
    assert 'dir/' in capture_ls(fs, '.')
    fs.cd('dir')
    assert 'file.txt' in capture_ls(fs, '.')

def capture_ls(fs, path):
    from io import StringIO
    import sys
    old = sys.stdout
    buf = StringIO()
    sys.stdout = buf
    fs.ls(path)
    sys.stdout = old
    return buf.getvalue()
