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

    def compare_mac(self, sample_mac, host_mac):
        """
        For SRX, bootp ge-0/0/0 => ge-0/0/0.mac = chassis.mac
        For  EX, bootp ge-0/0/0 => vlan.mac = chassis.mac + 1
        """
        sample_mac_int = int(sample_mac.replace(':', ''), 16)
        host_mac_int = int(target_mac.replace(':', ''), 16)
        if sample_mac_int == host_mac_int:
            return True
        else:
            return False

    def fetch_customer_requirements(self,sno):
	"""
	Fetch the customer requirements(serialnumber,image,config) from the MySQL DataBase
	"""
        db = MySQLdb.connect(host="localhost",user="root",passwd="salt123",db="AppleDB")
        cursor = db.cursor()
	query = 'select * from devices where sno="' + sno + '"'
        cursor.execute(query) 
        for row in cursor.fetchall():
            sno_db = row[0]
            version_db = row[1]
            config_db = row[2]
	
	    return sno_db,version_db,config_db 

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
            dev = self.device_conn(host_ip)
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

    def config_composer(self, model, hostname, junos_on_box_version):
        """
         Using Yaml and Jinja2 generate dynamic templates
        """
        if "QFX" in model:
            template_filename = "QFX_template.j2"
            network_parameter_filename = "QFX_networkParameters.yaml"
        elif "EX" in model:
            template_filename = "EX_template.j2"
            network_parameter_filename = "EX_networkParameters.yaml"

        complete_path = os.path.join(os.getcwd(), 'Config')
        ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(complete_path))
        template = ENV.get_template(template_filename)

        with open(complete_path + "/" + network_parameter_filename) as yamlfile:
            dict = yaml.load(yamlfile)  # yaml file is loaded as a dictionary with key value pairs
        addition = {"hostname": hostname, "version": junos_on_box_version}
        dict.update(addition)

        content = template.render(dict)

        target = open("Config_History/" + hostname + ".set", 'w')
        target.write(content)
        target.close()

