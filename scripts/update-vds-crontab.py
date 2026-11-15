import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('2.27.101.128', username='root', password='aQsu1G72f!')

cron_content = """# Celebi Yonetim Cron Jobs
* * * * * python3 /var/www/scripts/timer-runner.py >> /var/log/celebi-timer.log 2>&1
0 */12 * * * python3 /var/www/scripts/fetch-gsc-keywords.py >> /var/log/celebi-gsc.log 2>&1
"""

stdin, stdout, stderr = client.exec_command(f'cat << \'EOF\' | crontab -\n{cron_content}\nEOF')
out = stdout.read().decode()
err = stderr.read().decode()
if err:
    print("Err:", err)

stdin, stdout, stderr = client.exec_command('crontab -l')
print("=== Current Crontab ===")
print(stdout.read().decode())
client.close()
