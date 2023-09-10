import threading
import urllib3
import urllib.parse
import time

# config
url = 'https://www.cloudflare.com/ips-v6'
num_threads = 60
ip_list = 'valid_ip.txt'
output = 'cf_checked.txt'
timeout = 150/1000
# ----------

host = urllib.parse.urlsplit(url).hostname

ip_list = open(ip_list, 'r').read().splitlines()

total_line = len(ip_list)

output = open(output, 'w')

count = 0
def check_ip(ip):
    global count
    print(f'{format(count/total_line*100,".2f")}% checking: {ip}')
    
    try:
        pool = urllib3.HTTPSConnectionPool(ip, server_hostname=host,retries=False) 
        response = pool.urlopen('GET',url, assert_same_host=False, timeout=timeout)
        
        if response.status == 200:
            return ip
        return None
    except:
        return None

def thread_function():
    while(True):
        global count
        line_count = count
        count += 1
        if(line_count < total_line):
            ip = ip_list[line_count]
            valid_ip = check_ip(ip)
            if valid_ip:
                global output
                output.write(f'{valid_ip}\n')
                output.flush()
        else:
            break

start = time.time()
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=thread_function, args=())
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f'time: {time.time() - start}s')
print('Done')
