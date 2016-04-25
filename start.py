#/usr/bin/python
import os
import sys
import subprocess as sp

def main():
    try:
        loop_number = int(sys.argv[1])    
    except IndexError:
        loop_number = 1
    except ValueError as e:
        print "[Debug] you must give a number for sepcify loop times. Got Exception {0}".format(e)
        sys.exit(-1)
    scripts_location = os.path.join(os.getcwd(),'case_container')
    if not os.path.isdir(scripts_location):
        os.makedirs(scripts_location)
    cases_list = os.listdir(scripts_location)   
    if cases_list == []:
        print "There is no case exist in container, please copy cases to here : %s"%scripts_location
        sys.exit(-1)
    command_list = []
    print "[Info] Total run cases loop %d times"%loop_number
    for dev in get_devices():
        run_cmd = 'python executor.py ' + dev + ' --path ' + scripts_location + ' --loop_number ' + str(loop_number)
        command_list.append(run_cmd)
    generate_task(command_list)
    if not os.path.isfile(os.path.join(os.getcwd(),'execute_testcase.py')):
        print "Unknow error, generate execute_testcase script fail."	
        sys.exit(-1)
    execute_testcase_command = 'python execute_testcase.py'    
    sp.Popen(execute_testcase_command.split(' '))


def generate_task(command_list):
    str1='#!/usr/bin/python\n'
    str2='import os\n'
    str3='os.system("gnome-terminal'
    str4=" --tab -e 'bash -c \\\"keysentence ; exec bash\\\"\'"
    str5='")\n'
    str4_mod=''
    for full_cmd in command_list:
        str4_mod += str4.replace('keysentence',full_cmd)
    command_string = str1+str2+str3+str4_mod+str5
    script_file_name = 'execute_testcase.py'
    f1 = open(script_file_name,'w')
    f1.write(command_string)
    f1.close()    

def get_devices():
    cmd1 = ['adb','devices']
    cmd2 = ['grep' , '-w' , 'device']
    cmd3 = ['awk' , '{print $1}']
    p1=sp.Popen(cmd1,stdout=sp.PIPE)
    p2=sp.Popen(cmd2,stdin=p1.stdout,stdout=sp.PIPE)
    p3=sp.Popen(cmd3,stdin=p2.stdout,stdout=sp.PIPE)
    c1=p3.communicate()
    t1=c1[0]
    spl=t1.split('\n')
    del spl[len(spl)-1]
    device_list = spl
    return device_list

if __name__=="__main__":
    main()	