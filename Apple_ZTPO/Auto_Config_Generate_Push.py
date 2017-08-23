from helpers import Helpers
import random
import MySQLdb
from lxml import etree
from jnpr.junos.utils.config import Config
import os
import jinja2
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError
from ipcalculator import IPCalculator
import math

helpers = Helpers()

'''
fetch the list of devices and its details from the DB
'''
db = MySQLdb.connect(host="localhost",user="root",passwd="salt123",db="AppleDB")
cursor = db.cursor (MySQLdb.cursors.DictCursor)
query = 'select * from devices'
cursor.execute(query)
result = cursor.fetchall()
hosts_dict = {}
link_layer_map = {} 
link_layer_list = list()
'''
for each device build the required config CONFIG VARIABLES
'''
for row in result:
    '''
    CONNECT TO THE DEVICE USING PYEZ
    '''
    ip_mask = row["management_ip"]
    hostname = row["hostname"]
    ip = ip_mask.split("/")
    host = ip[0]

    dev = helpers.device_connect(host)
    dev.open()

    '''
    FETCH LINK LAYER INFORMATION USING RPC LLDP
    '''
    cli_lldp = dev.rpc.get_lldp_neighbors_information()
    interfaces = list() 
    remote_connections = list()
    ints_list = list()
    bgp_list = list()
    interfaces_dict = {}
    for lldp in cli_lldp.findall("lldp-neighbor-information"):
        '''
        LINK LAYER CONNECTIVITY INFORMATION APPENDED
        '''
	local_port = lldp.findtext("lldp-local-interface") 
	if local_port is None:
	    local_port = lldp.findtext("lldp-local-port-id")
	    local_port = local_port
	else:
	    local_port = local_port.split(".")
	    local_port = local_port[0]

	interfaces.append(local_port)
	remote_chassis = lldp.findtext("lldp-remote-chassis-id")
	remote_system = lldp.findtext("lldp-remote-system-name")
	remote_connections.append(remote_system)
	remote_port = lldp.findtext("lldp-remote-port-description")
        remote_port = remote_port.split(".")
        remote_port = remote_port[0]
	link_layer_list.append({'local_system': hostname, 'local_port': local_port, 'local_ip': 'None', 'remote_ip': 'None', 'remote_system': remote_system, 'remote_port': remote_port, 'broadcast': 'None'}) 

        '''
        INTERFACES INFORMATION FETCHED 
	IP IS NONE. WILL BE ASSIGNED LATER
        '''
	description = "to_" + remote_system
	local_port = local_port.strip()
	description = description.strip()
	ints_list.append({'physical_interface': local_port, 'description': description, 'ip_address': "None" })

    '''
    BGP INFORMATION FETCHED 
    IP IS NONE. WILL BE ASSIGNED LATER
    '''
    for remote_connection in remote_connections:
        query = 'select * from devices where hostname="' + remote_connection + '"'
        cursor.execute(query)
        result2 = cursor.fetchall()
        for row2 in result2:
	    remote_as = row2["bgpasn"]
	    remote_description = row2["hostname"]
	bgp_list.append({ 'remote_as': remote_as, 'remote_peer': 'None', 'remote_description' : remote_description})

    '''
    INTERFACES,BGP,BGP_ROUTER_ID,BGPASN,ROUTER_FILTER
    INFORMATION APPENDED
    IPs ARE NONE. WILL BE ASSIGNED LATER
    '''
    interfaces_dict.update({hostname: {'interfaces': ints_list,'bgp_router_id': row["bgp_router_id"],'bgpasn': row["bgpasn"],'bgp': bgp_list,'route_filter': []}})

    hosts_dict.update(interfaces_dict)
    dev.close()

'''
LINK LAYER MAP:
LINK INFO: LOCAL(PORT,IP,HOST) & REMOTE(PORT,IP,HOST)

REMOVE DUPLICATES: DUPLICATES EXIST BCOS SAME LINK INFO FOUND IN BOTH LOCAL AND REMOTE HOST
'''
link_layer_map.update({'link_layer': link_layer_list})
links = link_layer_map["link_layer"]
for link in links:
    for rlink in links:
        if link["local_system"]+link["local_port"] == rlink["remote_system"]+rlink["remote_port"]:
            if link["remote_system"]+link["remote_port"] == rlink["local_system"]+rlink["local_port"]:
		links.remove(rlink)

'''
GENERATE IPS FOR CONNECTED INTERFACES 
BASED ON:
IP START & IP END, NETMASK, ALREADY USED IP
'''
for link in links:
    query = 'select * from ips where subnet_num="1"'
    cursor.execute(query)

    result3 = cursor.fetchall()
    for row3 in result3:
        ip_start = row3["ip_start"]
        start = int(ip_start.split(".")[-1])

        ip_end = row3["ip_end"]
        end = int(ip_end.split(".")[-1])

        netmask = row3["netmask"]
        netmask = netmask.replace("/","")
        num_addresses = int(math.pow(2,(32 - int(netmask))))

        ip_used = row3["ip_used"]
	if not ip_used:
	    ip_used = []
        else:
	    ip_used = ip_used.split(",")
            ip_used = map(int, ip_used)

    ip_range = range(start,end,num_addresses)
    ip_avail = [x for x in ip_range if x not in ip_used] 
    ip_random = random.choice(ip_avail)
    ip_used.append(ip_random)
    ip_used = ','.join(map(str, ip_used))
    query = 'update ips set ip_used="' + ip_used + '" where subnet_num="1"'
    cursor.execute(query)
    db.commit()

    ip1 = ip_start.rsplit('.', 1)
    ip2 = start + ip_random
    ip = ip1[0] + "." + str(ip2) + "/30"

    ip = IPCalculator(ip)
    ip_detail = ip.__repr__()
    hostrange = ip_detail["hostrange"]
    hostrange = hostrange.split("-")
    broadcast = ip_detail["broadcast"]
    cidr = ip_detail["cidr"]

    link['local_ip'] = hostrange[0]+"/"+cidr
    link['remote_ip'] = hostrange[1]+"/"+cidr
    link['broadcast'] = broadcast+"/"+cidr

'''
ASSIGN THE GENERATED IPs TO THE INTERFACES CONFIG
'''
for key, vals in hosts_dict.iteritems():
    hostname = key
    for key,vals in vals.iteritems():
	if key == "interfaces":
	    for val in vals:
	        interface = val["physical_interface"]
		for link in links:
		    if hostname == link["local_system"] and interface == link["local_port"]:
			val["ip_address"] = link["local_ip"]
		    elif hostname == link["remote_system"] and interface == link["remote_port"]:
			val["ip_address"] = link["remote_ip"]

'''
ASSIGN THE GENERATED IPs TO THE "BGP CONFIG,ROUTE FILTERS CONFIG" 
'''
for key,vals in hosts_dict.iteritems():
    hostname = key
    filter_list = list()
    for key,vals in vals.iteritems():
	if key == "bgp":
	    for val in vals:
		bgp_remote_host = val["remote_description"]
		for link in links:
		    if hostname == link["local_system"] and bgp_remote_host == link["remote_system"]:
            		val["remote_peer"] = link["remote_ip"].replace("/30","")
			filter_list.append(val["remote_peer"]+"/32")
		    elif hostname == link["remote_system"] and bgp_remote_host == link["local_system"]:
	    		val["remote_peer"] = link["local_ip"].replace("/30","")
			filter_list.append(val["remote_peer"]+"/32")
	if key == "route_filter":
	    for filter in filter_list:
	        vals.append(filter)

'''
FINAL CONFIG VARIABLES DICTIONARY COMPLETED
## HOSTS_DICT ##
'''
print hosts_dict

'''
CONFIG TEMPLATE
'''
template_filename = "EX_template2.conf"
complete_path = os.path.join(os.getcwd(), 'Config')
template_file = complete_path + "/" + template_filename

templateLoader = jinja2.FileSystemLoader(searchpath="/")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template(template_file)

'''
CONNECT TO THE DEVICE PUSH THE AUTO GENERATED CONFIG
''' 
for row in result:
    ip_mask = row["management_ip"]
    hostname = row["hostname"]
    ip = ip_mask.split("/")
    host = ip[0]

    dev = helpers.device_connect(host)
    dev.open()

    '''
    RENDER CONFIG BASED ON VARIABLES AND TEMPLATE
    '''
    device_vars = hosts_dict[hostname]
    outputText = template.render(device_vars)
    print outputText

    config = Config(dev)

    '''
    LOCK DEVICE CONFIG
    '''
    print ("Locking the configuration")
    try:
        config.lock()
    except LockError as err:
        print ("Unable to lock configuration: {0}".format(err))

    '''
    LOAD DEVICE CONFIG
    '''
    print ("Loading configuration changes")
    try:
	config.load(template_path=template_file, template_vars=device_vars, merge=True)
    except (ConfigLoadError, Exception) as err:
        print ("Unable to load configuration changes: {0}".format(err))

    '''
    COMMIT DEVICE CONFIG
    '''
    print ("Committing the configuration")
    try:
        config.commit(comment='Loaded by example.')
    except CommitError as err:
        print ("Unable to commit configuration: {0}".format(err))

    '''
    GENERATE THE CONFIG STATUS & SEND IT TO THE GUI 
    '''

