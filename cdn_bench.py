#!/usr/bin/python

import commands, numpy, sys

def ping(ip):
    try:
        time = float(commands.getstatusoutput(r"ping -c 1 -W 1200 -q " + ip + r"| sed -n 's_.*= .*/\([0-9][0-9]*\.[0-9]*\)/.*/.*_\1_p'")[1])
    except:
        time = -1
    return time

def speed(nameserver, hostname):
    try:
        host_ip =  commands.getstatusoutput(r"host -v -c IN " + hostname + " " + nameserver + r"|sed -n 's_.*IN.*[[:space:]]\([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\)_\1_p'|head -1")[1]
        dns_time = float(commands.getstatusoutput(r"host -v -c IN " + hostname + " " + nameserver + r"|sed -n 's/.* \([0-9][0-9]*\) ms/\1/p'")[1])
        host_time = ping(host_ip)
    except:
        dns_time, host_time = -1, -1
    return dns_time, host_time

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
            dns_times = []
            host_times = []
            unreachables = []
            for hostname in hostnames:
                dns_time, host_time = speed(nameserver[1], hostname)
                if dns_time == -1 or host_time == -1:
                    unreachables.append(hostname)
                else:
                    dns_times.append(dns_time)
                    host_times.append(host_time)
            if dns_times and host_times:
                sys.stdout.write("{:>30} -- Nameserver speed: {:6.2f} ms -- Avg. host speed: {:6.2f} ms\n".format(nameserver[0], numpy.mean(dns_times), numpy.mean(host_times)))
            else:
                sys.stdout.write("Timed out\n")
            for unreachable in unreachables:
                sys.stdout.write(" " * 24 + "* " + unreachable + " timed out with " + nameserver[0] + "\n")

if __name__ == '__main__':
    main()