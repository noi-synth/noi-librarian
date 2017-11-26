import http.server
import socketserver
import fileinput
from os.path import join, exists
from distutils.dir_util import copy_tree
from noilibrarian.library import readlibfile


def copyfiles():
    copy_tree('noilibrarian/server/', 'dist/')
    
def replaceplaceholders(libpath):
    libfile = join(libpath, 'library.noi')
    
    if exists(libfile):
        library = readlibfile(libfile)
        
        with fileinput.FileInput(join('dist', 'index.html'), inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace('[[LIBRARY]]', str(library)), end='')
    else:
        print('library file {} does not exists. data missing.'.format(libfile))

def run(port, libpath):
    copyfiles()
    replaceplaceholders(libpath)
    
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        print('open http://localhost:{}/dist'.format(port))
        httpd.serve_forever()