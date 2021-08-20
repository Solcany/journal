import argparse

parser = argparse.ArgumentParser(
	usage= 'journalist.py [options] code',
	description='add journal entries')

# Add the arguments
parser.add_argument('entry_code',
                   	 metavar='CODE',
                     type=str,
                     help="the code for the project of the day")

parser.add_argument('-ht',
                       '--entry_host',
                       metavar='HOST',
                       type=str,
                       action='store',
                       help='the host of the project of the day')


args = parser.parse_args()

print(args)