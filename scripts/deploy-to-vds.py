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
sftp.close()

stdin, stdout, stderr = ssh.exec_command(
    "rm -rf /var/www/celebiyonetim/html/* && "
    "tar -xzf /tmp/celebiyonetim_dist_update.tar.gz -C /var/www/celebiyonetim/html/ && "
    "rm -f /tmp/celebiyonetim_dist_update.tar.gz && "
    "chown -R www-data:www-data /var/www/celebiyonetim/html"
)
stdout.channel.recv_exit_status()
print("VDS Update Complete!")

if os.path.exists(temp_archive):
    os.remove(temp_archive)

ssh.close()

