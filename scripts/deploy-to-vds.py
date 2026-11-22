import hashlib
import os
import tarfile
import tempfile
import paramiko

SERVER_IP = "2.27.101.128"
USERNAME = "root"
PASSWORD = "aQsu1G72f!"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SERVER_IP, port=22, username=USERNAME, password=PASSWORD, timeout=10)

dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))
temp_archive = os.path.join(tempfile.gettempdir(), "celebiyonetim_dist_update.tar.gz")

with tarfile.open(temp_archive, "w:gz") as tar:
    for root, dirs, files in os.walk(dist_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, dist_dir)
            tar.add(full_path, arcname=rel_path)

sftp = ssh.open_sftp()
sftp.put(temp_archive, "/tmp/celebiyonetim_dist_update.tar.gz")

# Upload backend scripts
scripts_dir = os.path.abspath(os.path.dirname(__file__))
for script_name in ["timer-runner.py", "auto-generate-cron.py", "fetch-gsc-keywords.py", "gsc-auto-index.py"]:
    local_script = os.path.join(scripts_dir, script_name)
    if os.path.exists(local_script):
        sftp.put(local_script, f"/var/www/scripts/{script_name}")
        print(f"Uploaded {script_name} to /var/www/scripts/")

# Sync PocketBase pb_hooks/*.js if present and restart only on change
hooks_changed = False
local_hooks_dir = os.path.join(scripts_dir, "pb_hooks")
if os.path.isdir(local_hooks_dir):
    hook_files = sorted(f for f in os.listdir(local_hooks_dir) if f.endswith(".js"))
    if hook_files:
        _, out_md5, _ = ssh.exec_command("mkdir -p /var/www/pocketbase/pb_hooks && md5sum /var/www/pocketbase/pb_hooks/*.js 2>/dev/null || true")
        remote_hashes = {}
        for line in out_md5.read().decode("utf-8", errors="ignore").splitlines():
            parts = line.split(None, 1)
            if len(parts) == 2:
                remote_hashes[os.path.basename(parts[1].strip())] = parts[0].strip()

        for fname in hook_files:
            local_p = os.path.join(local_hooks_dir, fname)
            local_md5 = hashlib.md5(open(local_p, "rb").read()).hexdigest()
            if remote_hashes.get(fname) != local_md5:
                hooks_changed = True
            sftp.put(local_p, f"/var/www/pocketbase/pb_hooks/{fname}")
            print(f"Synced pb_hooks/{fname}")

sftp.close()

restart_pb_cmd = "systemctl restart pocketbase && " if hooks_changed else ""
stdin, stdout, stderr = ssh.exec_command(
    "rm -rf /var/www/celebiyonetim/html/* && "
    "tar -xzf /tmp/celebiyonetim_dist_update.tar.gz -C /var/www/celebiyonetim/html/ && "
    "rm -f /tmp/celebiyonetim_dist_update.tar.gz && "
    "chmod +x /var/www/scripts/*.py && "
    "chown -R www-data:www-data /var/www/celebiyonetim/html && "
    f"{restart_pb_cmd}"
    "systemctl reload nginx"
)
stdout.channel.recv_exit_status()
if hooks_changed:
    print("PocketBase restarted due to pb_hooks update.")
print("VDS Update Complete!")

# Submit updated sitemap to Google Search Console & IndexNow immediately
stdin2, stdout2, stderr2 = ssh.exec_command("python3 /var/www/scripts/gsc-auto-index.py --submit-all")
stdout2.channel.recv_exit_status()
print(stdout2.read().decode("utf-8", errors="ignore"))
err2 = stderr2.read().decode("utf-8", errors="ignore").strip()
if err2:
    print("[GSC/IndexNow STDERR]:", err2)

if os.path.exists(temp_archive):
    os.remove(temp_archive)

ssh.close()
