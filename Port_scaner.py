import socket
import time
import threading

#Banner
print("Simple Python Port Scanner")

target = input("Enter Target Ip or domain") #-asks user for the Ip or domain the program will check, along with the starting and end ports
try: #-Validating user input
    Start_Port= int(input(" Start port: "))
    End_port= int(input("End port: "))
    if not (0<= Start_Port <= 65535 and 0<= End_port <= 65535):
       raise ValueError
except ValueError:
    print("Invalid port range. Please enter numbers between 0 and 65535.")
    exit()

try: #-resolves domain name to ip
    ip = socket.gethostbyname(target)
    print(f"Resolved {target} to {ip}")
except socket.gaierror:
    print("Unable to resolve host. Check the domain name.")
    exit()
   

print(f"\nScanning {target} from port {Start_Port} to {End_port}...\n")

start_time= time.time() #-timer is started
open_ports = [] # Shared list for open ports
lock= threading.Lock() # To prevent race conditions when updating list

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    result = s.connect_ex((target, port))
    if result == 0:
        with lock:
            open_ports.append(port)
            print(f"Port {port}: OPEN")
    s.close()

threads = []

for port in range(Start_Port,End_port + 1):
    t = threading.Thread(target=scan_port,args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join() #Wait for all threads to finish

if not open_ports:
    print("No open ports found in the specified range.")


end_time= time.time()

print(f"\nScan completed in {round(end_time - start_time, 2)} seconds.")
