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
-- Table structure for table `tblfleetlist`
--

DROP TABLE IF EXISTS `tblfleetlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblfleetlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vehicle_description` varchar(80) DEFAULT NULL,
  `registration_number` varchar(80) DEFAULT NULL,
  `year_model` varchar(80) DEFAULT NULL,
  `date_acquired` date DEFAULT NULL,
  `vin_number` varchar(80) DEFAULT NULL,
  `engine_number` varchar(80) DEFAULT NULL,
  `n_r_number` varchar(80) DEFAULT NULL,
  `tare` varchar(80) DEFAULT NULL,
  `fuel_type` varchar(80) DEFAULT NULL,
  `tank_capacity` varchar(80) DEFAULT NULL,
  `fuel_card_number` varchar(80) DEFAULT NULL,
  `fuel_card_expiry_date` date DEFAULT NULL,
  `ext_colour` varchar(80) DEFAULT NULL,
  `service_center` varchar(80) DEFAULT NULL,
  `service_center_tel_no` varchar(80) DEFAULT NULL,
  `driver` varchar(80) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `useridnew` int(11) NOT NULL,
  `dateadded` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=47 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblfleetlist`
--

LOCK TABLES `tblfleetlist` WRITE;
/*!40000 ALTER TABLE `tblfleetlist` DISABLE KEYS */;
INSERT INTO `tblfleetlist` VALUES (1,'Kia Workhorse K2700','CF 86933','2005','2005-11-01','KNCSE911267098123','J2430138','1001055DL8TJ','1530','Diesel','60','708283 15 0163 1653','2011-11-28','White','KIA Tygerberg','021-949 2558','1',0,5,'2011-11-28 00:00:00'),(2,'Kia Workhorse K2700','CF100073','2006','2006-06-01','KNCSE911267148410','J2445243','1001055CKKNK','1530','Diesel','60','708283 15 0227 4057','2011-11-28','White','KIA Tygerberg','021-949 2558','1',0,5,'2011-11-28 00:00:00'),(3,'Kia Workhorse K2700','CF 165801','2010','2010-09-01','KNCSGX71LB7503545','J2556501','','1530','Diesel','60','708283 15 0245 0384','2011-11-28','White','KIA Tygerberg','021-949 2558','33',1,5,'2011-11-28 00:00:00'),(4,'Kia Workhorse K2700','CF 167302','2010','2010-11-01','KNCSHX71LB7498286','J2553922','','1530','Diesel','60','708283 15 0245 0392','2011-11-28','White','KIA Tygerberg','021-949 2558','4',1,5,'2011-11-28 00:00:00'),(5,'Kia Workhorse K2700','CF 167305','2010','2010-11-01','KNCSHX71LB7498287','J2553928','','1530','Diesel','60','708283 15 0245 0368','2011-11-28','White','KIA Tygerberg','021-949 2558','1',1,5,'2011-11-28 00:00:00'),(6,'Kia Workhorse K2700','CF 173906','2011','2011-03-01','KNCSHX71LB7549402','J2570979','','1530','Diesel','60','708283 16 0249 1387','2011-11-28','White','KIA Tygerberg','021-949 2558','9',1,5,'2011-11-28 00:00:00'),(7,'Kia Workhorse K2700','CF 173907','2011','2011-03-01','KNCSHX71LB7549403','J2571930','','1530','Diesel','60','708283 16 0250 9352','2011-11-28','White','KIA Tygerberg','021-949 2558','1',1,5,'2011-11-28 00:00:00'),(8,'TATA 713 S Tipper','CF 37734','2007','2007-02-01','MAT39932267R52586','697D41KTZ904204','1001055C1LST','4140','Diesel','90','708283 15 0173 9076','2011-11-28','White','TATA Truck Service Centre','021-981 9894','11',1,5,'2011-11-28 00:00:00'),(9,'TATA 713 S Tipper','CF 47911','2009','2009-07-01','MAT39932287R26400','697D41FRZ833439','','4140','Diesel','90','708283 15 0223 5751','2011-11-28','White','TATA Truck Service Centre','021-981 9894','28',1,5,'2011-11-28 00:00:00'),(10,'TATA Tipper LPT 813 EX2 F/C C/C','CF 177206','2011','2011-05-01','MAT499051A7R38737','697TC55KZY855589','','4380','Diesel','90','708283 16 0174 8028','2011-11-28','White','TATA Truck Service Centre','021-981 9894','13',1,5,'2011-11-28 00:00:00'),(11,'Mitsubishi Colt 2800 Tdi ClubCab','CF 70104','2006','2007-03-01','ABJK67HNR2E059320','4M40GA5663','10010558L3RB','1715','Diesel','95','708283 15 0174 8028','2011-11-28','White','Eikestad Motors','021-887 6900','35',1,5,'2011-11-28 00:00:00'),(12,'Mitsubishi Colt 2400i Rodeo','CF 141921','','2009-02-01','','','','1715','Diesel','95','708283 15 0211 7058','2011-11-28','White','Own','','1',0,5,'2011-11-28 00:00:00'),(13,'Kia Sportage','CY 348528','2011','2011-11-01','KNAPC8116C7233567','G4KDBF174037','','','Unleaded','85','708283 16 0255 9050','2011-11-29','White','KIA Tygerberg','021-949 2558','32',1,5,'2011-11-29 00:00:00'),(14,'Opel Corsa 1.4 Club Utility','CF 138038','2008','2008-03-01','ADMXF80JGB4448886','6W0080794','1001055F8JZV','1090','Unleaded','45','708283 15 0191 3408','2011-11-29','White','Ferndale Motors','021-903 0135','1',1,5,'2011-11-29 00:00:00'),(15,'Opel Corsa Utility 1.4i Base','CF 149890','2009','2009-10-01','ADMXF80JA84484677','6W0092174','','1090','Unleaded','45','708283 15 0245 0665','2011-11-29','White','Ferndale Motors','021-903 0135','16',1,5,'2011-11-29 00:00:00'),(16,'Opel Corsa 1.4 Club Utility','CF 156980','2009','2009-10-01','ADMXF80JG84510341','6W0102921','40CRL10341','1090','Unleaded','45','708283 15 0224 2146','2011-11-29','White','Ferndale Motors','021-903 0135','1',1,5,'2011-11-29 00:00:00'),(17,'Chevrolet Opel Corsa 1.8 Sport ','CF 143259','2010','2010-07-01','ADMXF80NE845332719','7W0016621','','1140','Unleaded','45','708283 15 0239 8187','2011-11-29','White','Ferndale Motors','021-903 0135','2',1,5,'2011-11-29 00:00:00'),(18,'Chevrolet Opel Corsa 1.4 Club Utility','CF 124798','2010','2010-11-01','ADMXF80JG84536341','6W0115007','','1090','Unleaded','45','708283 15 0245 0376','2011-11-29','White','Ferndale Motors','021-903 0135','36',1,5,'2011-11-29 00:00:00'),(19,'Chevrolet Opel Corsa 1.4 Club Utility','CF 132261','2011','2011-02-01','ADMXF80JG84551983','6W0121157','','1090','Unleaded','45','708283 15 0247 9747','2011-11-29','White','Ferndale Motors','021-903 0135','25',1,5,'2011-11-29 00:00:00'),(20,'Chevrolet Opel Corsa 1.4 Club Utility','CF 172182','2011','2011-11-29','ADMXF80JG84544403','6W0118405','','1090','Unleaded','45','708283 16 0247 9754','2011-11-29','White','Ferndale Motors','021-903 0135','21',1,5,'2011-11-29 00:00:00'),(21,'Chevrolet Opel Corsa 1.4 Club Utility','CF 172842','2011','2011-11-29','ADMXF80JG84555039','6W0122765','','1090','Unleaded','45','708283 16 0248 3848','2011-11-29','White','Ferndale Motors','021-903 0135','22',1,5,'2011-11-29 00:00:00'),(22,'Chevrolet Corsa 1.4 Club Utility','CF 101794','2011','2011-11-29','ADMXF80JG84570640','6W0130666','','1090','Unleaded','45','708283 16 0254 6149','2011-11-29','White','Ferndale Motors','021-903 0135','8',1,5,'2011-11-29 00:00:00'),(23,'Chevrolet Corsa 1.4 Club Utility','CF 91233','2011','2011-10-01','ADMXF80JG84570923','6W0130814','','1090','Unleaded','45','708283 16 0254 6131','2011-11-29','White','Ferndale Motors','021-903 0135','37',1,5,'2011-11-29 00:00:00'),(24,'Mercedes-Benz ML 63 AMG','CF 35367','2010','2011-11-29','WDC1641772A605230','15698060057650','','2310','Uneaded','85','708283 15 0239 8179','2011-11-29','White','Mercedes-Benz Century City','021-528 0400','2',1,5,'2011-11-29 00:00:00'),(25,'Mercedes-Benz ML 350','CF 45400','2010','2010-07-01','WDC1641862A606700','27296731490274','','2135','Unleaded','85','708283 15 0239 8153','2011-11-29','Silver','Mercedes-Benz Century City','021-528 0400','3',1,5,'2011-11-29 00:00:00'),(26,'Ford Tracer','CF 169083','2001','2007-04-01','AFAVLDL44VR380938','3B104830','','933','Petrol','45','None','2011-11-29','White','','','1',0,5,'2011-11-29 00:00:00'),(27,'Datsun 1200','CF 132103','1975','2011-11-29','','','','','Petrol','45','None','2011-11-29','','','','1',0,5,'2011-11-29 00:00:00'),(28,'H2.5FT L Forklift Truck','','2011','2011-11-29','Serial No: L177B32967J','','','','Gas','','','2011-11-29','Yellow','Barloworld Handling','0800 01 00 88','38',1,5,'2011-11-29 00:00:00'),(29,'MAN 26-280 CLA','CF 185988','2011','2011-11-29','AAMMC60689PX25450','6DBC07356','1001055V9RWB','11420','Diesel','300','','2011-11-29','White','MAN Truck Services','021-980 2720','27',1,5,'2011-11-29 00:00:00'),(30,'Bobcat Skid Steer Loader','BOBCAT01','2011','2011-10-01','','','','','Diesel','75','7082831602592309','2012-07-31','White','Bobcat','','31',1,5,'2011-11-29 00:00:00'),(31,'Trailer','CF 149289','2006','2011-11-29','','','','','','','','2011-11-29','Grey','','','1',1,5,'2011-11-29 00:00:00'),(32,'KIA Sorento 3.5 V6','CF 119816 - CY 89696','2005','2007-05-01','KNEJC523855441601','G6U5112617U','1001055CC9MM','1984','Petrol','90','708283 15 0245 3370','2011-11-29','Blue-Grey','KIA Tygerberg','021-949 2558','1',0,5,'2011-11-29 00:00:00'),(33,'Mercedes-Benz ML 500','CF 35367','2007','2007-04-01','WDC1641752A231729','11396430746519','1001055CC9N5','','Unleaded','85','','2011-11-29','midnight-blue','Mercedes-Benz Century City','021-528 0400','1',0,5,'2011-11-29 00:00:00'),(34,'Mercedes-Benz 280E','CF 45400','','2011-11-29','','','','','Unleaded','','','2011-11-29','White','Mercedes-Benz Century City','021-528 0400','1',0,5,'2011-11-29 00:00:00'),(35,'Mercedes-Benz Viano','CF 190470','2012','2012-03-01','WDF63981323709645','','','','Diesel','75','7082831602589680','2013-03-31','White','Mercedes-Benz Century City','021-5280400','1',1,7,'2012-03-30 00:00:00'),(36,'KIA Workhorse K2700','CF 158274','2013','2013-04-25','KNCSHX71LD7754296','J2649097','','1530','Diesel','','','0000-00-00','White','KIA Tygerberg','','34',1,7,'2013-04-29 00:00:00'),(37,'KIA Workhorse K2700','CF 159229','2013','2013-04-25','KNCSHX71LD7754295','J2649095','','1530','Diesel','','','0000-00-00','White','KIA Tygerberg','','1',1,7,'2013-04-29 00:00:00'),(38,'KIA Workhorse K2700','CF 160722','2013','2013-04-25','KNCSHX71LD7759571','J2651191','','1530','Diesel','','','0000-00-00','White','KIA Tygerberg','','1',1,7,'2013-04-29 00:00:00'),(39,'KIA Workhorse K2700','CF 159864','2013','2013-04-25','KNCSHX71LD7759057','J2651183','','1530','Diesel','','','0000-00-00','White','KIA Tygerberg','','1',1,7,'2013-04-29 00:00:00'),(40,'KIA Workhorse K2700','CF 155396','2013','2013-04-25','KNCSHX71LD7760529','J2651905','','1530','Diesel','','','0000-00-00','White','KIA Tygerberg','','1',1,7,'2013-04-29 00:00:00'),(41,'KIA Sportage','CF 157050','2013','2013-04-25','KNAPC811ND7447161','G4KDDH400988','','','Petrol','','','0000-00-00','White','KIA Tygerberg','','19',1,7,'2013-04-29 00:00:00'),(42,'KIA Sportage','CF 77218','2013','2013-04-26','KNAPC811ND7445202','G4KDDH400717','','','Petrol','','','0000-00-00','White','KIA Tygerberg','','20',1,7,'2013-04-29 00:00:00'),(43,'Toyota Hilux 4x4','CF 106620','2013','2013-04-26','AHTHZ29G502201954','1KDA022699','','1705','Diesel','','','0000-00-00','White','Barloworld Toyota Kuilsrivier','021-906 6811','29',1,7,'2013-04-29 00:00:00'),(44,'Toyota Hilux 2x4','CF 174660','2013','2013-04-29','AHTGZ39G700004054','1KDA090453','','1705','Diesel','','','0000-00-00','White','Barloworld Toyota Kuilsrivier','021-906 6811','23',1,7,'2013-04-29 00:00:00'),(45,'Toyota Hilux 2x4','CF 174726','2013','2013-04-29','AHTGZ39G500004019','1KDA090665','','1705','Diesel','','','0000-00-00','White','Barloworld Toyota Kuilsrivier','021-906 6811','15',1,7,'2013-04-29 00:00:00'),(46,'Toyota Hilux 2x4','CF 175999','2013','2013-04-29','AHTGZ39G700004037','1KDA097896','','1705','Diesel','','','0000-00-00','White','Barloworld Toyota Kuilsrivier','021-906 6811','24',1,7,'2013-04-29 00:00:00');
/*!40000 ALTER TABLE `tblfleetlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-01-08  9:18:51
