import os
import sys
import urllib.request
import glob

HOP_LIB_DIR = r"C:\hop\lib"
CONNECTOR_VERSION = "8.4.0"
CONNECTOR_JAR = f"mysql-connector-j-{CONNECTOR_VERSION}.jar"
MAVEN_URL = f"https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/{CONNECTOR_VERSION}/{CONNECTOR_JAR}"

def main():
    print("=" * 60)
    print("MySQL Connector/J Setup for Apache Hop")
    print("=" * 60)

    if not os.path.isdir(HOP_LIB_DIR):
        print(f"[ERROR] Target directory '{HOP_LIB_DIR}' does not exist.")
        sys.exit(1)

    # Check for existing mysql connectors in both lib and lib/jdbc
    jdbc_dir = os.path.join(HOP_LIB_DIR, "jdbc")
    if os.path.isdir(jdbc_dir):
        existing_jdbc_jars = glob.glob(os.path.join(jdbc_dir, "*mysql*.jar"))
        if not existing_jdbc_jars:
            # Check if jar exists in lib and copy to jdbc
            lib_jars = glob.glob(os.path.join(HOP_LIB_DIR, "*mysql*.jar"))
            for jar in lib_jars:
                import shutil
                shutil.copy2(jar, os.path.join(jdbc_dir, os.path.basename(jar)))
                print(f"[INFO] Copied {os.path.basename(jar)} to {jdbc_dir}")

    existing_jars = glob.glob(os.path.join(HOP_LIB_DIR, "*mysql*.jar"))
    if existing_jars:
        print(f"[INFO] Found existing MySQL driver(s) in {HOP_LIB_DIR}:")
        for jar in existing_jars:
            print(f"  - {os.path.basename(jar)} ({os.path.getsize(jar)} bytes)")
        print("[SUCCESS] MySQL driver is already installed.")
        return

    dest_path = os.path.join(HOP_LIB_DIR, CONNECTOR_JAR)
    print(f"[INFO] Downloading {CONNECTOR_JAR} from:")
    print(f"       {MAVEN_URL}")
    print(f"[INFO] Destination: {dest_path}")

    try:
        def reporthook(blocknum, blocksize, totalsize):
            readsofar = blocknum * blocksize
            if totalsize > 0:
                percent = readsofar * 1e2 / totalsize
                s = f"\rDownloading: {percent:5.1f}% [{readsofar} / {totalsize} bytes]"
                sys.stdout.write(s)
                sys.stdout.flush()

        urllib.request.urlretrieve(MAVEN_URL, dest_path, reporthook)
        print("\n[SUCCESS] Download completed.")
        
        file_size = os.path.getsize(dest_path)
        print(f"[INFO] File size: {file_size:,} bytes")
        if file_size < 100000:
            print("[WARNING] Downloaded file seems suspiciously small. Please check file integrity.")
            sys.exit(1)
        else:
            print(f"[SUCCESS] {CONNECTOR_JAR} successfully placed into {HOP_LIB_DIR}")
            if os.path.isdir(jdbc_dir):
                import shutil
                shutil.copy2(dest_path, os.path.join(jdbc_dir, CONNECTOR_JAR))
                print(f"[SUCCESS] {CONNECTOR_JAR} also copied to {jdbc_dir}")
    except Exception as e:
        print(f"\n[ERROR] Failed to download MySQL Connector/J: {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)
        sys.exit(1)

if __name__ == "__main__":
    main()
