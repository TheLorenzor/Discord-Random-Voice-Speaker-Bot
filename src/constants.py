import configparser as parser
import  pathlib as path

DATA_PATH = path.Path(__file__).parent.parent / 'data'

config = parser.ConfigParser()

config.read(str(DATA_PATH / 'config.ini'))

DISCORD_TOKEN = config['Configuration']['token']

TIMEOUT_TIME = int(config['Configuration']['time_out'])

JOIN_MESSAGE = config['Configuration']['hello_message']

UPDATE_MESSAGE = str(config['Configuration']['update_message'])

IS_UPDATE = config['Configuration'].getboolean('is_update')