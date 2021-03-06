### AUTO GENERATED CONFIG SAMPLE IS AS BELOW

#### DEVICE 1
```
interfaces {

    ge-0/0/12 {
        unit 0 {
	
            family inet {
                address 192.168.210.97/30;
            }
        }
    }

    ge-0/0/8 {
        unit 0 {
	
            family inet {
                address 192.168.210.113/30;
            }
        }
    }

    ge-0/0/10 {
        unit 0 {
	
            family inet {
                address 192.168.210.101/30;
            }
        }
    }

}
routing-options {
    autonomous-system 111;
    router-id 10.0.0.1;
}
protocols {
    bgp {
        import import_bgp;
        export export_bgp;
        group CLOS {
            type external;
            multipath multiple-as;
	
	    neighbor 192.168.210.98 {
                peer-as 112;
            }
	
	    neighbor 192.168.210.114 {
                peer-as 113;
            }
	
	    neighbor 192.168.210.102 {
                peer-as 114;
            }
	
        }
    }
}
policy-options {
    policy-statement import_bgp {
        term term1 {
            from {
	
                route-filter 192.168.210.98/32 exact;
	
                route-filter 192.168.210.114/32 exact;
	
                route-filter 192.168.210.102/32 exact;
	
            }
            then accept;
        }
    }
    policy-statement export_bgp {
        term term1 {
            then accept;
        }
    }
}
```
```
Locking the configuration
Loading configuration changes
Committing the configuration
```
#### DEVICE 2:
```
interfaces {

    ge-0/0/12 {
        unit 0 {
	
            family inet {
                address 192.168.210.98/30;
            }
        }
    }

    ge-0/0/8 {
        unit 0 {
	
            family inet {
                address 192.168.210.241/30;
            }
        }
    }

    ge-0/0/10 {
        unit 0 {
	
            family inet {
                address 192.168.210.61/30;
            }
        }
    }

}
routing-options {
    autonomous-system 112;
    router-id 10.0.0.2;
}
protocols {
    bgp {
        import import_bgp;
        export export_bgp;
        group CLOS {
            type external;
            multipath multiple-as;
	
	    neighbor 192.168.210.97 {
                peer-as 111;
            }
	
	    neighbor 192.168.210.242 {
                peer-as 113;
            }
	
	    neighbor 192.168.210.62 {
                peer-as 114;
            }
	
        }
    }
}
policy-options {
    policy-statement import_bgp {
        term term1 {
            from {
	
                route-filter 192.168.210.97/32 exact;
	
                route-filter 192.168.210.242/32 exact;
	
                route-filter 192.168.210.62/32 exact;
	
            }
            then accept;
        }
    }
    policy-statement export_bgp {
        term term1 {
            then accept;
        }
    }
}
```
```
Locking the configuration
Loading configuration changes
Committing the configuration
```
#### DEVICE 3:
```
interfaces {

    ge-0/0/10 {
        unit 0 {
	
            family inet {
                address 192.168.210.242/30;
            }
        }
    }

    ge-0/0/8 {
        unit 0 {
	
            family inet {
                address 192.168.210.114/30;
            }
        }
    }

}
routing-options {
    autonomous-system 113;
    router-id 10.0.0.3;
}
protocols {
    bgp {
        import import_bgp;
        export export_bgp;
        group CLOS {
            type external;
            multipath multiple-as;
	
	    neighbor 192.168.210.241 {
                peer-as 112;
            }
	
	    neighbor 192.168.210.113 {
                peer-as 111;
            }
	
        }
    }
}
policy-options {
    policy-statement import_bgp {
        term term1 {
            from {
	
                route-filter 192.168.210.241/32 exact;
	
                route-filter 192.168.210.113/32 exact;
	
            }
            then accept;
        }
    }
    policy-statement export_bgp {
        term term1 {
            then accept;
        }
    }
}
```
```
Locking the configuration
Loading configuration changes
Committing the configuration
```
#### DEVICE 4
```
interfaces {

    ge-0/0/10 {
        unit 0 {
	
            family inet {
                address 192.168.210.62/30;
            }
        }
    }

    ge-0/0/8 {
        unit 0 {
	
            family inet {
                address 192.168.210.102/30;
            }
        }
    }

}
routing-options {
    autonomous-system 114;
    router-id 10.0.0.4;
}
protocols {
    bgp {
        import import_bgp;
        export export_bgp;
        group CLOS {
            type external;
            multipath multiple-as;
	
	    neighbor 192.168.210.61 {
                peer-as 112;
            }
	
	    neighbor 192.168.210.101 {
                peer-as 111;
            }
	
        }
    }
}
policy-options {
    policy-statement import_bgp {
        term term1 {
            from {
	
                route-filter 192.168.210.61/32 exact;
	
                route-filter 192.168.210.101/32 exact;
	
            }
            then accept;
        }
    }
    policy-statement export_bgp {
        term term1 {
            then accept;
        }
    }
}
```
