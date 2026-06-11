import subprocess

def scan_wifi():
    try:
        result = subprocess.run(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if not output:
            print("No networks detected. Make sure Wi-Fi is turned on.")
            return

        print("Available Wi-Fi Networks Detected:")
        print("=" * 70)

        lines = output.splitlines()

        # Usually the first line is the header
        header = lines[0]
        data_lines = lines[1:]

        for line in data_lines:
            if line.strip():
                # SSID can have spaces. Columns are usually aligned by at least 2 spaces.
                parts = [p.strip() for p in line.split("  ") if p.strip()]
                if len(parts) >= 5:
                    ssid = parts[0]
                    bssid = parts[1]
                    rssi = parts[2]
                    channel = parts[3]
                    security = parts[-1]

                    print(f"SSID: {ssid}")
                    print(f"  BSSID: {bssid}")
                    print(f"  RSSI: {rssi} dBm")
                    print(f"  Channel: {channel}")
                    print(f"  Security: {security}")
                    print("-" * 70)
                else:
                    print("Could not parse line:", line)

    except Exception as e:
        print(f"Error scanning Wi-Fi networks: {e}")

if __name__ == "__main__":
    scan_wifi()