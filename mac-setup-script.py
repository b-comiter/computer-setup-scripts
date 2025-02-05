import os
import time
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import threading

apps = ["google-chrome", "visual-studio-code", "iterm2", "chatgpt", "spotify", "rectangle", "scroll-reverser", "docker"]
packages = ["git", "node", "python", "wget", "docker-compose"]

setup_thread = None
stop_event = threading.Event()

def run_command(command, output_box):
    if stop_event.is_set():
        return
    output_box.insert(tk.END, f"Running: {command}\n")
    output_box.see(tk.END)
    output_box.update_idletasks()
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output_box.insert(tk.END, result.stdout + "\n")
    else:
        output_box.insert(tk.END, f"Error: {result.stderr}\n")
    output_box.see(tk.END)
    output_box.update_idletasks()

def install_xcode(output_box):
    if stop_event.is_set():
        return
    def check_xcode_installed():
        result = subprocess.run(['xcode-select', '-p'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0

    if check_xcode_installed():
        output_box.insert(tk.END, "Xcode is already installed.\n")
        output_box.update_idletasks()
        return

    run_command("sudo xcode-select --install", output_box)
    while not check_xcode_installed():
        if stop_event.is_set():
            return
        output_box.insert(tk.END, "Waiting for Xcode installation...\n")
        output_box.update_idletasks()
        time.sleep(2)
    output_box.insert(tk.END, "Xcode installation complete.\n")
    output_box.update_idletasks()

def install_homebrew(output_box):
    if stop_event.is_set():
        return
    output_box.insert(tk.END, "Checking Homebrew installation...\n")
    output_box.update_idletasks()
    if subprocess.run("command -v brew", shell=True).returncode != 0:
        run_command("/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"", output_box)
        os.system('echo "eval \"$(/opt/homebrew/bin/brew shellenv)\"" >> ~/.zshrc')
        os.system('eval "$(/opt/homebrew/bin/brew shellenv)"')
    else:
        output_box.insert(tk.END, "Homebrew is already installed.\n")
        output_box.update_idletasks()

def install_packages(output_box):
    if stop_event.is_set():
        return
    output_box.insert(tk.END, "Installing Homebrew packages...\n")
    output_box.update_idletasks()
    for package in packages:
        if stop_event.is_set():
            return
        run_command(f"brew install {package}", output_box)
        time.sleep(1)

def install_apps(output_box):
    if stop_event.is_set():
        return
    output_box.insert(tk.END, "Installing applications...\n")
    output_box.update_idletasks()
    for app in apps:
        if stop_event.is_set():
            return
        run_command(f"brew install --cask {app}", output_box)
        time.sleep(1)

def setup_github(output_box):
    if stop_event.is_set():
        return
    user_input = messagebox.askyesno("GitHub Setup", "Do you want to setup GitHub RSA?")
    if user_input:
        run_command("ssh-keygen -t rsa", output_box)
        messagebox.showinfo("GitHub", "Copy RSA key and add it to GitHub")
        run_command("open -a \"Google Chrome\" https://github.com/settings/keys", output_box)

def set_macos_preferences(output_box):
    if stop_event.is_set():
        return
    output_box.insert(tk.END, "Configuring macOS preferences...\n")
    output_box.update_idletasks()
    run_command("defaults write NSGlobalDomain AppleShowAllFiles -bool true", output_box)
    run_command("defaults write com.apple.dock autohide -bool true && killall Dock", output_box)

def start_setup(output_box):
    global setup_thread, stop_event
    stop_event.clear()
    def run_setup():
        install_xcode(output_box)
        install_homebrew(output_box)
        install_packages(output_box)
        install_apps(output_box)
        setup_github(output_box)
        set_macos_preferences(output_box)
        output_box.insert(tk.END, "Setup complete! Restart your machine for changes to take effect.\n")
        output_box.update_idletasks()
        messagebox.showinfo("Setup Complete", "Restart your machine for all changes to take effect.")
    
    setup_thread = threading.Thread(target=run_setup, daemon=True)
    setup_thread.start()

def stop_setup():
    global stop_event
    confirm = messagebox.askyesno("Confirm Stop", "Are you sure you want to stop the setup process?")
    if confirm:
        stop_event.set()
        messagebox.showinfo("Setup Stopped", "The setup process has been stopped.")

def create_gui():
    root = tk.Tk()
    root.title("Mac Setup Tool")
    root.geometry("600x400")
    
    frame = tk.Frame(root)
    frame.pack(pady=10)
    
    output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
    output_box.pack(pady=10)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    
    start_button = tk.Button(button_frame, text="Start Setup", cursor="circle", command=lambda: start_setup(output_box))
    start_button.pack(side=tk.LEFT, padx=5)
    
    stop_button = tk.Button(button_frame, text="Stop Setup", cursor="circle", command=stop_setup)
    stop_button.pack(side=tk.LEFT, padx=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
