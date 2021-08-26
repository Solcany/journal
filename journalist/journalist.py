import argparse
from datetime import date

# https://github.com/XXIIVV/oscean/blob/master/src/database/journal0005.tbtl

OUTJOURNAL_FILE_PATH = "journal_out.txt"
INJOURNAL_FILE_PATH = "journal_in.txt"

POMODORO_SESSION = 0.416 # as a fraction of hour, 0.416 == 25 minutes

CODE_ENTRY_MAX_CHARS = 2
DATE_ENTRY_MAX_CHARS = 6
HOST_ENTRY_MAX_CHARS = 20
NAME_ENTRY_MAX_CHARS = 20

parser = argparse.ArgumentParser(
	usage= 'journalist.py code host pomodoros total [options]',
	description='add journal entries')

# set Custom argument types
def activity_type(s):
    if isinstance(s, str) and len(s) == CODE_ENTRY_MAX_CHARS:
    	return s
    else:
        raise argparse.ArgumentTypeError("activity code must have 2 characters")

def host_type(s):
    if isinstance(s, str) and len(s) <= HOST_ENTRY_MAX_CHARS:
    	return s
    else:
        raise argparse.ArgumentTypeError("host must have 20 chars max")

def name_type(s):
    if isinstance(s, str) and len(s) <= NAME_ENTRY_MAX_CHARS:
    	return s
    else:
        raise argparse.ArgumentTypeError("name must have 20 chars max")        

def date_type(s):
    if isinstance(s, str) and len(s) == DATE_ENTRY_MAX_CHARS:
    	return s
    else:
        raise argparse.ArgumentTypeError("date must have 6 characters[DDMOYR]")

# Add the arguments
parser.add_argument('activity_code',
                   	 metavar='activity',
                   	 type=activity_type,
                     help="the code for the activity")

parser.add_argument('host',
                      metavar='host',
                      type=host_type,
                      action='store',
                      help='the host of the project')

parser.add_argument('pomodoros',
                   	 metavar='sessions',
                     type=float,
                     help="amount of pomodoros spent on the activity")

parser.add_argument('total',
                      metavar='time assigned',
                      type=float,
                      action='store',
                      help='total time spent working on the project in hours')

parser.add_argument('-nm',
                     '--name',
                      metavar='entry name',
                      type=name_type,
                      action='store',
                      help='the name of the project of the day')

parser.add_argument('-im',
                     '--image',
                      metavar='image name',
                      type=str,
                      action='store',
                      help='the name of associated project image')

parser.add_argument('-in',
                     '--is_input',
                     default=False,
                     action='store_true',
                     help='is this input entry?')

parser.add_argument('-dt',
                     '--date',
                     metavar='project date',
                     type=date_type,
                     action='store',
                     help='force custom date')

parser.add_argument('-pi',
                     '--prod_index',
                     metavar='productivity index',
                     type=float,
                     action='store',
                     help='force productivity index')

args = parser.parse_args()

if(args.prod_index):
	productivity_index = args.prod_index
else:
	if(args.total != 0):
		productive_time = POMODORO_SESSION * args.pomodoros
		productivity_index = productive_time / args.total
		productivity_index = round(productivity_index, 1)
	else:
		productivity_index = 0.0



if(args.date):
	date_entry = args.date
else:
	date_entry = date.today().strftime("%d%m%y")


activity_entry = args.activity_code

if(activity_entry == "00"):
	host_entry = ""
else:
	host_entry = args.host

productivity_entry = productivity_index
total_entry = args.total 
name_entry = args.name
image_entry = args.image

entry = "{0} {1}       {2}   {3}   {4}".format(date_entry, activity_entry, productivity_entry, total_entry, host_entry)

if(args.name):
	padding = ' ' * (HOST_ENTRY_MAX_CHARS - len(args.host) + 1)
	entry += padding + args.name

if(args.image):
	if(args.name):
		padding = ' ' * (HOST_ENTRY_MAX_CHARS - len(args.name) + 1)	
	else:
		padding = ' ' * (HOST_ENTRY_MAX_CHARS + NAME_ENTRY_MAX_CHARS - len(args.host) + 2)

	entry += padding + args.image

if(args.is_input):
	with open(INJOURNAL_FILE_PATH, "a") as output:
		output.write('\n')
		output.write(entry)
else:
	with open(OUTJOURNAL_FILE_PATH, "a") as output:
		output.write('\n')
		output.write(entry)
