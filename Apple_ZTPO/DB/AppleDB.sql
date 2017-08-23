-- MySQL dump 10.13  Distrib 5.5.57, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: AppleDB
-- ------------------------------------------------------
-- Server version	5.5.57-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `sno` varchar(20) NOT NULL,
  `hostname` varchar(30) DEFAULT NULL,
  `version` varchar(20) DEFAULT NULL,
  `mac` varchar(30) DEFAULT NULL,
  `rack` varchar(30) DEFAULT NULL,
  `bgp_router_id` varchar(50) DEFAULT NULL,
  `bgpasn` varchar(50) DEFAULT NULL,
  `root_password` varchar(50) DEFAULT NULL,
  `interfaces` varchar(500) DEFAULT NULL,
  `management_ip` varchar(30) DEFAULT NULL,
  `user` varchar(30) DEFAULT NULL,
  `user_password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
INSERT INTO `devices` VALUES ('P3744','QFX5100-1','15.1R6.7','78:fe:3d:5b:c1:0e',NULL,'10.0.0.1','111','$1$kuEKtOY3$BRJ3vJZ7QXp9iltyQUqLb/','\'ge-0/0/8\', \'ge-0/0/10\', \'ge-0/0/12\'','10.86.2.140/24','admin','$1$kuEKtOY3$BRJ3vJZ7QXp9iltyQUqLb/');
INSERT INTO `devices` VALUES ('P4039','QFX5100-2','15.1R6.7','78:fe:3d:5a:b8:fe',NULL,'10.0.0.2','112','$1$kuEKtOY3$BRJ3vJZ7QXp9iltyQUqLb/','\'ge-0/0/8\', \'ge-0/0/10\', \'ge-0/0/12\'','10.86.2.141/24','admin','$1$kuEKtOY3$BRJ3vJZ7QXp9iltyQUqLb/');
INSERT INTO `devices` VALUES ('P4765','QFX5100-3','15.1R6.7','ac:4b:c8:5f:fb:6c',NULL,'10.0.0.3','113','$1$kuEKtOY3$BRJ3vJZ7QXp9iltyQUqLb/','\'ge-0/0/8\', \'ge-0/0/10\', \'ge-0/0/12\', \'ge-0/0/14\', \'ge-0/0/16\'','10.86.2.142/24','admin','$1$kuEKtOY3$BRJ3vJZ7QXp9iltyQUqLb/');
INSERT INTO `devices` VALUES ('P4792','QFX5100-4','15.1R6.7','ac:4b:c8:61:44:10',NULL,'10.0.0.4','114','$1$kuEKtOY3$BRJ3vJZ7QXp9iltyQUqLb/','\'ge-0/0/8\', \'ge-0/0/10\', \'ge-0/0/12\', \'ge-0/0/14\', \'ge-0/0/16\'','10.86.2.143/24','admin','$1$kuEKtOY3$BRJ3vJZ7QXp9iltyQUqLb/');
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ips`
--

DROP TABLE IF EXISTS `ips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ips` (
  `subnet_num` varchar(20) NOT NULL,
  `ip_start` varchar(30) DEFAULT NULL,
  `ip_end` varchar(30) DEFAULT NULL,
  `netmask` varchar(10) DEFAULT NULL,
  `ip_used` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`subnet_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ips`
--

LOCK TABLES `ips` WRITE;
/*!40000 ALTER TABLE `ips` DISABLE KEYS */;
INSERT INTO `ips` VALUES ('1','192.168.210.0','192.168.210.251','/30','96,112,100,240,60');
/*!40000 ALTER TABLE `ips` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-23 15:30:48
