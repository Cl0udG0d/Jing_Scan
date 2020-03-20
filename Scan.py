import re
import requests
from fake_useragent import UserAgent
from lxml import etree
port_list=[80, 81, 88, 808, 888, 8000,8008, 8080,8001, 8888, 8020,8009,8081,8082,8083]
addr_url='http://ip.yqie.com/ip.aspx?ip='
ua = UserAgent()

def headers_pool():
    headers = {"User-Agent": ua.random}
    return headers

# def A_scan(ip):
# def B_scan(ip):
def C_scan(ip):
    ip = ip.split('.')
    host = []
    for tmpIP in range(1, 256):
        ip[-1] = str(tmpIP)
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
    if(check_ip(ip)):
        host=C_scan(ip)
        for url in host:
            for port in port_list:
                get_rep(url,port)
    else:
        print("ip error!!")

def start():
    print("hello world!")
    print("now please waiting ....")

def main():
    start()
    ip='47.94.132.67'
    scan(ip)

if __name__=='__main__':
    main()