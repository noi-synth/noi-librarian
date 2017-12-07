import sys
import noilibrarian.library
import noilibrarian.server

def main(args=sys.argv):
    command = 'maintain' if len(args) < 2 else args[1]
    
    if not command in ['maintain', 'server', 'refresh']:
        raise RuntimeError('Unknown command {}'.format(command))
    
    libpath = 'library/'
    port = 8000
    
    if command == 'maintain':
        print('creating library...')
        library = noilibrarian.library.create(libpath, True, r'.*\.wav')
        
        print('maintaining library...')
        new_metadata = noilibrarian.library.maintain(library)
        
        print('saving maintained library...')
        noilibrarian.library.update(libpath, new_metadata)
        
    elif command == 'server':
        print('starting server on port {}...'.format(port))
        noilibrarian.server.run(port, libpath)
        
    elif command == 'refresh':
        print('refershing server data')
        noilibrarian.server.refresh(libpath)
    
    print('done.')

if __name__ == '__main__':
    main()