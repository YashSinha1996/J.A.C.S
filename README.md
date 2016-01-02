### J.A.C.S
Sorry for the wierdness. This entire thing is literaly twodays of work

Just Another Competitive Scorer. It takes input, filters the files to be checked, and Scores them on Ten
This is Command Line Program based, built bu using python 3.4
For best usage, run with python3
TODO: 

1.  TESTING

2.  MAKE AN EXECUTABLE AFTER CHECKING PROs AND CONs

3.  ADD SUPPORT FOR MORE LANGUAGES (MAYBE)

4.  MAKE A BETTER DIFF FUNCTION (IT SUCKS AF)

5.  SUGGESTIONS

It is not an executable yet. (See todo)

Dependencies:

[*exrex:*](https://github.com/asciimoo/exrex) A module to give random strings, given a regex. Required if input is going to be regex

  
*subprocess32:* A module to port python3's builtin subprocess to python2.x. Required for ONLY for python2.x

*Supports:* C,C++,Java,Python 2.x

*Notes:*
- The input generator and correct answer can be in any of the supported lnguages
- For regex input exrex is a must
- Default timeout incase of infinite loops is 5 sec (Can be changed. See optional argument -tm)
- In case of regex input, number of test cases defaults to 100. (changable. See -ntl,-tl)
- WARNING Will check all ALL FILES if -ckf is not given (See optional argument -ckf)

##Documentation:

###Required arguments:
To be given in this order:
- *python jacs.py*
  - Obviously 

- *correct_answer*
  - The correct answer file, with full path. 
  - If just the filename is given, it is assumed to be on the current working directory
  - Can be txt file

- *starting_directory* 
  - The directory path where the program will start to look for the answers. It may or may not look into subdirectories. (You can specify)
- *input_file_orregex* 
  - The input generator script. Same conditions of path as correct_answer. Can be txt file.
  - However, the input can be regex. Strings satisfying the regex will be generated and fed as input.

###Optional Arguments: The fun and useful part  :)

- *-sf* or *--store_faults* 
  - Flag to declare that any mistakes found in the checked file
  - (SHITTY AS AF, SEE TODO)
- *-ir* or *--is_regex*
  - Declares that the input string given is a regex
- *-tm TIME* or  *--timeout TIME*
  - TIME in seconds after which to stop program execution
- *-ckf N filenames* or *--check_file N filenames*
  - Will only check files having a filename as one of these, OR staisfying one of these regex (See -alreg)
- *-mulm N checkN N+m checkn+m* or *--multi_check N checkN N+m checkn+m*
  - Requires -ckf to declared first. Else, will fail.
  - Filter at multiple directory levels. Ex:
  - `-mulm 1 Q1 1 Q2 2 Q2.1` 
  - impilies: check files having name as Q2.5 and directory level 2,and as Q1 or Q2 at directory level 1
  - DIR_LEVEL FILTER  (See -l for info on directory levels)
- *-alreg* or *--all_regex*
  - Requires -ckf to declared first. Else, will fail.
  - Implies ALL FILTERS IN -ckf and -mulm ARE REGULAR EXPRESSIONS
- *-d* or *--direct*
  - Flag declaring that files to be checked are all within the starting_directory itself. No need to check for directory within directory
  - (Equivalent to -l 0) 
  - MUTUALLY EXCLUSIVE WITH -l (i.e, using -d and -l together is not allowed)
- *-l LEVEL* or *--level LEVEL*
  - To look till LEVEL directory within directories.(Starting from 0)
  - i.e, 
    - -l 2 means to look in directory within directory within directory 
    - -l 1 means to look directory within directory 
  - MUTUALLY EXCLUSIVE WITH -d (i.e, using -d and -l together is not allowed)
- *-ntl* or *--no_test_limit*
  - Use with input scripts. Will check for ALL POSSIBLE IN CASE OF REGEX. USE CAREFULLY
  - Equivalent to -tl 0
  - MUTUALLY EXCLUSIVE WITH -tl (i.e, using -ntl and -tl together is not allowed)
- *-tl LIMIT* or *--test_limit LIMIT*
  - Test for LIMIT cases. First enters LIMIT in code to checked. Preferable use only with regex input.
  - Defaults to 100
  - MUTUALLY EXCLUSIVE WITH -tl (i.e, using -ntl and -tl together is not allowed)


#DEBUGGING AND TESTING IS LEFT !!!
