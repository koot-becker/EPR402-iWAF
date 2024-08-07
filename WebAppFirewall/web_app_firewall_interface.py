import subprocess

def run_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")

if __name__ == "__main__":
    scripts = [
        "web_app_firewall_ctf.py",
        "web_app_firewall_dvwa.py",
        "web_app_firewall_tiredful.py"
    ]

    for script in scripts:
        run_script(script)