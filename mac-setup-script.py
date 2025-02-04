import os
import time
import subprocess

# Edit the apps and packages below for setup
apps = ["google-chrome", "visual-studio-code", "iterm2", "chatgpt", "spotify", "rectangle"]
packages = ["git", "node", "python", "wget", "docker", "docker-compose"]

def run_command(command):
    """Runs a shell command and prints output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Error: {result.stderr}")

def install_xcode():
    def check_xcode_installed():
        result = subprocess.run(['xcode-select', '-p'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0

    def wait_for_xcode_installation():
        while not check_xcode_installed():
            print("Waiting for Xcode to be installed...")
            time.sleep(10)  # Check every 10 seconds

    if (check_xcode_installed()):
        return
    # You can prompt the user to install Xcode here, or automatically invoke a command to start the installation
    subprocess.run(['sudo', 'xcode-select', '--install'])
    wait_for_xcode_installation()
    print("Xcode is now installed.")

def install_homebrew():
    print("Checking Homebrew installation...")
    if subprocess.run("command -v brew", shell=True).returncode != 0:
        print("Installing Homebrew...")
        run_command("/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        os.system('echo "eval \"$(/opt/homebrew/bin/brew shellenv)\"" >> ~/.zshrc')
        os.system('eval "$(/opt/homebrew/bin/brew shellenv)"')
    else:
        print("Homebrew is already installed.")

def install_packages():
    print("Installing Homebrew packages... ")
    for package in packages: 
        command = f"brew install {package}"
        print(f"\n {command}")
        run_command(command)

def install_apps():
    print("Installing applications...")
    for app in apps: 
        command = f"brew install --cask {app}"
        print(f"\n {command}")
        run_command(command)

def setup_github():

    user_input = input("Do you want to setup Github RSA? [Type YES or NO]").strip().lower()

    if user_input in ("yes", "y"):
        run_command("ssh-keygen -t rsa")
        output = input("Copy RSA key and enter it into github [Press Enter and continue to github]")

        run_command("open -a \"Google Chrome\" https://github.com/settings/keys")
        output = input("Press Enter to Continue.")
    elif user_input in ("no", "n"):
        print("You have indicated no.")

def set_macos_preferences():
    print("Configuring macOS preferences...")
    run_command("defaults write NSGlobalDomain AppleShowAllFiles -bool true")
    run_command("defaults write com.apple.dock autohide -bool true && killall Dock")

def main():
    install_xcode()
    install_homebrew()
    install_packages()
    install_apps()
    setup_github()
    set_macos_preferences()
    print("Setup complete! Restart your machine for all changes to take effect.")

if __name__ == "__main__":
    main()
