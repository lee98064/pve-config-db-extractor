import sqlite3
import os

def extract_pve_config(db_path, output_dir):
    # Check if the database file exists
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found")
        return

    # Create the main output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Fetch all nodes from the tree table (including directories and files)
        # type: 4 represents directories, 8 represents regular files
        cursor.execute("SELECT inode, parent, type, name, data FROM tree")
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        print("Error: This does not appear to be a valid PVE config.db format (tree table not found).")
        return

    # Step 1: Build a dictionary of directories for path reconstruction
    directories = {}
    for row in rows:
        inode, parent, ftype, name, data = row
        if ftype == 4:
            directories[inode] = {"parent": parent, "name": name}

    # Helper function: Traverse upward through parent_inode to construct the full relative path
    def get_full_path(parent_inode):
        path_parts = []
        curr = parent_inode
        seen = set() # Prevent infinite loops from corrupted database structure
        while curr in directories and curr not in seen:
            seen.add(curr)
            if directories[curr]["name"]:
                path_parts.insert(0, directories[curr]["name"])
            curr = directories[curr]["parent"]
        return os.path.join(*path_parts) if path_parts else ""

    extracted_count = 0

    # Step 2: Iterate through all files and write them to disk
    for row in rows:
        inode, parent, ftype, name, data = row
        # Filter files (type == 8) with non-empty data
        if ftype == 8 and data is not None:
            # Get the directory path where the file is located
            dir_path = get_full_path(parent)
            full_dir_path = os.path.join(output_dir, dir_path)

            # Create the directory if it doesn't exist
            if not os.path.exists(full_dir_path):
                os.makedirs(full_dir_path)

            # Construct the final file path
            file_path = os.path.join(full_dir_path, name)

            # Write file in binary mode (wb) to avoid text encoding issues
            with open(file_path, 'wb') as f:
                f.write(data)
            
            extracted_count += 1
            print(f"Extracted: {os.path.join(dir_path, name)}")

    conn.close()
    print("-" * 40)
    print(f"✅ Extraction complete! Restored {extracted_count} files.")
    print(f"Files saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    # ===== Modify your file paths here =====
    DATABASE_FILE = "config.db"           # Path to your config.db file
    OUTPUT_FOLDER = "pve_configs_backup"  # Output folder name
    # ========================================
    
    extract_pve_config(DATABASE_FILE, OUTPUT_FOLDER)
