import subprocess
import re

def get_wifi_password(ssid):
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-D", "AirPort network password", "-ga", ssid],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return "❌ No password found or permission denied."
        
        match = re.search(r'password: "(.*)"', result.stderr)
        if match:
            return match.group(1)
        else:
            return "❌ Password not available."
    except Exception as e:
        return f"Error: {e}"

# Example usage:
ssid_to_lookup = "MEO-4C26E0"
password = get_wifi_password(ssid_to_lookup)
print(f"🔑 Password for SSID '{ssid_to_lookup}': {password}")