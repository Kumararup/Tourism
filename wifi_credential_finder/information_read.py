import subprocess
import re
import socket

# --- Get system_profiler output ---
result = subprocess.run(
    ["system_profiler", "SPAirPortDataType"],
    capture_output=True,
    text=True
)

output = result.stdout

# --- Function to determine if security requires password ---
def is_password_protected(security_value):
    if security_value and "None" not in security_value:
        return "✅ Yes"
    return "❌ No"

# --- Get current Wi-Fi IP Address ---
def get_ip_address():
    try:
        ip_result = subprocess.run(
            ["ipconfig", "getifaddr", "en0"],
            capture_output=True,
            text=True
        )
        return ip_result.stdout.strip()
    except Exception:
        return "N/A"

# --- Show current IP ---
ip_address = get_ip_address()
print(f"🌐 Local Wi-Fi IP Address: {ip_address}")
print("-" * 60)

# --- Extract connected network ---
connected_match = re.search(
    r"Current Network Information:\s*\n\s*(\S+):\n((?:\s{14}.+\n)+)",
    output
)

if connected_match:
    ssid = connected_match.group(1)
    details = connected_match.group(2)

    phy_mode = re.search(r"PHY Mode:\s*(.+)", details)
    channel = re.search(r"Channel:\s*(.+)", details)
    security = re.search(r"Security:\s*(.+)", details)
    signal = re.search(r"Signal / Noise:\s*(.+)", details)

    print("✅ Connected Wi-Fi Network:")
    print(f"   SSID: {ssid}")
    print(f"   PHY Mode: {phy_mode.group(1) if phy_mode else 'N/A'}")
    print(f"   Channel: {channel.group(1) if channel else 'N/A'}")
    print(f"   Security: {security.group(1) if security else 'N/A'}")
    print(f"   Password Protected: {is_password_protected(security.group(1) if security else None)}")
    print(f"   Signal/Noise: {signal.group(1) if signal else 'N/A'}")
    print("-" * 60)
else:
    print("❌ No connected network detected.")
    print("-" * 60)

# --- Extract other networks ---
print("📡 Other Detected Wi-Fi Networks:")

network_blocks = re.finditer(
    r"Other Local Wi-Fi Networks:\n((?:\s{12}.+\n)+)",
    output
)

found_any = False
for block in network_blocks:
    networks_text = block.group(1)

    entries = re.finditer(
        r"\s{12}(\S+):\n((?:\s{14}.+\n)+)",
        networks_text
    )

    for entry in entries:
        found_any = True
        ssid = entry.group(1)
        details = entry.group(2)

        phy_mode = re.search(r"PHY Mode:\s*(.+)", details)
        channel = re.search(r"Channel:\s*(.+)", details)
        security = re.search(r"Security:\s*(.+)", details)
        signal = re.search(r"Signal / Noise:\s*(.+)", details)

        print(f"   SSID: {ssid}")
        print(f"     PHY Mode: {phy_mode.group(1) if phy_mode else 'N/A'}")
        print(f"     Channel: {channel.group(1) if channel else 'N/A'}")
        print(f"     Security: {security.group(1) if security else 'N/A'}")
        print(f"     Password Protected: {is_password_protected(security.group(1) if security else None)}")
        print(f"     Signal/Noise: {signal.group(1) if signal else 'N/A'}")
        print("-" * 60)

if not found_any:
    print("   No other networks detected.")