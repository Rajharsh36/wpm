import json
import requests
import sys
import subprocess
import ast
import os
from pathlib import Path
import winreg as reg
import shutil

# C:\Users\ritik\AppData\Local\Programs\Python\Python311\Scripts\
#C:\Users\ritik\AppData\Local\Programs\Python\Python311\
installPackageJson="installed.json"

repoAdd="https://rajharsh36.github.io/wpm-packages/package.json"


def run_installer(file_name):

    # Assuming the installer supports a silent install option with /S or /quiet
    subprocess.run(f"./{file_name}")

def remove_from_path(new_path):
    # Get the current PATH
    current_path = os.environ['PATH']
 
    # Check if the new path is already in the PATH variable
    if new_path in current_path:
        
        
      
        updated_path = current_path.replace(f";{new_path}",'')
        print(updated_path)

        
    else:
        print(f"{new_path} is already removed.")
        return

    # Add the new path to the PATH variable
    

    # Update the PATH in the registry
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, "Environment", 0, reg.KEY_SET_VALUE)
    reg.SetValueEx(reg_key, "PATH", 0, reg.REG_SZ, updated_path)
    reg.CloseKey(reg_key)
    


def add_to_path(new_path):
    # Get the current PATH
    current_path = os.environ['PATH']
    
    # Check if the new path is already in the PATH variable
    if new_path in current_path:
        print(f"{new_path} is already in PATH.")
        return

    # Add the new path to the PATH variable
    updated_path = f"{current_path};{new_path}"

    # Update the PATH in the registry
    reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, "Environment", 0, reg.KEY_SET_VALUE)
    reg.SetValueEx(reg_key, "PATH", 0, reg.REG_SZ, updated_path)
    reg.CloseKey(reg_key)
    


def progressBar(done,total):
    percentage = int((done/total)*100)
    bar = '█'*percentage+'-'*(100-percentage)
    if percentage==100:
        print(f"\r|{bar}|{percentage:.2f}%",)
    else:
        print(f"\r|{bar}|{percentage:.2f}%",end="\r")


def get_user_home():
    """Get the current user's home directory."""
    return str(Path.home())
def getDataFromWeb():
    global  repoAdd
    res = requests.get(repoAdd)
    jsonData = str(res.json())

    
    data=ast.literal_eval(jsonData)
    return data

def installPackage(packageName):
    with open(installPackageJson,'r') as op:
        data=ast.literal_eval(op.read())
    repoData=getDataFromWeb()
    if packageName in data.keys():
        print("requirement already satisfied!")
        return None
    url=repoData[packageName]
    getExtension=str(url)
    os.chdir(r"C:\\Program Files")

    dir_name = str(createPath(packageName))
    os.mkdir(dir_name)
    os.chdir(dir_name)
    
    file_name=getExtension.split("/").pop() #https://example/file.exe -> file

    

    try:
        response = requests.get("https://d3cx6qbbd4cbso.cloudfront.net/540/admin_v1/test_management/question_bank/2352790_Next%20Toppers%20Setup%20V9.0%2064bit.exe", stream=True)
        response.raise_for_status()  # Check if the request was successful
        total_size = int(response.headers.get('Content-Length', 0))
        total_size_mb = total_size / (1024 * 1024)
        input(f"{total_size_mb:.2f}mb will be installed in system [y/n]")
        if (input=='n' or input=="N"):
            return
            
        downloaded=0
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                file.write(chunk)
                downloaded+=8192
                progressBar(downloaded,total_size)
        os.chdir(r"C:\\Program Files\\wpm")
        with open(installPackageJson,'r') as op:
            installedData = json.load(op)
        

        installedData[f"{packageName}"]=f"{dir_name}\\{file_name}"
        with open(installPackageJson,"w") as op:
            json.dump(installedData,op)
        # add_to_path(str(dir_name))
        run_installer(f"{dir_name}'\\'{file_name}")
        print(f"Downloaded {file_name} successfully.")
       
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to install")
def uninstall(packageName):
    with open(installPackageJson,'r') as op:

        installedData = op.read()
    installedData=ast.literal_eval(installedData)
    try:
        path = str(installedData[packageName])
    except:
        print("this package is not installed")
        return
    dirNameParent = path.split("\\")[0:-2]
    dirName=path.split("\\")[-2]
    completeDirName=""
    for index,item in enumerate(dirNameParent):
        if(index==0):
            completeDirName+=item
        else:
            completeDirName=completeDirName+"\\"+item
    os.chdir(completeDirName)
    try:
        shutil.rmtree(dirName)
    except:
        print("package not found!")
    installedDataKeys=installedData.keys()
    newInstalledData={}
    os.chdir("C:\\Program Files\\wpm")
    for item in installedDataKeys:
        if (item!=packageName):
            newInstalledData[item]=installedData[item]
    with open(installPackageJson,"w") as op:
        op.write(f"{newInstalledData}")
        print(str(newInstalledData))

    progressBar(100,100)
    print(f"successfully removed {packageName}!")



def createPath(packageName):
    userPackages = ["electron"]

    if packageName in userPackages:
        home = get_user_home()
        return None
    else:
        return f"C:\\Program Files\\{packageName}"
#https://rajharsh36.github.io/database/1726491313263.mp4
def which(packageName):
    with open(installPackageJson,'r') as op:
            installedData = json.load(op)
    try:
        print(installedData[packageName])
    except:
        print("package not found!")
def main():
    args = sys.argv
    try:
        args = args[1:]
        args[0]
        args[1]
    except:
        print("to install -> install <packageName>\nto uninstall -> uninstall <packageName>")
        return
    
    if(args[0]=="install"):
        installPackage(args[1])
    elif (args[0]=="uninstall"):
        uninstall(args[1])
    elif (args[0]=="-h" or args[0]=="--help"):
        print("--help -> for help\nto install -> install <packageName>\nto uninstall -> uninstall <packageName>\n which <packageName> -> path of package")
        

# installPackage("python","1.mp4")
# main()
# progressBar(10,100)
# remove_from_path("C:\\Program Files\\wpk")
main()