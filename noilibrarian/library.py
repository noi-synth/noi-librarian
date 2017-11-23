from os import listdir
from os.path import isfile, join, exists
from functools import reduce
from noilibrarian.audio import loadaudio
from noilibrarian.classifier import classify
from re import match

def readlibfile(libfile):
    f = open(libfile, 'r') 
    
    def separate(item):
        filename, category, offset = item.split(',')
        return {
            'filename': filename, 'category': category, 'offset': int(offset)
        }
        
    read = map(separate, f.read().splitlines())
    f.close()
    return list(read)

def savelibfile(libfile, library):
    f = open(libfile, 'w')
    
    def glue(acc, item):
        fields = map(lambda x: str(x), item.values())
        return acc + ('\n' if acc != '' else '') + ','.join(fields)
    
    contents = reduce(glue, library['metadata'], '')
        
    f.write(contents)
    f.close()

def create(folder, rewrite = False, pattern = r'.*\.wav'):
    files = [f for f in listdir(folder) 
                if isfile(join(folder, f)) and match(pattern, f)]
    print('found {} supported files'.format(len(files)))
    
    libfile = join(folder, 'library.noi')
    
    if exists(libfile):
        print('found existing NOI Library')
        metadata = readlibfile(libfile)
    else:
        print('folder is not NOI Library')
        metadata = []
        
    # Force rewriting library metadata
    if rewrite:
        metadata = []
        
    return { 'path': folder, 'files': files, 'metadata': metadata }
    
def maintain(library):
    storedfiles = list(map(lambda x: x['filename'], library['metadata']))
    metadata = library['metadata']
    
    # Get files needs to be maintained
    for f in filter(lambda x: x not in storedfiles, library['files']):
        print('maintaining file {}...'.format(f))
        # Load audio file
        audio = loadaudio(join(library['path'], f))
        
        # Classify each file
        category, offset = classify(audio)
        
        # Append result to metadata collection
        metadata.append({
            'filename': f,
            'category': category,
            'offset': offset,
        })
        
    return { 'path': library['path'], 'files': library['files'], 'metadata': metadata }

def update(folder, library):
    savelibfile(join(folder, 'library.noi'), library)
        