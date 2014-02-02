import configparser

def main():
    config = configparser.ConfigParser()
    config['Data'] = {"username" :'',
                      "password" :'',
                      "sync_dir" : '',
                      "prefix" : ''
                      }
    config['Server'] = {"url" : 'http://140.160.107.111:8080'}
    with open('wombat.ini', 'w') as configfile:
        config.write(configfile)


main()


