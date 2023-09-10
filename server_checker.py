import threading
import socket
import time
import random

# config
ip_list = 'cf_ips.txt'
ip_list = 'fofa_cf.txt'
output = 'valid_ip.txt'
num_threads = 100
timeout = 200/1000
default_port = 443
# ----------

ip_list = open(ip_list, 'r').read().splitlines()
total_line = len(ip_list)

output = open(output, 'w')

count = 0
def check_ip(ip):
    global count
    
    print(f'{format(count/total_line*100,".2f")}% checking: {ip}')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        c_ip = ip
        c_port = default_port
        ip_port = ip.split(':')
        if len(ip_port) == 2:
            c_ip = ip_port[0]
            c_port = int(ip_port[1])
        
        result = s.connect_ex((c_ip, c_port))
        
        if result == 0:
            return ip
    except Exception as e:
        print(e)
        pass
    finally:
        s.close()
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

threads = []
for i in range(num_threads):
    thread = threading.Thread(target=thread_function, args=())
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print('Done')