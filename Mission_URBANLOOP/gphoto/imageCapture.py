from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess
import sys

#Kill gphoto process when camera is connected

def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    #Search for the line that has the process
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            #kill the process
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)

shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#photos name
picID = "TEST"

clearCommand = ["--folder", "/store_00020001/DCIM/100EOS5D", "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + "_" +picID
save_location = "/home/luc/Documents/Mission_URBANLOOP/gphoto/images/" + folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create the new directory.")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    sleep(3)
    gp(downloadCommand)
    gp(clearCommand)

def renameFiles(ID):
    for filename in os.listdir("."):
        print(filename)
        if 10 < len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (ID + ".JPG"))
                print("Renamed the JPG")
            elif filename.endswith(".JPEG"):
                os.rename(filename, (ID + ".JPEG"))
                print("Renamed the JPEG")
            elif filename.endswith(".CR2"):
                os.rename(filename, (shot_time + ID + ".CR2"))
                print("Renamed the CR2")

if __name__ == "main":

    picID = sys.argv[1]

    #def shot(picID):
    killgphoto2Process()
    gp(clearCommand)
    createSaveFolder()
    captureImages()
    renameFiles(picID)
    #sleep(3)