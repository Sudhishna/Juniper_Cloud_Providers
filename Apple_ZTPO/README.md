# Apple ZTPO (Zero Touch Provisioning & Operation)

### Environment Setup:
1.	Spin 2 Virtual Machines (Ubuntu) 
2.	Setup one of the VMs as a DHCP Server
3.	Setup the other one as TFTP Server

### Planned Workflow:
1.	The new devices are cabled. (Device Status is OFF)
2.	In the GUI: User chooses the number of Spines and Leaves
	 and the below topology is generated
	![Alt text](/Apple_ZTPO/img/InitialTopology.jpg "Initial Topology") 

3.	In the topology that appears, the user will enter the Serial Number of the Spines and Leaves by clicking on the boxes.

	![Alt text](/Apple_ZTPO/img/SerialNumberAssigned.jpg "Serial Number Assigned")

4.	The User can now Boot/ON the devices.
5.	### ZTPO Starts:
	- DHCP Server assigns the IP address
	- TFTP Server pushes CONFIG (netconf and login credentials)
	- Python Script runs as CRON. 
	  - Keeps tracking the dhcp leases file and triggers Action.
	- Action would be:
	  - fetch the Serial Number of the device
	  - match the Serial Number against the Database and fetch the CONFIG and IMG file. 
	  - Upgrade to the new IMG and push CONFIG
6.	The Entire ZTPO Process communicates with the GUI to give live updates. And the GUI will transition as shown below.
	![Alt text](/Apple_ZTPO/img/GUILiveProgres.jpg "GUI Live Progress")
 
#### NOTE: The images represent the GUI that will be built. Once the GUI is built, it will be replaced by the actual snapshots.
