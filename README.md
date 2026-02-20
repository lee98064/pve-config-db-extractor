# Proxmox VE config.db Extractor

A lightweight Python script to extract and restore configuration files from a Proxmox VE (PVE) `config.db` database. 

When a PVE node fails, you might only have a backup of the `/var/lib/pve-cluster/config.db` file (which is the SQLite database powering the Proxmox Cluster File System, `pmxcfs`). This script allows you to easily extract all your VM (`.conf`), LXC, and cluster configuration files directly from the database without needing to spin up a PVE environment or manually mount the filesystem.

## ✨ Features

* **Zero Dependencies:** Uses only Python's built-in `sqlite3` and `os` libraries. No need to `pip install` anything.
* **Preserves Directory Structure:** Reconstructs the exact folder hierarchy as it appears in `/etc/pve/` (e.g., `qemu-server/100.conf`, `lxc/101.conf`, `corosync.conf`).
* **Cross-Platform:** Works on Linux, macOS, and Windows.

## 🚀 Usage

1. **Clone the repository or download the script:**
   ```bash
   git clone [https://github.com/yourusername/pve-config-extractor.git](https://github.com/yourusername/pve-config-extractor.git)
   cd pve-config-extractor
   ```

2. **Prepare your database file:**
   Place your rescued `config.db` file in the same directory as the script.

3. **Run the script:**
   ```bash
   python extract_pve.py
   ```

4. **Check the output:**
   By default, the script will create a new directory named `pve_configs_backup` and extract all files there.

   *Example Output:*
   ```text
   Extracted: qemu-server/100.conf
   Extracted: qemu-server/101.conf
   Extracted: lxc/200.conf
   Extracted: corosync.conf
   Extracted: storage.cfg
   ----------------------------------------
   ✅ Extraction complete! Restored 35 files.
   Files saved to: /path/to/your/pve_configs_backup
   ```

## ⚙️ Configuration

If you want to use a different database name or output directory, you can easily modify the variables at the bottom of the `extract_pve.py` file:

```python
if __name__ == "__main__":
    # ===== Configuration =====
    DATABASE_FILE = "config.db"           # Path to your PVE database
    OUTPUT_FOLDER = "pve_configs_backup"  # Desired output directory
    # =========================
```

## ⚠️ Disclaimer

This tool is designed for data recovery and offline inspection. It strictly performs read-only operations on your `config.db`. However, always make sure to keep a backup of your original `config.db` before proceeding.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
