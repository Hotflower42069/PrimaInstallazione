# Prima installazione
# @version 1.0.0
# @author matteo scarano
# @creation date 2023-06-05
# @last update date 2023-06-19


import subprocess, sys, os, ctypes, pyautogui, eel, pygetwindow as gw, win32clipboard, webbrowser
from tkinter import messagebox


# Determine whether the current script has admin privilege
def is_admin():
  try:
    return ctypes.windll.shell32.IsUserAnAdmin()
  except:
    return False


# Re-run the current python script as admin
def rerun_as_admin():
  ctypes.windll.shell32.ShellExecuteW(
    None,
    u"runas",
    str(sys.executable),
    str(__file__),
    None,
    1
  )


@eel.expose
def main(packages, uninstall_office_flag, install_windows_updates_flag, disable_windows_hello_autoprovisioning_flag):
  # Clear console
  os.system("cls")

  # Get current folder
  cwd=os.path.dirname(os.path.realpath(__file__))

  # Install selected apps
  if packages:
    install_apps(cwd, packages)

  # Uninstall office
  if uninstall_office_flag:
    uninstall_office(cwd)
  
  # Disable Windows Hello for Business autoprovisioning
  if disable_windows_hello_autoprovisioning_flag:
    disable_windows_hello_autoprovisioning()

  # Install windows updates
  if install_windows_updates_flag:
    install_windows_updates()    

  # Finished message
  print("\n\n> Esecuzione finita")

  eel.main_finished()


def install_apps(cwd, packages):
  # Install Chocolatey (Non-Administrative install)
  print("> Installazione Chocolatey...")
  p=subprocess.Popen(["powershell.exe", "Set-ExecutionPolicy Bypass -Scope Process -Force; $InstallDir='%s\chocolatey'; $env:ChocolateyInstall=\"$InstallDir\"; Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" % (cwd)], stdout=sys.stdout)
  p.communicate()

  # Install Packages
  for package in packages:
    print("\n\n> Installazione %s..." % (package["name"]))
    p=subprocess.Popen(["powershell.exe", "%s\chocolatey\choco install %s -y --exit-when-reboot-detected" % (cwd, package["value"])], stdout=sys.stdout)
    p.communicate()


def uninstall_office(cwd):
  print("\n\n> Disinstallazione dei prodotti Microsoft Office...")

  # Uninstall Office with 'Office Deployment Tool'
  p=subprocess.Popen(["powershell.exe", r"%s\data\setup.exe /configure %s\data\uninstall-configuration.xml" % (cwd, cwd)], stdout=sys.stdout)
  p.communicate()


def disable_windows_hello_autoprovisioning():
  # Disable Windows Hello for Business autoprovisioning
  print("\n\n> Disabilitazione del provisioning automatico di Windows Hello for Business...")
  p=subprocess.Popen(["powershell.exe", '$Helloforbusinesspath="HKLM:\SOFTWARE\Policies\Microsoft\PassportForWork"; if(-not (Test-Path $Helloforbusinesspath)){New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\" -Name "PassportForWork" -Force}; New-ItemProperty -Path $Helloforbusinesspath -Name "Enabled" -Value 1 -Force; New-ItemProperty -Path $Helloforbusinesspath -Name "DisablePostLogonProvisioning" -Value 1 -Force'], stdout=sys.stdout)
  p.communicate()


def install_windows_updates():
  # Install package provider NuGet
  print("\n\n> Installazione Pacchetto NuGet...")
  p=subprocess.Popen(["powershell.exe", "Install-PackageProvider -Name NuGet -Confirm:$false -Force"], stdout=sys.stdout)
  p.communicate()

  # Install and import module PSWindowsUpdate
  print("\n\n> Installazione Modulo PSWindowsUpdate...")
  p=subprocess.Popen(["powershell.exe", "Install-Module PSWindowsUpdate -Confirm:$False -Force; Set-ExecutionPolicy RemoteSigned; Import-Module PSWindowsUpdate"], stdout=sys.stdout)
  p.communicate()

  # Download and install Windows Updates
  print("\n\n> Installazione aggiornamenti di Windows...")
  p=subprocess.Popen(["powershell.exe", "Install-WindowsUpdate -AcceptAll"], stdout=sys.stdout)
  p.communicate()


@eel.expose
def create_log_file():
  # Get window
  console_window=gw.getWindowsWithTitle("Amministratore:  Prima installazione - Console")[0]

  # Change active window to console
  console_window.minimize()
  console_window.restore()

  # Copy console text
  pyautogui.keyDown("ctrl")
  pyautogui.press("a")
  pyautogui.keyUp("ctrl")

  pyautogui.keyDown("ctrl")
  pyautogui.press("c")
  pyautogui.keyUp("ctrl")

  # Get copied text
  win32clipboard.OpenClipboard()
  data=win32clipboard.GetClipboardData()
  win32clipboard.CloseClipboard()

  # Create log file and write text
  with open("log.txt", "w") as f:
    f.write(data)
  
  # Open log file
  webbrowser.open("log.txt")


if  __name__ == "__main__":
  # Change window title
  os.system("title Prima installazione - Console")

  # 'Administrative privileges and Internet connection required' message
  if not is_admin():
    messagebox.showinfo("Prima installazione", "Questa applicazione richiede 🛡️Privilegi amministrativi ed una 🌐Connesione ad Internet per essere eseguita e funzionare correttamente.")

  if is_admin():
    # Start GUI
    eel.init("web")
    eel.start("main.html", size=(650, 700), mode="edge")
  else:
    rerun_as_admin()