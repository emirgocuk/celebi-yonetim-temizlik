import os
import sys
import tarfile
import tempfile
import paramiko

SERVER_IP = "2.27.101.128"
USERNAME = "root"
PASSWORD = "aQsu1G72f!"

def run_ssh_command(ssh, cmd, check=True):
    print(f"--> [CMD]: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    exit_status = stdout.channel.recv_exit_status()
    if out.strip():
        print(f"STDOUT:\n{out.strip()}")
    if err.strip():
        print(f"STDERR:\n{err.strip()}")
    if check and exit_status != 0:
        raise RuntimeError(f"Command '{cmd}' failed with exit code {exit_status}")
    return out, err, exit_status

def main():
    print(f"Connecting to {SERVER_IP} via SSH...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, port=22, username=USERNAME, password=PASSWORD, timeout=15)
    print("SSH Connection established successfully.\n")

    # 1. Swap Setup (2GB) if no swap exists
    print("=== Step 1: Swap Memory Check ===")
    out, _, _ = run_ssh_command(ssh, "free -m | grep Swap")
    if " 0 " in out or out.endswith(" 0") or "0B" in out:
        print("Creating 2GB swap file for memory stability...")
        swap_cmds = (
            "fallocate -l 2G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=2048 && "
            "chmod 600 /swapfile && "
            "mkswap /swapfile && "
            "swapon /swapfile && "
            "grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab"
        )
        run_ssh_command(ssh, swap_cmds)
    else:
        print("Swap already configured.")

    # 2. Package updates & installations
    print("\n=== Step 2: Essential Packages (Nginx, UFW, Unzip, Certbot) ===")
    pkg_cmd = (
        "DEBIAN_FRONTEND=noninteractive apt-get update && "
        "DEBIAN_FRONTEND=noninteractive apt-get install -y nginx ufw curl unzip certbot python3-certbot-nginx"
    )
    run_ssh_command(ssh, pkg_cmd)

    # 3. UFW Firewall Setup
    print("\n=== Step 3: Firewall (UFW) Configuration ===")
    ufw_cmds = (
        "ufw allow 22/tcp && "
        "ufw allow 80/tcp && "
        "ufw allow 443/tcp && "
        "echo 'y' | ufw enable"
    )
    run_ssh_command(ssh, ufw_cmds)

    # 4. PocketBase Setup
    print("\n=== Step 4: PocketBase Binary & Systemd Service ===")
    pb_cmds = """
mkdir -p /var/www/pocketbase
if [ ! -f /var/www/pocketbase/pocketbase ]; then
    echo "Downloading PocketBase..."
    cd /tmp
    curl -fsSL -o pocketbase.zip https://github.com/pocketbase/pocketbase/releases/download/v0.25.9/pocketbase_0.25.9_linux_amd64.zip
    unzip -q -o pocketbase.zip -d /var/www/pocketbase/
    chmod +x /var/www/pocketbase/pocketbase
    rm -f pocketbase.zip
fi
"""
    run_ssh_command(ssh, pb_cmds)

    # Create pocketbase.service
    service_content = """[Unit]
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
"""
    # Write systemd file
    sftp = ssh.open_sftp()
    with sftp.file("/etc/systemd/system/pocketbase.service", "w") as f:
        f.write(service_content)
    sftp.close()

    run_ssh_command(ssh, "systemctl daemon-reload && systemctl enable pocketbase && systemctl restart pocketbase")

    # 5. Nginx Configuration
    print("\n=== Step 5: Nginx Virtual Host Configuration ===")
    nginx_conf = """server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name celebiyonetim.com.tr www.celebiyonetim.com.tr 2.27.101.128 _;

    root /var/www/celebiyonetim/html;
    index index.html;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript application/rss+xml application/atom+xml image/svg+xml;

    # Static Assets Cache (Immutable 1 Year)
    location /_astro/ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    # PocketBase Admin UI & API Reverse Proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8090/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /_/ {
        proxy_pass http://127.0.0.1:8090/_/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # SPA / Astro Static Fallback
    location / {
        try_files $uri $uri/ /index.html;
    }
}
"""
    sftp = ssh.open_sftp()
    with sftp.file("/etc/nginx/sites-available/celebiyonetim", "w") as f:
        f.write(nginx_conf)
    sftp.close()

    run_ssh_command(ssh, "mkdir -p /var/www/celebiyonetim/html")
    run_ssh_command(ssh, "ln -sf /etc/nginx/sites-available/celebiyonetim /etc/nginx/sites-enabled/celebiyonetim")
    run_ssh_command(ssh, "rm -f /etc/nginx/sites-enabled/default")
    run_ssh_command(ssh, "nginx -t && systemctl reload nginx")

    # 6. Upload Astro Static Build
    print("\n=== Step 6: Upload Astro Build to /var/www/celebiyonetim/html ===")
    dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist"))
    if not os.path.exists(dist_dir):
        raise FileNotFoundError(f"Dist dir {dist_dir} does not exist. Run npm run build first.")

    # Create a tar.gz locally for super fast single-file transfer
    temp_archive = os.path.join(tempfile.gettempdir(), "celebiyonetim_dist.tar.gz")
    print(f"Creating local tar.gz from {dist_dir}...")
    with tarfile.open(temp_archive, "w:gz") as tar:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, dist_dir)
                tar.add(full_path, arcname=rel_path)

    print(f"Uploading {temp_archive} to server...")
    sftp = ssh.open_sftp()
    sftp.put(temp_archive, "/tmp/celebiyonetim_dist.tar.gz")
    sftp.close()

    print("Extracting files on server...")
    run_ssh_command(ssh, "rm -rf /var/www/celebiyonetim/html/* && tar -xzf /tmp/celebiyonetim_dist.tar.gz -C /var/www/celebiyonetim/html/ && rm -f /tmp/celebiyonetim_dist.tar.gz")
    run_ssh_command(ssh, "chown -R www-data:www-data /var/www/celebiyonetim/html")

    # Cleanup local temp
    if os.path.exists(temp_archive):
        os.remove(temp_archive)

    # 7. Verification
    print("\n=== Step 7: Local Server Verification ===")
    run_ssh_command(ssh, "systemctl status pocketbase --no-pager | head -n 12")
    run_ssh_command(ssh, "curl -sI http://127.0.0.1 | head -n 10")
    run_ssh_command(ssh, "curl -sI http://127.0.0.1:8090/api/health")

    ssh.close()
    print("\n*** ALL SERVER SETUP COMPLETED SUCCESSFULLY! ***")

if __name__ == "__main__":
    main()

