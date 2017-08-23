import re
import os
import time
import json
import yaml
import jinja2
import pprint
import hashlib
import logging
import difflib
import MySQLdb
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos import exception
from jnpr.junos.utils.sw import SW
from jnpr.junos.utils.config import Config

class Helpers:
    """
    Collection of helper functions that will be used for 
    Apple ZTPO
    """

    __known_hosts = []
    __new_hosts = []

    def lease_read(self, path):
        """
        Initial read from 'dhcpd.leases' file
        Get {ip, mac}
        """
        ip_pattern = r"(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"
        mac_pattern = r"(?:(?:[0-9a-f][0-9a-f]:){5}(?:[0-9a-f][0-9a-f]))"

        leases_file = open('/var/lib/dhcp/dhcpd.leases', 'r')
	content =leases_file.read() 

        hosts = re.findall( ip_pattern, content )
	macs = re.findall( mac_pattern, content )

	host_mac = {}
        for i in range(0, len(hosts)):
	    host_mac[macs[i]] = hosts[i]

        return host_mac

    def fetch_customer_requirements(self,sno):
	"""
	Fetch the customer requirements(serialnumber,image,config) from the MySQL DataBase
	"""
        db = MySQLdb.connect(host="localhost",user="root",passwd="salt123",db="AppleDB")
        cursor = db.cursor (MySQLdb.cursors.DictCursor)
        query = 'select * from devices where sno="' + sno + '"'
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            for key,value in row.iteritems():
                if key == "sno":
                    sno_db = value
            	if key == "version":
		    version_db = value
	
	    return sno_db,version_db 

    def device_connect(self, host_ip):
	"""
	Connect to the device to perform tasks in it
	"""
        user = "root"
        password = "salt123"
        return Device(host=host_ip, user=user, password=password)

    def version_analyze(self, version):
        holder = 0
        result = []
        counter = 0
        for x in version:
            counter += 1
            if x.isdigit():
                holder = holder * 10 + int(x)
                if counter == len(version):
                    result.append(holder)
            else:
                if holder != 0:
                    result.append(holder)
                    holder = 0
                if x.isalpha():
                    result.append(str(x))
                else:
                    continue
        return result

    def junos_version_compare(self, host_ver, req_ver):
        host_version = self.version_analyze(host_ver)
        req_version = self.version_analyze(req_ver)
        print host_version,req_version

        count = min(len(host_version), len(req_version))

        for x in range(count):
            if host_version[x] != req_version[x]:
                if host_version[x] > req_version[x]:
                    print("current one has newer version @" + str(x+1) + " digit")
                    return 1
                elif host_version[x] < req_version[x]:
                    print("current one has older version")
                    return -1

        # if every compared digit is the same it indicates
	# they have same version  
        return 0

    def junos_img_check(self, model, version):
        """ read file names under local stored junos,
            extract label and compare them with junos version
            return local filename if we have;
            return False if we don't
        """
        if "EX" in model:
            match = re.match(r"([a-z]+)([0-9]+)", model, re.I)
            filename_part = "jinstall-ex-" + match.groups()[1] + "-" + version
        elif "QFX" in model:
            filename_part = "junos-qfx-" + version

        print("Local junos directory check for version " + version + " ...")
        for filename in os.listdir("Junos/"):
            if filename.endswith(".tgz") and (filename_part in filename):
                print("Found proper image ...")
                return filename
        # if not found, return False
        return False

    def junos_auto_install(self,host_ip, path, device):
        """
        Use PyEz to secure install new junos version
        to remote host
        """

        sw = SW(device)
        path = os.path.join(os.getcwd(),path)
        print path,type(path)
        try:
            ok = sw.install(package=path, progress=install_progress)
        except Exception as err:
            print("Install error")
            raise err
        if ok is True:
            print("\nSoftware installation succeeded")
        else:
            print(ok)
            time.sleep(30)
        try:
            rsp = sw.reboot()
            print(rsp)
        except exception.ConnectClosedError:
            print("About to loose connection ..")
        finally:
            print("Please wait for the box to wake-up!")
            time.sleep(120)
            dev = self.device_connect(host_ip)
            feeds = dev.probe(10)
            while not feeds:
                feeds = dev.probe(20)
                #print("probing in 20 seconds interval")
            print("\n\nConnecting to box now ...")
            dev.open()
            print("Connected")
            print("New version:")
            self.print_base_info(dev)
            return dev

    def load_config(self, model, sno, device):
        """
        Using Yaml and Jinja2 generate dynamic templates
        """
        dict = {}
        conn = MySQLdb.connect(host="localhost",user="root",passwd="salt123",db="AppleDB")
        cursor = conn.cursor (MySQLdb.cursors.DictCursor)
        query = 'select * from devices where sno="' + sno + '"'
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            for key,value in row.iteritems():
		if key == "interfaces":
		    ints_list = []
		    ints = value.split(",") 
		    for int in ints:
			int = int.replace("'", "")
			int = int.replace(" ", "")
			phy_ints = {"physical_interface": int}
			ints_list.append(phy_ints)
		    dict.update({key: ints_list})
		else:
                    dict.update({key: value})
	print dict

        if "QFX" in model:
            template_filename = "QFX_template.conf"
        elif "EX" in model:
            template_filename = "EX_template.conf"
        complete_path = os.path.join(os.getcwd(), 'Config')
	template = complete_path + "/" + template_filename

        config = Config(device)
        config.load(template_path=template, template_vars=dict, overwrite=True)
        config.commit()

        return dict

    def ipRange(self, start_ip, end_ip):
	start = list(map(int, start_ip.split(".")))
	end = list(map(int, end_ip.split(".")))
	temp = start
	ip_range = []

	ip_range.append(start_ip)
	while temp != end:
	    start[3] += 1
	    for i in (3, 2, 1):
	        if temp[i] == 256:
	            temp[i] = 0
	            temp[i-1] += 1
	    ip_range.append(".".join(map(str, temp)))

	return ip_range
