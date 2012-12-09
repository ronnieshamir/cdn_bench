#!/usr/bin/python

import re, commands, dns.resolver, numpy, sys

def ping(ip):
    ping = commands.getstatusoutput("ping -c 1 -W 1200 -q " + ip + "|grep min")[1]
    match = re.search(r'= (\d+\.\d+)/', ping)
    time = float(match.group(1)) if match else -1
    return time

def nameserver_speed(nameserver, hostname):
    resolver = dns.resolver.Resolver()
    resolver.lifetime = 10.0
    resolver.nameservers = [nameserver]
    try:
        host_ip = resolver.query(hostname, 'A')[0].address
        time = ping(host_ip)
    except:
        time = -1
    return time

def main():
    nameservers = (
                   ('Primary Local Distributel', '209.195.95.95'), ('Secondary Local Distributel', '209.197.128.2'),
                   ('Primary National Distributel', '206.80.254.4'), ('Secondary National Distributel', '206.80.254.68'),
                   ('Google Public DNS', '8.8.8.8'),
                   ('Primary Norton ConnectSafe', '198.153.192.50'),
                   ('Secondary Norton ConnectSafe', '198.153.194.50'),
                   ('OpenDNS', '208.67.222.222'),
                   ('Primary Outremer', '217.175.160.11'), ('Secondary Outremer', '217.175.160.12'),
                   ('Numericable', '89.2.0.1')
                   )
    hostnames = (
                 'static.ak.fbcdn.net',         #facebook
                 'twimg0-a.akamaihd.net',       #twitter
                 's0.2mdn.net',                 #slashdot
                 'www.redditstatic.com',        #reddit
                 'gs1.wac.edgecastcdn.net',     #tumblr
                 'ecx.images-amazon.com',       #amazon
                 'i.s-microsoft.com',           #microsoft
                 'l.yimg.com',                  #yahoo
                 'o.scdn.co',                   #spotify
                 'static.bbci.co.uk',           #bbc
                 'upload.wikimedia.org',        #wikipedia
                 'a.tgcdn.net'                  #thinkgeek
                 )
    for nameserver in nameservers:
        time = ping(nameserver[1])
        if time == -1:
            sys.stdout.write("Name server " + nameserver[0] + " unreachable\n")
        else:
            sys.stdout.write("{:>30} -- Nameserver speed: {:6.2f} ms -- Avg. host speed: ".format(nameserver[0], time))
            times = []
            unreachables = []
            for hostname in hostnames:
                time = nameserver_speed(nameserver[1], hostname)
                if time == -1:
                    unreachables.append(hostname)
                else:
                    times.append(time)
            if times:
                sys.stdout.write("{:6.2f} ms\n".format(numpy.mean(times)))
            else:
                sys.stdout.write("Timed out\n")
            for unreachable in unreachables:
                sys.stdout.write(" " * 24 + "* " + unreachable + " timed out with " + nameserver[0] + "\n")

if __name__ == '__main__':
    main()