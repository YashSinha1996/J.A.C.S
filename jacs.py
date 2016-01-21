import finder
import argparse
import textwrap
parser = argparse.ArgumentParser(
	description=textwrap.dedent("""\
INSTANTLY CHECK ALL PROGRAMS AT YOUR LOCAL COMPETITION !!!!!
------------------------------------------------------------------------------------------------------------------
This is a CLI Program to check a lot programs in local competition. Works on Linux based OS only. Sorry Windows :)
Requires exrex, an external python module, for using regex.

To install do 'sudo pip install exrex'
	if pip is not present, do 'sudo apt-get install python-pip python-dev build-essential'
	then install using pip

For python 2.x, also requires subprocess32
Not required if using python 3.x

As of now, only .c , .o , .cpp , .class , .java and .py files are supported for correct version and input generator
Any other file extension will be treated as a text file. (For cases of constant input and output)

For infinte loops, timeout is 5 seconds
"""),
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog="Hope this works as it is supposed to :)"
)
parser.add_argument("correct", help="The source code/Compiled version (like .class or .out files) which gives the correct output for a given input")
parser.add_argument("check_dir", help="The directory/folder containing source files to be compiled and checked")
parser.add_argument("input_gen", help="The input generator. Can either be a Regular Expression or another source/compiled file to generate inputs")

parser.add_argument("-sf", "--store_faults", action="store_true",help="Will create a file to store which test cases went wrong")
parser.add_argument("-ir", "--is_regex", action="store_true",help="When input_gen is a regex. Please Specify this when it is a regex")
parser.add_argument("-tm","--timeout",type=int,help="Timeout limit in seconds, Integer. Use when speed matters. :)",default=5)
parser.add_argument("--version", action="version", version="%(prog)s alpha 0.1.0")

parser.add_argument("-ckf","--check_file", metavar="filename",nargs="+",help="Source file names (without extension) to check. Use for filtering in case of multiple files")

class dependent(argparse.Action):
    def __call__(self,parser,namespace,values,option_string=None):
        didfoo=getattr(namespace,'check_file',None)
        if(didfoo == None):
            parser.error( "File checking without check files")
        else:
            setattr(namespace,self.dest,values)
parser.add_argument("-mulm","--multi_check",metavar="N filename",nargs="+",action=dependent,help="Specify checking at each level. Example: '-mulm 1 check 2 check2' will check for foledrs with the name check at level 1 and check2 at level 2")

class dependent_true(argparse.Action):
    def __call__(self,parser,namespace,values,option_string=None):
        didfoo=getattr(namespace,'check_file',None)
        if(didfoo == None):
            parser.error( "File checking without check files")
        else:
            setattr(namespace,self.dest,True)
parser.add_argument("-alreg","--all_regex",action=dependent_true,help="All filters, in check_file or multi_check are regex expressions. Will make the program a lot slower.")

dir_sublevel = parser.add_mutually_exclusive_group()
dir_sublevel.add_argument("-d","--direct", action="store_true", help="Indicates not to look into subdirectories,files present directly inside specified folder.")
dir_sublevel.add_argument("-l","--levels", type=int,help="Number of level of Directory within Directory to look into. Default=1",default=1)

test_limit_group = parser.add_mutually_exclusive_group()
test_limit_group.add_argument("-ntl", "--no_test_limit", action="store_true",help="There is no test limit/Test limit will provided by input_gen file. Will check for ALL POSSIBLE IN CASE OF REGEX. USE CAREFULLY")
test_limit_group.add_argument("-tl", "--test_limit", type=int, default=100,help="Number of test cases to be generated. Defaults to 100. Useful only when inp_gen is a regex.")

args = parser.parse_args()

is_file=True          #Dillema, as putting it true means inp is a file if doesn't end expectently, and false impies regex

corr=args.correct	  #All these are 
folder=args.check_dir
inp=args.input_gen
limit=args.test_limit
dirlevel=args.levels

if inp.lower().endswith(('.c', '.cpp', '.o', '.class', '.java', '.py')):    #List of supported filenames
    is_file=True
if args.is_regex:														    #As this will work even when the while ends with above but is a regex
    is_file=False
if args.no_test_limit:                                                      #There is no test limit
    limit=-1
if args.direct:
    dirlevel=0
multi_file_check=[]
if args.multi_check:
    for i in range(dirlevel):
        x=[args.multi_check[index+1] for index,number in enumerate(args.multi_check) if number==str(i)]     #The next object if number mather
        multi_file_check.append(x)                                              #Yes, the append is delibrate

finder.crawlDir(corr=corr,inp=inp,folder=folder,fault=args.store_faults,limit=limit,time=args.timeout,is_file=is_file,level=dirlevel,file_check=args.check_file,multi_check=multi_file_check,all_regex=args.all_regex)
#





