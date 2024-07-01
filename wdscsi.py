import subprocess
import sys
import re

def get_drive_details(device_path):
    try:
        # Get SCSI inquiry data
        inquiry_cmd = ["sg_inq", device_path]
        inquiry_result = subprocess.run(inquiry_cmd, capture_output=True, text=True)
        inquiry_data = inquiry_result.stdout

        # Get SCSI read capacity data
        capacity_cmd = ["sg_readcap", "-b", device_path]
        capacity_result = subprocess.run(capacity_cmd, capture_output=True, text=True)
        capacity_data = capacity_result.stdout

        return inquiry_data, capacity_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def parse_inquiry_data(inquiry_data):
    details = {}
    lines = inquiry_data.split('\n')
    for line in lines:
        if 'Vendor identification' in line:
            details['Vendor'] = line.split(':')[-1].strip()
        if 'Product identification' in line:
            details['Product'] = line.split(':')[-1].strip()
        if 'Product revision level' in line:
            details['Revision'] = line.split(':')[-1].strip()
        if 'Unit serial number' in line:
            details['Serial Number'] = line.split(':')[-1].strip()
    return details

def parse_capacity_data(capacity_data):
    details = {}
    lines = capacity_data.split('\n')
    read_capacity_16 = False

    for line in lines:
        if "READ CAPACITY (16)" in line:
            read_capacity_16 = True
        if read_capacity_16 and re.match(r'\s*[0-9a-fA-F]+\s+[0-9a-fA-F]+\s*', line):
            parts = line.split()
            if len(parts) >= 2:
                details['Capacity (blocks)'] = int(parts[0], 16)
                details['Block Size (bytes)'] = int(parts[1], 16)
                details['Total Capacity (bytes)'] = details['Capacity (blocks)'] * details['Block Size (bytes)']
                details['Total Capacity (GB)'] = details['Total Capacity (bytes)'] / (1024 ** 3)
    return details

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 wdscsi.py /dev/sdX")
        sys.exit(1)

    device_path = sys.argv[1]
    inquiry_data, capacity_data = get_drive_details(device_path)

    if inquiry_data and capacity_data:
        inquiry_details = parse_inquiry_data(inquiry_data)
        capacity_details = parse_capacity_data(capacity_data)

        print("Drive Details (Inquiry Data):")
        for key, value in inquiry_details.items():
            print(f"{key}: {value}")

        print("\nDrive Details (Capacity Data):")
        for key, value in capacity_details.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()

