import re
import requests
from fake_useragent import UserAgent
from lxml import etree
import sys
import getopt
ip=''
port_list=[80, 81, 88, 808, 888, 8000,8008, 8080,8001, 8888, 8020,8009,8081,8082,8083]
addr_url='http://ip.yqie.com/ip.aspx?ip='
ua = UserAgent()

def headers_pool():
    headers = {"User-Agent": ua.random}
    return headers

def A_scan(ip):
    ip = ip.split('.')
    host = []
    for tmpAip in range(1, 256):
        ip[1]=str(tmpAip)
        for tmpBip in range(1, 256):
            ip[-2] = str(tmpBip)
            for tmpCip in range(1, 256):
                ip[-1] = str(tmpCip)
                host.append(".".join(ip))
    return host

def B_scan(ip):
    ip=ip.split('.')
    host=[]
    for tmpBip in range(1,256):
        ip[-2]=str(tmpBip)
        for tmpCip in range(1,256):
            ip[-1]=str(tmpCip)
            host.append(".".join(ip))
    return host

def C_scan(ip):
    ip = ip.split('.')
    host = []
    for tmpCip in range(1, 256):
        ip[-1] = str(tmpCip)
        host.append(".".join(ip))
    return host

def get_addr(ip):
    url = addr_url + ip
    rep = requests.get(url)
    html = etree.HTML(rep.text)
    content = html.xpath('//input[@class="displayno_address"]/@value')[0]
    print ip + "  >>>>>  " + content

def get_rep(ip,port):
    url1 = 'http://' + str(ip) + ':' + str(port)
    url2 = 'https://' + str(ip) + ':' + str(port)
    try:
        rep1 = requests.get(url1,headers=headers_pool(),timeout=3,verify=False)
        if (rep1.status_code==200):
            get_title(url1,rep1)
            get_addr(ip)
    except:
        pass
    try:
        rep2 = requests.get(url2,headers=headers_pool(),timeout=3,verify=False)
        if (rep2.status_code==200):
            get_title(url2,rep2)
            get_addr(ip)
    except:
        pass

def get_title(url,rep):
    title=re.findall(r'<title>(.*?)</title>', rep.text)[0]
    print("[+] "+url+"  >>>>>  "+title)

def check_ip(ip):
    if re.compile(r"^\d+\.\d+\.\d+\.\d+$").match(ip):
        return True
    return False

def scan(ip):
    host=C_scan(ip)
    for url in host:
        for port in port_list:
            get_rep(url,port)


def logo():
    print "hi"

def main(argv):
    if len(sys.argv) <= 1:
        exit("[-]please input ip,you can -h or --help\n")
    try:
        opts, args=getopt.getopt(argv[1:],"hi:t:m:",["help","ip=","thread=","method="])
    except getopt.GetoptError:
        exit("[-]please check your input true argv\n")
    for opt,arg in opts:
        if opt in ['-h','--help']:
            print '''
         [+]this is Jing_scan,To scan internet A,B or C range
            you can input argvs:-h --help,-i --ip,-t --thread,-m --method
            (Default scan C)
            for example:
            python2 Scan.py -i 127.0.0.1 -t 10 -m C
            '''
            sys.exit()
        elif opt in ['-i','--ip']:
            get_ip=arg
        elif opt in ['-t','--thread']:
            thread=arg
        elif opt in ['-m','--method']:
            method=arg
        else:
            exit("Error: invalid parameters :(")
    logo()
    if check_ip(get_ip):
        if method=="A":
            A_scan(ip)
        elif method=="B":
           B_scan(ip)
        else:
            C_scan(ip)
    else:
        exit("please input true ip")

if __name__=='__main__':
    main(sys.argv)