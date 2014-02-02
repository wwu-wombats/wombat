import configparser
import os

def main():
    config = configparser.ConfigParser()
    config['Data'] = {"username" :'',
                      "password" :'',
                      "sync_dir" : '',
                      "prefix" : ''
                      }
    config['Server'] = {"url" : 'http://localhost:8080'}
    with open(os.path.join(os.environ['HOME'], '.wombat.ini'), 'w') as configfile:
        config.write(configfile)


main()


