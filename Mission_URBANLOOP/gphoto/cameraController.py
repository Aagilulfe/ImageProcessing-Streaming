import time
from sh import gphoto2 as gp2
import signal, os, subprocess, sys

#Get current path & set the path to captures folder
current_path = os.getcwd()
save_location = current_path + "/previews"
# os.chdir(save_location)

#Useful commands
clearCommand = ["--folder", "/store_00020001/DCIM/100EOS5D", "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
previewCommand = ["--capture-preview"]
downloadCommand = ["--get-all-files"]


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


#Create folder for captured photos
def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create the new directory.")
    os.chdir(save_location)


def getPreview():
    killgphoto2Process()
    gp2(triggerCommand)
    time.sleep(3)
    gp2(downloadCommand)
    gp2(clearCommand)

getPreview()