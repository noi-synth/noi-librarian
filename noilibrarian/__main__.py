import noilibrarian.library

def main(args=None):
    libpath = 'library/'
    
    print('creating library...')
    library = noilibrarian.library.create(libpath, True)
    
    # print(library)
    
    print('maintaining library...')
    new_metadata = noilibrarian.library.maintain(library)
    # print(new_metadata)
    
    print('saving maintained library...')
    noilibrarian.library.update(libpath, new_metadata)
    
    print('done.')

if __name__ == '__main__':
    main()