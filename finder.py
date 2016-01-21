import os
import re
import sys
import tester           #Importing as Tester is in another file
def reg_matcher(folder,multi_check,level):
    if not multi_check:
        return True
    if multi_check[level]:
        for regex in multi_check[level]:
            if reger(regex,folder):
                return True
    return False

def reger(regex,tomatch):
    try:
        result=re.match(regex,tomatch)
        if result:
            return True
    except re.error:
        print ("Your regex %s didn't compile properly, i.e it's an invalid regex. :(" % regex)
        sys.exit(0)

def norm_matcher(folder,multi_check,level):
    if (not multi_check) or (not multi_check[level]) :
        return True
    if folder in multi_check[level]:
        return True
    return False

def file_reg(regex,file_list):
    if not file_list:
        return True
    for regex in file_list:
        if reger(regex,folder):
            return True
    return False

def file_norm(folder,file_list):
    if not file_list:
        return True
    if folder in file_list:
        return True
    return False

def evaluate(corr,inp,folder,fault,limit,time,is_file,file_check=None,all_regex=False):

    from os import path
    checker=all_regex and file_reg or file_norm
    files = [f for f in os.listdir(folder) if path.isfile(f) and checker(f,file_check)]
    corr=tester.check_compile(corr)
    if(is_file):
        inp = tester.check_compile(inp)
    else:
        try:
            re.compile(inp)
        except re.error:
            print ("Your input regex %s didn't compile properly, i.e it's an invalid regex. :(" % inp)
            sys.exit(0)

    for to_test in files:
        if is_file:
            how_ss=tester.from_file(corr=corr,inp=inp,folder=folder,file_check=os.path.join(folder, to_test),fault=fault,limit=limit,time=time)
        else:
            how_ss=tester.regex_test(corr=corr,inp=inp,folder=folder,file_check=os.path.join(folder, to_test),fault=fault,limit=limit,time=time)
        how=how_ss[0]
        if how==0:
            print ("All Tests passed for %s" % to_test)
        elif how==1:
            print ("Compiled and executed, but wrong answer.")
        elif how==2:
            print ("Some tests passed, some did not, for %s " % to_test)
        elif how==3:
            print ("Compliation error")
        elif how==4:
            print ("The correct version didn't compile properly. Please check it")
        elif how==5:
            print ("The input didn't compile properly")
        elif how==6:
            print("Uncheckable File")
        else:
            print("how ",how)

def crawlDir(corr,inp,folder,fault,limit,time,is_file,level,file_check=None,multi_check=[],all_regex=False):
    if level==0:
        evaluate(corr=corr,inp=inp,folder=folder,fault=fault,limit=limit,time=time,is_file=is_file,file_check=file_check,all_regex=all_regex)
        return
    checker=all_regex and reg_matcher or norm_matcher
    sub_dir_list=[sub_dir for sub_dir in os.listdir(folder) if os.path.isdir(os.path.join(folder, sub_dir)) and checker(folder,multi_check,level)]
    for sub_dir in sub_dir_list:
        crawlDir(corr=corr,inp=inp,folder=os.path.join(folder, sub_dir),fault=fault,limit=limit,time=time,is_file=is_file,level=level-1,file_check=file_check,multi_check=multi_check,all_regex=all_regex)
