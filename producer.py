import argparse
import sys
import os
import time
import threading
import subprocess as sp


def main():
    parse=argparse.ArgumentParser(usage='%(prog)s [options]')
    parse.add_argument('file_name',type=str,nargs='?',help="name of case")
    args=parse.parse_args()
    file_name = args.file_name
    if len(sys.argv)==1:
        print "Error : you must give a file name, such as camera_test or execute python xxx.py -h to read more info"	
        sys.exit(-1)
    file_location = os.path.join(os.getcwd(),'recording',file_name)
    print file_location
    archive_name = 'rec_'+file_name+'.ini'
    file_path = os.path.join(file_location,archive_name)     
    if not os.path.isdir(file_location):
        os.makedirs(file_location)  
    move_command = 'mv temp.ini ' + file_location
    old_name = os.path.join(file_location,'temp.ini')
    print "if you have completed recorded events, you can press Ctrl + C to stop..."
    #manuplater()
    record()
    sp.Popen(move_command.split(' ')).wait()
    os.rename(old_name,file_path)

def record():
    record_command = 'adb shell getevent -t -c 100000000 > temp.ini'
    os.system(record_command)
 	
# def make_movie():
#     make_movie_command = 'adb shell screenrecord /sdcard/temp.mp4'
#     sp.Popen(make_movie_command.split(' ')).wait()

# def manuplater():
#     threads=[]
#     t1 = threading.Thread(target=record)
#     threads.append(t1)
#     t2 = threading.Thread(target=make_movie)
#     threads.append(t2)
#     for thread in threads:
#         thread.setDaemon(True)
#         thread.start()
#     for thread in threads:
#         thread.join()    


if __name__ == "__main__":
    main()    
