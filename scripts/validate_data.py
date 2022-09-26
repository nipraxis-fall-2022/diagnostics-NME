""" Python script to validate data

Run as:

    python3 scripts/validata_data.py data
"""

from pathlib import Path
import sys
import hashlib


def file_hash(filename):
    """Get byte contents of file `filename`, return SHA1 hash

    Parameters
    ----------
    filename : str
        Name of file to read

    Returns
    -------
    hash : str
        SHA1 hexadecimal hash string for contents of `filename`.
    """
    # Open the file, read contents as bytes.
    # Calculate, return SHA1 has on the bytes from the file.
    # This is a placeholder, replace it to write your solution.
    fpath = Path(filename)
    con = fpath.read_bytes()
    hash_v = hashlib.sha1(con).hexdigest()
    # Your code here.

    # raise NotImplementedError(
    #     "This is just a template -- you are expected to code this."
    # )
    return hash_v


def validate_data(data_directory):
    """Read ``data_hashes.txt`` file in `data_directory`, check hashes

    Parameters
    ----------
    data_directory : str
        Directory containing data and ``data_hashes.txt`` file.

    Returns
    -------
    None

    Raises
    ------
    ValueError:
        If hash value for any file is different from hash value recorded in
        ``data_hashes.txt`` file.
    """
    # Read lines from ``data_hashes.txt`` file.
    # Split into SHA1 hash and filename
    # Calculate actual hash for given filename.
    # If hash for filename is not the same as the one in the file, raise
    # ValueError
    # This is a placeholder, replace it to write your solution.
    data_pth = Path() / data_directory
    # print(data_pth)
    hash_pth = list(data_pth.glob("**/*.txt"))
    hash_pth = str(hash_pth[0])
    # hash_pth= "data_pth/**/hash_list.txt"
    # print(hash_pth[0])

    # hash_pth = Path(data_directory)
    # hash_pth =  data_pth/group-0/'data_hashes.txt'
    # data_dir = hash_pth.parent
    with open(hash_pth) as f:
        lines = f.readlines()
        # print(lines)
        f.close()
    # Split into lines.
    # lines.strip()

    # For each line:
    for line in lines:
        # Split each line into expected_hash and filename
        spl = line.split()
        # Calculate actual hash for given filename.
        d_pth = list(data_pth.glob("**/*"))
        # print(d_pth)
        cal_hash = file_hash(data_pth / spl[1])
        # Check actual hash against expected hash
        act_hash = spl[0]
        # Return False if any of the hashes do not match.
        if cal_hash != act_hash:
            return False

        # raise NotImplementedError(
        #     "This is just a template -- you are expected to code this."
        # )
    return True


def main():
    # This function (main) called when this file run as a script.
    #
    # Get the data directory from the command line arguments
    if len(sys.argv) < 2:
        raise RuntimeError("Please give data directory on " "command line")
    data_directory = sys.argv[1]
    # Call function to validate data in data directory
    validate_data(data_directory)


if __name__ == "__main__":
    # Python is running this file as a script, not importing it.
    main()
