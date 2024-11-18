import os

FILE_BUF_SIZE = 1024 * 1024 * 64  # 64 MB buffer
SECTOR_SIZE = 2352  # CD-ROM sector size
DATA_OFFSET = 0x18  # Offset to data in Mode 1 sectors
DATA_SIZE = 2048  # Size of actual data in Mode 1 sectors

def convert_bin_to_iso(bin_file):
    try:
        # Generate output ISO filename by changing the extension
        base_name = os.path.splitext(bin_file)[0]
        iso_file = base_name + ".iso"

        print(f"Converting: {bin_file} -> {iso_file}")

        # Open the BIN file for reading
        with open(bin_file, "rb") as fp1:
            # Get file size
            fp1.seek(0, os.SEEK_END)
            fsize = fp1.tell()
            fp1.seek(0, os.SEEK_SET)

            # Open the ISO file for writing
            with open(iso_file, "wb") as fp2:
                # Set a large buffer for writing
                buf = bytearray(FILE_BUF_SIZE)

                cur = 0
                nold = 0

                # Process the BIN file sector by sector
                while True:
                    sector = fp1.read(SECTOR_SIZE)
                    if not sector:
                        break

                    # Extract and write the 2048-byte data part of the sector
                    fp2.write(sector[DATA_OFFSET:DATA_OFFSET + DATA_SIZE])

                    cur += SECTOR_SIZE
                    n = (cur * 100) // fsize
                    if n != nold:
                        print(".", end="", flush=True)
                        nold = n

        print("\nConversion complete:", iso_file)
        return 0

    except Exception as e:
        print(f"Error processing {bin_file}: {e}")
        return -1

def process_directory_recursively(directory):
    print(f"Scanning directory: {directory}")

    # Find all BIN files recursively
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".bin"):
                bin_file_path = os.path.join(root, file)
                convert_bin_to_iso(bin_file_path)

# Example usage
if __name__ == "__main__":
    # Replace this with your directory path
    input_directory = "./"  # Current directory
    process_directory_recursively(input_directory)
