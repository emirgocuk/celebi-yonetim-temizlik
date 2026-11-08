import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('2.27.101.128', port=22, username='root', password='aQsu1G72f!', timeout=10)

cmds = """
set -e
mkdir -p /var/www/pocketbase
cd /tmp
rm -f pocketbase.zip
curl -fsSL -o pocketbase.zip "https://ganigeorgiev.com/meta/pocketbase/pocketbase/download/v0.41.1/pocketbase_0.41.1_linux_amd64.zip"
unzip -q -o pocketbase.zip -d /var/www/pocketbase/
chmod +x /var/www/pocketbase/pocketbase
rm -f pocketbase.zip

# Ensure systemd service exists and is configured
cat << 'EOF' > /etc/systemd/system/pocketbase.service
[Unit]
Description=PocketBase Service for Celebi Yonetim
After=network.target

[Service]
Type=simple
User=root
Group=root
LimitNOFILE=4096
WorkingDirectory=/var/www/pocketbase
ExecStart=/var/www/pocketbase/pocketbase serve --http=127.0.0.1:8090
Restart=always
RestartSec=5
StandardOutput=append:/var/log/pocketbase.log
StandardError=append:/var/log/pocketbase.error.log

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable pocketbase
systemctl restart pocketbase
sleep 2
systemctl status pocketbase --no-pager
curl -sI http://127.0.0.1:8090/api/health
"""

stdin, stdout, stderr = ssh.exec_command(cmds)
out = stdout.read().decode('utf-8', errors='ignore')
err = stderr.read().decode('utf-8', errors='ignore')
print("OUTPUT:\n", out)
if err.strip():
    print("ERR:\n", err)

ssh.close()

