import subprocess
import re

def list_known_ssids():
    # Run the command to list preferred networks
    result = subprocess.run(
        ["networksetup", "-listpreferredwirelessnetworks", "en0"],
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().split("\n")
    # Skip header line
    ssids = [line.strip() for line in lines[1:] if line.strip()]
    return ssids

def get_wifi_password(ssid):
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-D", "AirPort network password", "-ga", ssid],
            capture_output=True,
            text=True
        )
        # Password is usually in stderr
        match = re.search(r'password: "(.*)"', result.stderr)
        if match:
            return match.group(1)
        else:
            return "❌ Password not available or permission denied."
    except Exception as e:
        return f"Error: {e}"

# Get list of SSIDs
ssids = list_known_ssids()

print("📡 Known Wi-Fi Networks and Passwords:")
print("-" * 60)

for ssid in ssids:
    password = get_wifi_password(ssid)
    print(f"SSID: {ssid}")
    print(f"Password: {password}")
    print("-" * 60)