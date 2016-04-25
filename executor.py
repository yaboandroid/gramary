#/usr/bin/python
import argparse
import sys
import re
import os
import time
import datetime
import subprocess as sp


def main():
    parse=argparse.ArgumentParser(usage='%(prog)s [options]')
    parse.add_argument('device_id',type=str,nargs='?',help="ID of your device")
    parse.add_argument('--path',dest='path',type=str,nargs='+',help="path of test cases")
    parse.add_argument('--loop_number',dest="run_times",type=int,nargs="+",help="run loop times")
    args=parse.parse_args()
    device_id = args.device_id
    case_path = args.path[0]
    run_times = args.run_times[0]
    origin_history = parse_history(device_id)
    opera_name = 'temp_event_'+device_id+'.ini'
    remove_command="rm " + opera_name + ' execute_testcase.py' 
    for loops in range(1,int(run_times)+1):
        print "[Info] Start to run loop %d"%loops
        opera = 'temp_event_'+device_id+'.ini'
        r2=r'rec_(\w+).ini'
        for case in os.listdir(case_path):
            file_path = os.path.join(case_path,case)
            key_words=re.findall(r2,file_path)[0]
            print "[info] Start to run testcase : %s"%key_words.upper()
            pic_save_teshu = os.path.join(os.getcwd(),'running',device_id)
            pic_save_te = os.path.join(pic_save_teshu,key_words)
            dt = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            pic_save_run = os.path.join(pic_save_te,('loop_'+str(loops)))
            if not os.path.isdir(pic_save_run):
                os.makedirs(pic_save_run)
            parse_event_file(file_path,device_id)
            take_pic_flag = False
            picture_number = 0
            op_handler = open(opera,'r')
            for cmd_prefix in op_handler:
                if filter_execute_command(cmd_prefix):	
                    cmd = 'adb -s ' + device_id + ' shell sendevent ' + cmd_prefix.strip('\n')
                    take_pic_flag = False
                elif filter_timer_command(cmd_prefix):
                    cmd = cmd_prefix.strip('\n')
                    take_pic_flag = False
                elif filter_takesnap_command(cmd_prefix):
                    time.sleep(1)
                    cmd = 'adb -s ' + device_id + ' shell ' + cmd_prefix.strip('\n')
                    take_pic_flag = True
                    picture_number += 1
                print cmd
                sp.Popen(cmd.split(' ')).wait()
                if take_pic_flag:
                    current_history = parse_history(device_id)
                    record_event_to_local(iter_event(get_different_list(origin_history,current_history)),pic_save_teshu,device_id)
                    new_file_path = pull_picture(device_id,pic_save_run)
                    rename_picure(picture_number,loops,new_file_path,key_words)
                    origin_history = current_history
            op_handler.close()        
            time.sleep(1)
            current_history = parse_history(device_id)
            record_event_to_local(iter_event(get_different_list(origin_history,current_history)),pic_save_teshu,device_id)  
            screenshot(device_id)        
            rename_picure('end',loops,pull_picture(device_id,pic_save_run),key_words)
            origin_history = current_history
    sp.Popen(remove_command.split(' ')).wait()            

def parse_event_file(file_path,device_id):
    temp_list=[]
    temp_list_1=[]
    file_dir = os.path.dirname(file_path)
    f_handler = open(file_path,'r')
    for line in f_handler:
        if my_filter(line):
            temp_list.append(line)
    f_handler.close()
    temp_value = 0.0
    for temp_line in temp_list:
        time_value,scanner,new_temp_line = get_timestamp(temp_line)
        if temp_value == 0.0:
            temp_value = time_value
            temp_list_1.append(new_temp_line)
        else:
            internal = round((time_value - temp_value),1)
            if internal > 0.7:
                sleep_time = internal - 2.0
                if sleep_time < 0.0:
                    sleep_time = 0      
                time_command_string = 'sleep {0}'.format(sleep_time)
                temp_list_1.append(time_command_string)
                takesnap_command_string = take_snapshot()
                temp_list_1.append(takesnap_command_string)
            temp_list_1.append(new_temp_line)    
            temp_value = time_value
    file_temp_name = 'temp_event_'+device_id+'.ini'        
    w_handler = open(file_temp_name,'w+')
    for new_line in temp_list_1:
        if filter_numbers_command(new_line):  
            new_line_1 = transfer(new_line)+'\n'
        else:
            new_line_1 = new_line + '\n'
        w_handler.write(new_line_1)    
    w_handler.close()            	


def get_timestamp(string):
    string = string.replace('[','').replace(']','').replace(':','').lstrip()
    return (float(string.split(' ')[0]),string.split(' ')[1],string)


def dec_to_hex(string):
    temp_a=int(string,16)
    return str(temp_a)	
 	
def my_filter(line):
    is_match_re=False
    r1=r'^\['
    if not re.findall(r1,line) == []:	
        is_match_re=True
    return is_match_re

def filter_execute_command(string):
    is_match_re=False
    r3=r'^/dev/input/event'
    if not re.findall(r3,string) == []:
        is_match_re=True
    return is_match_re    

def filter_numbers_command(string):
    is_match_re=False
    r6=r'^\d+.\d+'
    if not re.findall(r6,string) == []:
        is_match_re=True
    return is_match_re 


def filter_timer_command(string):
    is_match_re=False
    r4=r'^sleep'
    if not re.findall(r4,string) == []:
        is_match_re=True
    return is_match_re 

def filter_takesnap_command(string):
    is_match_re=False
    r5=r'^/system/bin/screencap'
    if not re.findall(r5,string) == []:
        is_match_re=True
    return is_match_re 

def take_snapshot():
    picture_name = 'run_temp.png'
    file_path_device = os.path.join('/sdcard/' + picture_name)
    take_snapshot_commad = '/system/bin/screencap -p ' + file_path_device
    return take_snapshot_commad

def screenshot(device_id):
    picture_name = 'run_temp.png'
    file_path_device = os.path.join('/sdcard/' + picture_name)
    take_snapshot_commad = 'adb -s ' + device_id + ' shell /system/bin/screencap -p ' + file_path_device
    print take_snapshot_commad
    sp.Popen(take_snapshot_commad.split(' ')).wait()

def pull_picture(device_id,location):
    pull_picture_command = "adb -s " + device_id + " pull /sdcard/run_temp.png " + location
    picture_ful_name = os.path.join(location,'run_temp.png')
    sp.Popen(pull_picture_command.split(' ')).wait()
    return picture_ful_name

def rename_picure(counter,loops,location,key_words):
    new_pic_name = 'screenshot'+'_'+str(key_words)+'_loop_'+str(loops)+'_000'+str(counter)+'.png'
    file_dirname = os.path.dirname(location)
    new_pic_full_name = os.path.join(file_dirname,new_pic_name)
    os.rename(location,new_pic_full_name)



def transfer(string):
    temp_le = []
    temp_le.append(string.split(' ')[1])
    temp_le.append(dec_to_hex(string.split(' ')[2]))
    temp_le.append(dec_to_hex(string.split(' ')[3]))
    temp_le.append(dec_to_hex(string.split(' ')[4]))
    return ' '.join(temp_le)


def parse_history(device_id):
    root_command = 'adb -s ' + device_id + ' root'
    cat_history_command = 'adb -s ' + device_id + ' shell cat /data/logs/history_event'
    sp.Popen(root_command.split(' '))
    return sp.Popen(cat_history_command.split(' '),stdout=sp.PIPE).stdout.read().strip('\n')


def get_different_list(string1,string2):
    l1 = string1.split('\n')
    l2 = string2.split('\n')
    return list(set(l2).difference(set(l1)))


def iter_event(diff_list):
    crash_list = []
    event = ['BOOT_LOGS','TOMBSTONE','JAVACRASH','ANR','SWWDT','UIWDT','IPANIC','MPANIC','MRESET','VMMTRAP']
    if diff_list == []:
        crash_list = []
    else:    
        for line in diff_list:
            for ev in event:
                if ev in line:
                    crash_list.append(line)
    return crash_list

def record_event_to_local(diff,log_path,device_id):
    server_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    print_event = "Server time : crash occurs at %s\ncrashfile content show as below :\n"%server_time
    print_crashfile = ''
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    log_file_name = 'log.txt'
    log_file = os.path.join(log_path,log_file_name)
    touch_command = 'touch ' + log_file
    if not os.path.isfile(log_file):
        sp.Popen(touch_command.split(' ')).wait()   
    f_handler1 = open(log_file,'a')
    for line_str in diff:
        crashlog_path = get_crash_path(line_str)
        if crashlog_path is not None:
            print_crashfile = get_crashfile_conetnt(device_id,crashlog_path)
        f_handler1.write((line_str+'\n'))
        f_handler1.write(print_event)
        f_handler1.write((print_crashfile+'\n'))
    f_handler1.close()          


def get_crash_path(string):
    path=None
    if '/data/logs/crashlog' in string:
        path = string.strip('\n').strip('\r').strip(' ').split(' ')[-1]
    return path

def get_crashfile_conetnt(device_id,string):
    crashfile_path = os.path.join(string,'crashfile')
    cat_crashfile_command = 'adb -s ' + device_id + ' shell cat ' + crashfile_path
    return sp.Popen(cat_crashfile_command.split(' '),stdout=sp.PIPE).stdout.read()


if __name__ == "__main__":	
    main()
