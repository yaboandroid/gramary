import os
import sys
import subprocess as sp

def main():
    temp_picture_dir = os.path.join(os.getcwd(),'temp_picture')
    if not os.path.isdir(temp_picture_dir):
        os.makedirs(temp_picture_dir)
    from_dir = os.path.join(os.getcwd(),'running')
    if not os.path.isdir(from_dir):
        print "[Debug] you have not ran testcase, so no pictures can be pulled."
        sys.exit(-1)
    search_command = 'find ' + from_dir + ' -name *.png'
    out = sp.Popen(search_command.split(' '),stdout=sp.PIPE).stdout.read().strip('\n')
    if out == '':
        print "[Info] there is no picture exist"
        sys.exit(-1)
    for cmd in out.split('\n'):
        pull_cmd = 'cp ' + cmd.strip(' ').strip('\r') + ' ' + temp_picture_dir
        sp.Popen(pull_cmd.split(' ')).wait()
    print "[Info] copy done!"    	

if __name__=="__main__":
    main()	