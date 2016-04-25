import os
import subprocess as sp

def main():
    delete_flag = False
    print "[Warning] You try to return to initial status, and logs,pictures will be flushed."
    if not ask_if_continue():
        sys.exit(-1)
    if os.path.isdir('running'):
        os.system("rm -rf running")
    if os.path.isdir('temp_picture'):
        os.system("rm -rf temp_picture")
    if os.path.isdir('case_container'):
        case_container_path = os.path.join(os.getcwd(),'case_container')
        for item in os.listdir(case_container_path):
            delete_command="rm -rf "+os.path.join(case_container_path,item)       
            sp.Popen(delete_command.split(' ')).wait()
    print "[Info] clear caches done"


def ask_if_continue():
    answer = raw_input("Are you sure to continue? [yes/no] : ")
    if answer == "yes":
        print "[Info] Start to delete caches..."
        delete_flag = True
    elif answer == "no":
        print "[Info] Stop to delete caches"
        delete_flag = False
    else:
        print "[Debug] Invalid input. please input again."
        ask_if_continue()
    return delete_flag


if __name__ == "__main__":
    main()	