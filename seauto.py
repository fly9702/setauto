# import time
import netmiko
import paramiko
import pymysql
import os

acase_list = ["router","switch","server"]
scase_list = []
# cmd path list = cmd 파일의 경로값이 저장되어 있는 dict
ahost_list = [] # all host list =  특정 파일에서 읽어온 모든 host가 담긴 리스트
shost_list= [] # selected host list = 사용자가 선택한 host들이 담긴 list
cmd_list = [] # all cmd list = 사용자가 고른 파일 유형에 맞는 모든 명령어 목록을 담을 함수
scnt = 0 #스위치 반복시 증가하는 값

# db 질의 def query(database,cmd) return rows
def query(database,cmd):
    ip = "DB ip"
    port = "3306"
    id = "DB id"
    pw = "DB password"
    db = pymysql.connect(host=ip, user=id, passwd=pw, charset='utf8', db=database)
    #db 객체를 호출하는 cursor 생성
    cur = db.cursor()
    cur.execute(cmd)
    rows = []
    if "SELECT" in cmd or "SHOW" in cmd:
        rows = cur.fetchall()   # DBMS에서 전달하는 응답값을 가져온다.
    elif "INSERT" in cmd:
        db.commit()
        rows = ["query ok"]
    return list(rows)


#1. 파일 선택 def selcase(fpath_list) return x
def selcase(acase_list, scase_list) :

    print("전체 케이스 목록입니다.")
    cnt = 1
    for i in acase_list :
        print("%d. %s"%(cnt,i),end="  ")
        cnt += 1
    txt = input("선택하려는 케이스의 번호를 ,를 붙여서 입력해주세요.").split(",")
    
    for k in txt :
        if k.isdigit() :
        	index = int(k)-1
        	scase_list.append(acase_list[index])
        else :
            print("숫자를 입력해주세요")

#2. 호스트 정보 읽고 저장 def gethost
def gethost(case) :
    cmd = "SELECT * from host"
    rows = query(case,cmd)
    for i in rows:
        #print(i)
        host = {}
        host["hostname"] = i[0]
        host["ip"] = i[1]
        host["username"] = i[2]
        host["password"] = i[3]
        if len(i) == 5 :
            host["os"] = i[4]
        ahost_list.append(host.copy())
        

#3. 전체 호스트 보여주고 선택한 호스트 저장 def selhost(ahost_list, shost_list) return x
def selhost(case,ahost_list, shost_list) :
    print("전체 호스트 목록입니다.")
    cnt = 1
    for i in ahost_list :
        print("%d. %s"%(cnt,i["hostname"]),end="  ")
        cnt += 1
        
    #수동화
    txt = input("선택하려는 호스트의 번호를 ,를 붙여서 입력해주세요.").split(",")

    #자동화
    """
    if case == "router":
        #txt = "2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17"
        txt = "2,3,4,5,6,7,8,9,10,14,15,16,17"
    elif case == "switch":
        txt = "1"
    elif case == "server":
        txt = ""
    txt = txt.split(",")
    """
    
    for k in txt :
        if k.isdigit() :
            index = int(k)-1
            shost_list.append(ahost_list[index])
        else :
            print("숫자를 입력해주세요")

#4. 명령어 정보 읽고 저장 def getcmd(cpath) return x
def getcmd(case) :
    if case in ("router","switch"):
        cmd = "SHOW tables like 'set_%'"
        rows = query(case,cmd)
        rows = list(rows[1:])
        result = []
        for a in rows:
            a = str(a)
            a = a[2:-3]
            result.append(a)
    elif case == "server":
        result = ["key_exchange", "smb_server", "smb_client", "dns_server", "ftp_login", "ftp_anonymous", "install_php",
                 "nginx", "nfs_server", "nfs_client", "install_mariadb", "pydio", "joomla", "wp", "monitorix_server",
                 "monitorix_client", "mrtg"]
    return result
    
        

#5. 전체 명령어 보여주고 선택한 명령어 저장 def selcmd(shost_list, cmd_list) return x
def selcmd(case,host, cmd_list) :
    
    print("현재 호스트는 %s 입니다."%(host["hostname"]))
    print("전체 명령어는 다음과 같습니다.")
    cnt = 1
    host["cmd"] = []
    txt = ""    
    for j in cmd_list:
    	print("%d. %s"%(cnt,j))
    	cnt += 1

    #수동화
    #txt = input("선택하려는 명령어의 번호를 ,를 붙여서 입력해주세요.").split(",")

    #테스트
    txt = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17".split(",")
    
    #자동화
    """
    if case == "router" :
        if host["hostname"] == "R01":
            txt = "7,5,9,14,16"
        elif host["hostname"] == "R02":
            txt = "1,7,5,15,16,9,10,11,12,14"
        elif host["hostname"] == "R03":
            txt = "1,7,5,15,16,4,9,12,14,13,2"
        elif host["hostname"] == "R04":
            txt = "7,5,15,16,9,12"
        elif host["hostname"] == "R05":
            txt = "7,15,16,9"
        elif host["hostname"] == "R06":
            txt = "7,15,16,9,3"
        elif host["hostname"] == "R07":
            txt = "7,15,16,9"
        elif host["hostname"] == "R08":
            txt = "1,7,15,16,9,12,3,6,8,13"
        elif host["hostname"] == "R09":
            txt = "1,7,15,16,9,12,6,8,13"
        elif host["hostname"] == "R10":
            txt = "7,15,16,9"
        elif host["hostname"] == "R11":
            txt = "7,15,16,9,3"
        elif host["hostname"] == "R12":
            txt = "7,15,16,9,3"
        elif host["hostname"] == "R13":
            txt = "1,7,15,16,9,2"
        elif host["hostname"] == "R14":
            txt = "7,15,16,9"
        elif host["hostname"] == "R15":
            txt = "7,15,16,9"
        elif host["hostname"] == "R16":
            txt = "7,15,16,9"
    elif case == "switch":
        if host["hostname"] == "ESW1":
            txt = "7,5,9,14,16"
        elif host["hostname"] == "ESW2":
            txt = "7,5,9,14,16"
    elif case == "server" :
        if host["hostname"] == "Rocky1":
            txt = "7,5,9,14,16"
        elif host["hostname"] == "Ubuntu1":
            txt = "7,5,9,14,16"
    txt = txt.split(",")
    """
    
    for k in txt :
        if k.isdigit() :
            index = int(k) - 1
            host["cmd"].append(cmd_list[index])


#6. 명령어 전달 및 결과값 저장 def para_connect(user) return result
#6. 명령어 전달 및 결과값 저장 def para_connect(user) return result
def para_connect(cmd,time1) :
    print("connect 시작")
    ip = "172.16.0.101"
    user = "root"
    pwd = "asd123!@"
    cli = paramiko.SSHClient() # ssh 클라이언트 인스턴스를 생성 ---> cli 객체
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)  # 접속할 때 에러 메시지 처리 
    cli.connect(ip,username=user,password=pwd) #ip,username,password로 ssh 연결
    connection = cli.invoke_shell()

    idle_time = 120
    time.sleep(1)  # 초기 버퍼 비우기
    if connection.recv_ready():
        connection.recv(65535)

    cmd_list = cmd.strip().split("\n")
    result_all = ""

    for cmd_item in cmd_list:
        print(f"▶ {cmd_item} 실행 중...")
        connection.send(cmd_item + "\n")
        result = ""
        last_data_time = time.time()

        while True:
            time.sleep(0.2)
            if connection.recv_ready():
                chunk = connection.recv(65535).decode('utf-8')
                result += chunk
                last_data_time = time.time()
            elif time.time() - last_data_time > idle_time:
                # idle_time 동안 데이터가 안 들어오면 종료된 것으로 판단
                break

        print(f"⏹ {cmd_item} 완료")
        result_all += f"\n\n==== {cmd_item} 결과 ====\n{result}"

    cli.close()
    
    return result_all # 디코드된 결과값 리턴

#6. 명령어 전달 및 결과값 저장 def net_connect(user) return result
def net_connect (host, cmd,time1):
    net_connect = netmiko.ConnectHandler(device_type="cisco_ios", ip=host["ip"],username=host["username"],password=host["password"],timeout=15) # ssh 연결
    net_connect.enable() #관리자 모드 실행
    cmdt = cmd.strip()
    #print(" %s를 시작합니다."%(cmdt)) # 명령어 시작 알림
    tmp = cmd.split("\n")
    if len(tmp) == 1 :
        result =net_connect.send_command(tmp[0])
    else :
        result = net_connect.send_config_set(tmp)
    time.sleep(time1)
    #print(result)
    #print(" %s가 완료되었습니다."%(cmdt)) # 명령어 완료 알림
    net_connect.disconnect()

    return result 
            



    
#라우트 함수

def set_create_accesslist(host):
    print("start set_create_accesslist")
    cmd = "SELECT * FROM set_create_accesslist WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        if int(a[1]) < 100 :
            cmd += "access-list %s %s %s %s \n" % (a[1],a[2],a[4],a[5]) 
        elif int(a[1]) > 100 :
            cmd += "access-list %s %s %s %s %s %s %s \n" % (a[1],a[2],a[3],a[4],a[5],a[6],a[7])
          
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_gw(host):
    print("start set_gw")
    cmd = "SELECT * FROM set_gw WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "int %s \n" % (a[1])
        cmd += "ip add %s %s \n" % (a[2],a[3]) 
        cmd += "no sh \n"
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_static_routing(host):
    print("start set_static_routing")
    cmd = "SELECT * FROM set_static_routing WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
#    if len(data) == 1 :
#        cmd += "conf t"
    for a in data:
        #print(a)
        cmd += "ip route %s %s %s \n" % (a[1], a[2], a[3])   
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_rip(host):
    print("start set_rip")
    cmd = "SELECT * FROM set_rip WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    cmd += "router rip \n"
    cmd += "no au \n"
    cmd += "ver 2 \n"
    for a in data:
        #print(a)
        cmd += "network %s \n"%(a[1])
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

    
def set_eigrp(host):
    print("start set_eigrp")
    cmd = "SELECT * FROM set_eigrp WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "router eigrp %s \n" % (a[1])
        cmd += "no au \n"
        cmd += "network %s %s \n"%(a[2],a[3])
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_pat(host):
    print("start set_pat")
    cmd = "SELECT * FROM set_pat WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "int %s \n" % (a[1])
        cmd += "ip nat inside \n"
        cmd += "int %s \n" % (a[2])
        cmd += "ip nat outside \n" 
    cmd += "exit \n"
    for a in data:
        cmd += "ip nat pool %s %s %s netmask %s \n"%(a[3],a[4],a[5],a[6])
        cmd += "ip nat inside source list %s pool %s overload \n"%(a[7],a[3])
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_intervlan(host):
    print("start set_intervlan")
    cmd = "SELECT * FROM set_intervlan WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    cmd += "int %s \n"%(data[0][1])
    cmd += "no sh \n"
    for a in data:
        #print(a)
        cmd += "int %s.%s \n"%(a[1],a[4])
        cmd += "enc dot1q %s \n"%(a[4])   
        cmd += "ip add %s %s \n"%(a[2],a[3])
        cmd += "no sh \n"
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_dhcp(host):
    print("start set_dhcp")
    cmd = "SELECT * FROM set_dhcp WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "ip dhcp pool %s \n" % (a[1])
        cmd += "network %s %s \n"%(a[2],a[3])
        cmd += "dns-server %s \n"%(a[4])
        cmd += "default-router %s \n"%(a[5])
        cmd += "exit \n"%()
        cmd += "ip dhcp excluded-address %s %s \n"%(a[6],a[7])
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_glbp(host):
    print("start set_glbp")
    cmd = "SELECT * FROM set_glbp WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "int %s \n"%(a[1]) 
        cmd += "glbp %s ip %s \n"%(a[2],a[3])
        cmd += "glbp %s priority %s \n"%(a[2],a[4])
        cmd += "glbp %s preempt \n"%(a[2])
        cmd += "glbp %s load-balancing %s \n"%(a[2],a[5])
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_redistribute(host):
    print("start set_redistribute")
    cmd = "SELECT * FROM set_redistribute WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "router %s \n" % (a[1])
        cmd += "redistribute %s metric %s \n"%(a[2],a[3])
    cmd += "end \n"
    result = net_connect(host,cmd,5)
    return result

def set_offset(host):
    print("start set_offset")
    cmd = "SELECT * FROM set_offset WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "router %s \n"%(a[1])
        cmd += "offset-list %s %s %s %s \n"%(a[2],a[3],a[4],a[5])
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_distribute(host):
    print("start set_distribute")
    cmd = "SELECT * FROM set_distribute WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "router %s \n" % (a[1])   
        cmd += "distribute-list %s %s %s \n" % (a[2],a[3],a[4]) 
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_accesslist(host):
    print("start set_accesslist")
    cmd = "SELECT * FROM set_accesslist WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "int %s \n" % (a[1])   
        cmd += "ip access-group %s %s \n" % (a[2],a[3]) 
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_passive(host):
    print("start set_passive")
    cmd = "SELECT * FROM set_passive WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "router %s \n" % (a[1])   
        cmd += "passive %s \n" % (a[2])  
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_manual_summary(host):
    print("start set_manual_summary")
    cmd = "SELECT * FROM set_manual_summary WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "int %s \n" % (a[1])   
        cmd += "ip summary-address %s %s %s \n" % (a[2],a[3],a[4])
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_key_chain(host):
    print("start set_key_chain")
    cmd = "SELECT * FROM set_key_chain WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "key chain %s \n" % (a[1])   
        cmd += "key %s \n" % (a[2])
        cmd += "key-string %s \n" % (a[3])
        cmd += "end \n"
        cmd += "conf t \n"
        cmd += "int %s \n" % (a[4])
        if a[5] == "rip":
            cmd += "ip rip authentication mode %s \n" % (a[6])
            cmd += "ip rip authentication key-chain %s \n" % (a[1])
        elif "eigrp" in a[5]:
            cmd += "ip authentication mode %s %s \n" % (a[5],a[6])
            cmd += "ip authentication key-chain %s %s \n" % (a[5],a[1])
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result


    
#스위치 함수

def set_vlan(host):
    cmd = "SELECT * FROM set_vlan WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = "end \n"
    cmd += "vlan da \n"
    for a in data:
        cmd += "vlan %s \n"%a[1]
    
        
    cmd += "exit \n"
    result = net_connect(host,cmd,5)
    return result

def set_vtp(host):
    cmd = "SELECT * FROM set_ WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd += "end \n"   
    cmd += "vlan da \n"  
    for a in data:
        #print(a)
        cmd += "vtp %s \n"
        cmd += "vtp domain %s \n"  
        cmd += "vtp password %s \n"  
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

def set_span(host):
    cmd = "SELECT * FROM set_ WHERE hostname = '%s'"%(host["hostname"])
    data = query("router",cmd)
    cmd = ""
    for a in data:
        #print(a)
        cmd += "monitor session %s %s int %s %s \n" % (a[1],a[2],a[3],a[4])   
    cmd += "end"
    result = net_connect(host,cmd,5)
    return result

# 명령어 결과 백업 관련 함수들

def backup(hostname,case,result) :
    cmd = "INSERT INTO network (hostname, type, data) VALUES ('%s', '%s', '%s'); "%(hostname,case,result)
    result = query("backup",cmd)
    print(result)

#테스트 함수
def ping(case,host) :
    print(host)
    cmd = """
end \n
ping 172.16.0.180 repeat 1 timeout 1 \n
ping 172.16.0.131 repeat 1 timeout 1 \n
ping 10.0.0.2 repeat 1 timeout 1 \n
ping 10.8.0.2 repeat 1 timeout 1 \n
ping 10.16.0.2 repeat 1 timeout 1 \n
ping 10.80.0.2 repeat 1 timeout 1 \n
ping 10.84.0.2 repeat 1 timeout 1 \n
ping 10.64.0.2 repeat 1 timeout 1 \n
ping 10.68.0.2 repeat 1 timeout 1 \n
ping 10.72.0.2 repeat 1 timeout 1 \n
ping 10.96.0.2 repeat 1 timeout 1 \n
ping 10.100.0.2 repeat 1 timeout 1 \n
ping 10.108.0.2 repeat 1 timeout 1 \n
ping 10.192.0.2 repeat 1 timeout 1 \n
ping 10.136.0.2 repeat 1 timeout 1 \n
ping 10.152.0.2 repeat 1 timeout 1 \n
ping 10.144.0.2 repeat 1 timeout 1 \n
"""
    if case == "switch" :
        cmd += """
"""
    print("connect start")
    result = net_connect(host, cmd, 5)
    print("connect finish")
    #print(cmd)
    #result = 1

    return result



#서버 함수
def key_exchange(host):
    command = ""
    command += "export ANSIBLE_HOST_KEY_CHECKING=False\n"
    command += 'cd /home/smt/ansible\n'
    command += """ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i "%s," ssh.yaml --extra-vars "target_host=all" -u root -k -K\n""" % host["ip"]
    command += "asd123!@\n"
    command += "asd123!@\n"

    result = para_connect(command, 7)
    return result

def smb_server(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    if host["os"] == "rocky":
        command += """ansible-playbook -i "%s," rocky_smb_server.yaml -u root"""%host["ip"]
    else:
        command += """ansible-playbook -i "%s," ubuntu_smb_server.yaml -u root"""%host["ip"]

    result = para_connect(command, 20)
    return result

def smb_client(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    if host["os"] == "rocky":
        command += """ansible-playbook -i "%s," rocky_smb_client.yaml -u root"""%host["ip"]
    else:
        command += """ansible-playbook -i "%s," ubuntu_smb_client.yaml -u root"""%host["ip"]

    result = para_connect(command, 20)
    return result

def dns_server(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    if host["os"] == "rocky":
        command += """ansible-playbook -i "%s," rocky_dns.yaml -u root"""%host["ip"]
    else:
        command += """ansible-playbook -i "%s," ubuntu_dns.yaml -u root"""%host["ip"]

    result = para_connect(command, 20)
    return result

def ftp_login(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    if host["os"] == "rocky":
        command += """ansible-playbook -i "%s," rocky_ftp_login.yaml -u root"""%host["ip"]
    else:
        command += """ansible-playbook -i "%s," ubuntu_ftp_login.yaml -u root"""%host["ip"]

    result = para_connect(command, 20)
    return result

def ftp_anonymous(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    if host["os"] == "rocky":
        command += """ansible-playbook -i "%s," rocky_ftp_anonymous.yaml -u root"""%host["ip"]
    else:
        command += """ansible-playbook -i "%s," ubuntu_ftp_anonymous.yaml -u root"""%host["ip"]

    result = para_connect(command, 20)
    return result

def install_php(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    if host["os"] == "rocky":
        command += """ansible-playbook -i "%s," rocky_php_auto.yaml -u root"""%host["ip"]
    else:
        command += """ansible-playbook -i "%s," ubuntu_php_auto.yaml -u root"""%host["ip"]

    result = para_connect(command, 120)
    return result

def nginx(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    if host["os"] == "rocky":
        command += """ansible-playbook -i "%s," rocky_nginx.yaml -u root"""%host["ip"]
    else:
        command += """ansible-playbook -i "%s," ubuntu_nginx.yaml -u root"""%host["ip"]

    result = para_connect(command, 20)
    return result

def nfs_server(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    if host["os"] == "rocky":
        command += """ansible-playbook -i "%s," rocky_nfs_server.yaml -u root"""%host["ip"]
    else:
        command += """ansible-playbook -i "%s," ubuntu_nfs_server.yaml -u root"""%host["ip"]

    result = para_connect(command, 25)
    return result

def nfs_client(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    if host["os"] == "rocky":
        command += """ansible-playbook -i "%s," rocky_nfs_client.yaml -u root"""%host["ip"]
    else:
        command += """ansible-playbook -i "%s," ubuntu_nfs_client.yaml -u root"""%host["ip"]

    result = para_connect(command, 30)
    return result

def install_mariadb(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    if host["os"] == "rocky":
        command += """ansible-playbook -i "%s," rocky_mariadb.yaml -u root"""%host["ip"]
    else:
        command += """ansible-playbook -i "%s," ubuntu_mariadb.yaml -u root"""%host["ip"]

    result = para_connect(command, 20)
    return result

def pydio(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    command += """ansible-playbook -i "%s," ubuntu_pydio.yaml -u root"""%host["ip"]

    result = para_connect(command, 30)
    return result

def pydio_db(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    command += """ansible-playbook -i "%s," ubuntu_pydio_db.yaml -u root"""%host["ip"]

    result = para_connect(command, 30)
    return result

def joomla(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    command += """ansible-playbook -i "%s," ubuntu_apache2_joomla.yaml -u root"""%host["ip"]

    result = para_connect(command, 50)
    return result

def joomla_db(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    command += """ansible-playbook -i "%s," ubuntu_apache2_joomla_db.yaml -u root"""%host["ip"]

    result = para_connect(command, 40)
    return result

def wp_setup(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    command += """ansible-playbook -i "%s," ubuntu_apache2_wp_setup.yaml -u root"""%host["ip"]

    result = para_connect(command, 30)
    return result

def wp(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    command += """ansible-playbook -i "%s," ubuntu_apache2_wp.yaml -u root"""%host["ip"]

    result = para_connect(command, 30)
    return result

def wp_db(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    command += """ansible-playbook -i "%s," ubuntu_apache2_wp_db.yaml -u root"""%host["ip"]

    result = para_connect(command, 30)
    return result

def monitorix_server(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    command += """ansible-playbook -i "%s," ubuntu_monitorix_server.yaml -u root"""%host["ip"]

    result = para_connect(command, 30)
    return result
    
def monitorix_client(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    command += """ansible-playbook -i "%s," ubuntu_monitorix_client.yaml -u root"""%host["ip"]

    result = para_connect(command, 25)
    return result
    
def mrtg(host):
    command = ""
    command += "cd /home/smt/ansible\n"
    command += """ansible-playbook -i "%s," ubuntu_mrtg.yaml -u root"""%host["ip"]

    result = para_connect(command, 25)
    return result


#main 시작
#케이스 선택
print("""

  ;;~     ~;;  
,$:,!#   #!,:$,
*.#*#.@ @ @.#*#.*               oooo        oooo        uuuu      uuuu        uuuuu      mmmm                 aaa
=:  .       .  :=               oooo       oooo         uuuu      uuuu       uuuu  mm   mm  mmm              aaaaa   
@:.           .:@               oooo      oooo          uuuu      uuuu      uuu      mmm     mmm            aaa aaa   
:~  **     **  ~:               oooooooooooo            uuuu      uuuu     uuuu      mmm     mmmm          aaa   aaa  
.!             !,               oooooooooo              uuuu      uuuu     uuuu       m      mmmm         aaa     aaa
;    @@ @ @@    ;               oooooooo                uuuu      uuuu     uuuu              mmmm        aaaaaaaaaaaaa
;  -$ @ @ @ $-  ;               oooooooooo               uuu       uuu     mmmm              mmmm       aaa         aaa
;~ $ .@   @. $ ~;               oooo    ooooo             uuuuuuuuuuu      mmmm              mmmm       aaa         aaa 
.! =  , @ ,  = !.               oooo      ooooo             uuuuuuu        mmmm              mmmm      aaa           aaa
 !;;!   @   !;;! 
  !;:$* @ *$:;!                                           곰은.... 사람을.... 찢 어....
   :#!~ : ~!#:   
     ;; ; ;;     
      """)
selcase(acase_list, scase_list) 
print("selcase check")
for p in scase_list:
    print(p)


for m in scase_list :
    #host_list 초기화
    ahost_list = [] # all host list =  특정 파일에서 읽어온 모든 host가 담긴 리스트
    shost_list= [] # selected host list = 사용자가 선택한 host들이 담긴 list
    #호스트 정보 읽고 저장
    gethost(m)
    print("gethost check")
    for a in ahost_list :
        print(a)
    
    #호스트 선택
    selhost(m,ahost_list, shost_list)
    print("selhost check")
    for k in shost_list :
        print(k)    
    
    
    #호스트 한 명씩 꺼내서 명령어 넣어주기
    for i in shost_list :
        #명령어 정보 읽고 저장
        cmd_list = getcmd(m)
        if m in ["router","switch"]:
            cmd_list.append("sh run")
            cmd_list.append("ping")
        #print("getcmd check")
        #for e in cmd_list :
        #    print(e)
        #전체 명령어 보여주고 선택
        selcmd(m,i, cmd_list)
        print("selcmd check")
        for k in i["cmd"] :
            print(k)
        #선택한 명령어 실행 및 결과값 반환 + 가공
        for j in i["cmd"] :
            print("실행 시작")
            #print("j = %s"%(j))
            
            if m == "router" :
                #명령어 그대로 입력하는 경우
                if "sh run" in j:
                    result = net_connect(i,j,5)
                    backup(i["hostname"],m,result)
                elif "set_create_accesslist" in j:
                    result = set_create_accesslist(i)
                    print(result)
                elif "set_gw" in j:
                    result = set_gw(i)
                    print(result)
                elif "set_static_routing" in j:
                    result = set_static_routing(i)
                    print(result)
                elif "set_rip" in j:
                    result = set_rip(i)
                    print(result)
                elif "set_eigrp" in j:
                    result = set_eigrp(i)
                    print(result)
                elif "set_pat" in j :
                    result = set_pat(i)
                    print(result)
                elif "set_intervlan" in j:
                    result = set_intervlan(i)
                    print(result)
                elif "set_dhcp" in j :
                    result = set_dhcp(i)
                    print(result)
                elif "set_glbp" in j:
                    result = set_glbp(i)
                    print(result)
                elif "set_redistribute" in j:
                    result = set_redistribute(i)
                    print(result)
                elif "set_offset" in j:
                    result = set_offset(i)
                    print(result)
                elif "set_distribute" in j:
                    result = set_distribute(i)
                    print(result)
                elif "set_accesslist" in j:
                    result = set_accesslist(i)
                    print(result)
                elif "set_passive" in j:
                    result = set_passive(i)
                    print(result)
                elif "set_manual_summary" in j:
                    result = set_manual_summary(i)
                    print(result)
                elif "set_key_chain" in j:
                    result = set_key_chain(i)
                    print(result)
                elif "ping" in j :
                    result = ping(m,i)
                    print(result)
                    """
                    num = 0
                    for d in result :
                        if "!" in d :
                            num += 1
                    print("router는 전체 16 switch는 전체 ")
                    print(num)
                    """
                    
            elif m == "switch" :
                if "sh run" in j:
                    result = net_connect(i,j,5)
                    backup(i["hostname"],m,result)
                elif "set_vtp" in j :
                    result = set_vtp(i)
                    print(result)
                elif "set_vlan" in j :
                    result = set_vlan(i)
                    print(result)
                elif "set_span" in j :
                    result = set_span(i)
                    print(result)
                elif "ping" in j :
                    result = ping(m,i)
                    #print(result)
                    num = 0
                    for d in result :
                        if "!" in d :
                            num += 1
                    print("router는 전체 30 switch는 전체 33")
                    print(num)
                
            elif m == "server" :
                if "key_exchange" in j:
                    result = key_exchange(i)
                    print(result)
                elif "smb_server" in j :
                    result = smb_server(i)
                    print(result)
                elif "smb_client" in j :
                    result = smb_client(i)
                    print(result)
                elif "dns_server" in j :
                    result = dns_server(i)
                    print(result)
                elif "ftp_login" in j :
                    result = ftp_login(i)
                    print(result)
                elif "ftp_anonymous" in j :
                    result = ftp_anonymous(i)
                    print(result)
                elif "install_php" in j :
                    result = install_php(i)
                    print(result)
                elif "nginx" in j :
                    result = nginx(i)
                    print(result)
                elif "nfs_server" in j :
                    result = nfs_server(i)
                    print(result)
                elif "nfs_client" in j :
                    result = nfs_client(i)
                    print(result)
                elif "install_mariadb" in j :
                    result = install_mariadb(i)
                    print(result)
                elif "pydio_db" in j :
                    result = pydio_db(i)
                    print(result)
                elif "pydio" in j :
                    result = pydio(i)
                    print(result)
                elif "joomla_db" in j :
                    result = joomla_db(i)
                    print(result)
                elif "joomla" in j :
                    result = joomla(i)
                    print(result)
                elif "wp_setup" in j :
                    result = wp_setup(i)
                    print(result)
                elif "wp_db" in j :
                    result = wp_db(i)
                    print(result)
                elif "wp" in j :
                    result = wp(i)
                    print(result)
                elif "monitorix_server" in j :
                    result = monitorix_server(i)
                    print(result)
                elif "monitorix_client" in j :
                    result = monitorix_client(i)
                    print(result)
                elif "mrtg" in j :
                    result = mrtg(i)
                    print(result)
                
            print("실행 끝")

        if m == "switch" :
            scnt += 1

print("all finish!!!!!!!!!!!!!!!!!!!!!!!!!!!!")     
