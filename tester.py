import os
from os import path
import sys
import tempfile
import difflib
import signal
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess
def from_file(corr,inp,folder,file_check,fault,limit,time):
	inp_temp=tempfile.TemporaryFile(dir=folder)
	(head,tail)=path.split(inp)
	(root,ext)=path.splitext(tail)
	executable=True
	if not head:
		head=os.getcwd()
	if ext==".o":
		args="./"+tail
	elif ext==".class":
		args=["java",root]
	elif ext==".py":
		args=["python",tail]
	else:
		executable=False
	if executable:
		p=subprocess.call(args,stdout=inp_temp,cwd=head,timeout=5)
		#pass inp_temp
		how=check(corr=corr,inp=inp_temp,folder=folder,file_check=file_check,fault=fault,time=time)
	else:
		#pass inp
		how=check(corr=corr,inp=inp,folder=folder,file_check=file_check,fault=fault,time=time)
	inp_temp.close()
	return how


def regex_test(corr,inp,folder,file_check,fault,limit,time):
	import exrex
	inp_temp=tempfile.TemporaryFile(dir=folder)
	if limit==0:
		inp_gen=exrex.generate(inp,limit=sys.maxint)
		for inp_n in inp_gen:
			inp_temp.write(inp_n+"\n")
	else:
		inp_gen=exrex.generate(inp,limit=limit)
		n=0
		inp_temp.write(str(limit)+"\n")
		for inp_n in inp_gen:
			n+=1
			if(n>limit):
				break
			inp_temp.write(inp_n+"\n")
		if(n<limit):
			for x in range(n,limit):
				inp_one=exrex.getone(inp,limit=limit)
				inp_temp.write(inp_one+"\n")
		#pass inp_temp
		how=check(corr=corr,inp=inp_temp,folder=folder,file_check=file_check,fault=fault,time=time)
		inp_temp.close()
		return how

def check_compile(inp):
	(head,tail)=path.split(inp)
	(root,ext)=path.splitext(tail)
	time=5
	if not head:
		head=os.getcwd()
	if ext==".c":
		args=["gcc",tail,"-o",root+".o"]
		final= path.join(head,root+".o")
	elif ext==".cpp":
		args=["g++",tail,"-o",root+".o"]
		final= path.join(head,root+".o")
	elif ext==".java":
		args=["javac",tail]
		final= path.join(head,root+".class")
	elif ext==".py":
		args=["python",tail]
		return inp
	else:
		return inp
	subprocess.check_call(args,cwd=head,timeout=5)
	return final
	
def check(corr,inp,folder,file_check,fault,time):
	(root,ext)=path.splitext(file_check)
	(head,tail)=path.split(corr)
	(corr_root,corr_ext)=path.splitext(tail)
	correct=tempfile.TemporaryFile(dir=folder)
	to_check=tempfile.TemporaryFile(dir=folder)
	#---------------------------------------------------
	#Code Block to find output of file_check
	is_python=False
	if ext==".c":
		args=["gcc",tail,"-o",root+".o"]
		final_args="./"+tail
	elif ext==".cpp":
		args=["g++",tail,"-o",root+".o"]
		final_args="./"+tail
	elif ext==".java":
		args=["javac",tail]
		final_args=["java",root]
	elif ext==".py":
		args=["python",tail]
		final=args
		is_python=True
	try:
		if not is_python:
			subprocess.call(args,cwd=folder,timeout=5)
	except Exception(e):
		if fault:
			f=open(path.join(folder,root)+".fault.txt","w")
			subprocess.check_call(args,stdin=inp,stdout=to_check,stderr=f,cwd=folder)
			return 3
	f=None
	if fault:
		f=open(path.join(folder,root)+".fault.txt","w")
	try:
		p=subprocess.call(final_args,stdin=inp,stdout=to_check,stderr=f,cwd=folder,timeout=time)		
	except Exception(e):
		if not is_python:
			return 2
		return 3
	#----------------------------------------------------------------
	#Code Block to execute the "correct" version. All exceptions in it are to be thrown out
	executable=True
	if not head:
		head=os.getcwd()
	if ext==".o":
		corr_args="./"+tail
	elif ext==".class":
		corr_args=["java",root]
	elif ext==".py":
		corr_args=["python",tail]
	else:
		executable=False
		how=diff(corr,to_check,f)
	if executable:
		p=subprocess.call(corr_args,stdin=inp,stdout=correct,cwd=head,timeout=time)
		how=diff(correct,to_check,f)
	correct.close()
	to_check.close()
	return how

def diff(corr,to_check):
	d=difflib.Differ()
	result = list(d.compare(corr.readlines(), to_check.readlines()))
	num_match=0
	num_unmatched=0
	no_lines=len(result)
	for line in result:
		if line[0]=='-':
			num_unmatched+=1
			if f:
				f.write(line+"\n")
		elif line[0]=='?' or line[0]=='+':
			pass
		else:
			num_match+=1
	if num_match==no_lines:
		status=0
		score=10
	else:
		status=1
		score=10*(num_match//result)
	how=(status,score)
	return how










