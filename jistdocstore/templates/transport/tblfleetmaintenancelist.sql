-- MySQL dump 10.13  Distrib 5.1.63, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: jistcontracts
-- ------------------------------------------------------
-- Server version	5.1.63-0ubuntu0.11.10.1

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
-- Table structure for table `tblfleetmaintenancelist`
--

DROP TABLE IF EXISTS `tblfleetmaintenancelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblfleetmaintenancelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fleetid` int(11) DEFAULT NULL,
  `reqid` int(11) DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `supplier` varchar(80) DEFAULT NULL,
  `odometer` varchar(40) DEFAULT NULL,
  `work_description` varchar(255) DEFAULT NULL,
  `next_service` varchar(40) DEFAULT NULL,
  `amount` varchar(40) DEFAULT NULL,
  `person` varchar(80) DEFAULT NULL,
  `useridnew` int(11) NOT NULL,
  `useridedited` int(11) NOT NULL,
  `dateedited` datetime DEFAULT NULL,
  `dateadded` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblfleetmaintenancelist`
--

LOCK TABLES `tblfleetmaintenancelist` WRITE;
/*!40000 ALTER TABLE `tblfleetmaintenancelist` DISABLE KEYS */;
INSERT INTO `tblfleetmaintenancelist` VALUES (1,NULL,0,'2011-12-03','Somewhere','89045','Some Work was done','45666','5623.90','',2,2,'2011-12-03 00:00:00','2011-12-03 00:00:00'),(2,NULL,0,'2011-12-03','Somewhere2','89045','Some Work was done','45666','5623.90','me',2,2,'2011-12-03 00:00:00','2011-12-03 00:00:00'),(3,3,0,'2011-12-03','Somewhere2','9001','Some Work2','48785','45222','meto',2,2,'2011-12-03 00:00:00','2011-12-03 00:00:00'),(4,3,0,'2011-12-03','Toyota ','455666','Some More work done','8999','9009.32','',2,2,'2011-12-03 00:00:00','2011-12-03 00:00:00');
/*!40000 ALTER TABLE `tblfleetmaintenancelist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-01-08  9:19:27
