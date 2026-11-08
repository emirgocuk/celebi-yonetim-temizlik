import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('2.27.101.128', port=22, username='root', password='aQsu1G72f!', timeout=10)

# Generate self-signed cert for Cloudflare Full SSL mode
stdin, stdout, stderr = ssh.exec_command('openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj "/CN=celebiyonetim.com.tr"')
stdout.channel.recv_exit_status()

# Update Nginx config with both 80 and 443
nginx_conf = """server {
    listen 80 default_server;
    listen [::]:80 default_server;
    listen 443 ssl http2 default_server;
    listen [::]:443 ssl http2 default_server;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

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
with sftp.file('/etc/nginx/sites-available/celebiyonetim', 'w') as f:
    f.write(nginx_conf)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('nginx -t && systemctl reload nginx')
print("STDOUT:", stdout.read().decode())
print("STDERR:", stderr.read().decode())
ssh.close()
print("Cloudflare SSL readiness completed!")

