# gramary
instability issue checker for android
What it is
It is a small tool which written by python.
It includes a folder which you can put your test case together, it’s empty in initial status, besides, there are other five script files, and they are: producer.py executor.py restore.py show_picture.py and start.py in package.
This tool can help you record one event or more. So what’s the event? It should be a serial of actions which you try to execute some steps on android device for reproduce some issue. Or you can treat it as a test case which not written by words and sentences, but instead of concrete behavior. So the case is quite vivid.by the way, how can you stop to record, it’s simple, you only need to press ctrl + c to quit it.
After you have recorded an event or more, there should a new folder which named ‘recording’ exist in package, it created by programmer automatically when you start to record. Open it and there is a folder named xxx, ‘xxx’ means the content depends on your input which you try to give the event a name, such as test0 or camera_test, whatever, any name you want to specify, but, obviously, if you can make a meaningful name is the best. Note:  name of event must be a word, it means camera_test is acceptable, and camera test is not allowed. Because script can’t receive two parameters as a name of case. In the folder, there is a file with ‘ini’ as suffix, you have no necessary to read it or try to know it what’s meaning of it. Tool will parse it itself.
Event is ready, what’s the next? The tool can let you try to duplicate the event to device. What’s the mean? It means the android phone will be launched and executed event which you just recorded automatically. Amazing? Additionally, it provides a function which can let you specify how many times you want device to duplicate your event. It really useful if you want to reproduce an instability issue, which maybe need to duplicate event more than 100 times or more. So tool also can get crash log from device if crash generated. They will be recorded to a log.txt file which located in ‘running’ folder, the folder also is created by programmer, it contains a subfolder, its name is about your device id number, under this folder, log.txt is in here, except it, there is another folder which name is same as event folder in ‘recording’, it contains loop module, which is a place for put captured screenshot pictures together.
How this tool get useful data for catch logs if crash occurs? Mechanism is that before every step, program will read data from history event archive and check whether a new event recorded by system and if it is a crash event at the same time, if it is, programmer will get the event and write to log.txt. So if there is no crash occurs, the log.exe should be an empty file. Some critical event will be recorded, they are : 'BOOT_LOGS','TOMBSTONE','JAVACRASH','ANR','SWWDT','UIWDT','IPANIC','MPANIC','MRESET','VMMTRAP
The tool also can help you to take a screenshot of device during process of running events, when to start snapshotting depends on intervals of each step. So after executed there should be many pictures exist in ‘/running/device_id/case_name/loop_x’. from the address you can know that pictures will be stored according to different case and different loop, so it is quite complicated for check all pictures manually, for resolve it, there is another script named ‘show_picture.py’ written. When you execute it, it will automatically build a new folder ‘temp_picture’ and all the pictures from different case and loops will be put together.
After used this tool for a while, there will be many caches exist in package, so if you want to clear them, you can run another command: ‘python restore.py’, then the ‘running’ ‘temp_picture’ folder will be removed and items in case_container also will be cleared.
How to execute
producer
The method provides a way to record event. Before you execute it, you should make sure adb installed and works on your server. If the event which you want to record is quite completed, the duration should not be too long, and it’s best if you can split it to many pieces then named them as a serial cases. 
Command line: python producer.py
Options: case name
How to stop it? Press Control + C key meantime.
Example:
buildbot@shlabacsmn04:~/gramary$ python producer.py camera_test
start
The method provides a way to run all test cases which located in case_container folder, so before execute it , you have to manually copy event files which suffix is ‘ini’ in recording folder to case_container folder, or it will quit and pop up an error info. Its option is loop number, but programmer have provided a default value for it, so if no option given, it will run script 1 time, and if loop number given, it will run loop times.
Command line: python start.py
Options: loop number [default value is 1]
Example:
buildbot@shlabacsmn04:~/gramary$ python start.py 3
show_picture
The method provides a way to show all pictures which located in different case and loop folder in temp_picture folder. It is quite conveniently if you have so many cases and loops executed and generated too many pictures.
Command line: python show_picture.py
Options: none
Example:
buildbot@shlabacsmn04:~/gramary$ python show_picture.py
restore
The method provides a way to clear all caches which generated by programmer, please note that if you execute it, some important data located in running folder also will be removed, so program will pop up a message to let you confirm whether you need clear them seriously.
Command line: python restore.py
Options: none
Example:
buildbot@shlabacsmn04:~/gramary$ python restore.py
Limitation
This tool only can help you duplicate event on one device which also used for recording, it means that if you try to run event in different devices, that is not allowed.
It can’t judge error except crashes accurately, it means this tool can work with high efficiency for grasping crashes, but for functional issue, its efficiency is quite low, because it only can take screenshots for every steps to you.
Supported system: Linux. For windows not developed yet.

