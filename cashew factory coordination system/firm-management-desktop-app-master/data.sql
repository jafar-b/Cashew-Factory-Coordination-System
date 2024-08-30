-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients` (
  `id` tinyint(4) DEFAULT NULL,
  `name` varchar(8) DEFAULT NULL,
  `address` varchar(8) DEFAULT NULL,
  `mobile` mediumint(9) DEFAULT NULL,
  `phone` mediumint(9) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES (2,'osffvne','njwnnewj',2342,23424),(3,'jnvjnejo','nreinn',671488,631497);
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `expenses` (
  `id` tinyint(4) DEFAULT NULL,
  `adate` varchar(0) DEFAULT NULL,
  `name` varchar(7) DEFAULT NULL,
  `rs` decimal(5,1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (1,'','wf',122.0),(3,'','machine',5678.0);
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labour_attendance`
--

DROP TABLE IF EXISTS `labour_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `labour_attendance` (
  `name` varchar(0) DEFAULT NULL,
  `Jun` varchar(0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labour_attendance`
--

LOCK TABLES `labour_attendance` WRITE;
/*!40000 ALTER TABLE `labour_attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `labour_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labour_details`
--

DROP TABLE IF EXISTS `labour_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `labour_details` (
  `name` varchar(1) DEFAULT NULL,
  `other` varchar(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labour_details`
--

LOCK TABLES `labour_details` WRITE;
/*!40000 ALTER TABLE `labour_details` DISABLE KEYS */;
INSERT INTO `labour_details` VALUES ('a','greading'),('b','greading'),('c','greading'),('',''),('d','cutting'),('',''),('e','cutting'),('',''),('',''),('',''),('',''),('',''),('',''),('',''),('',''),('',''),('b','sdams'),('','');
/*!40000 ALTER TABLE `labour_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labour_payment`
--

DROP TABLE IF EXISTS `labour_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `labour_payment` (
  `adate` varchar(0) DEFAULT NULL,
  `name` varchar(0) DEFAULT NULL,
  `rs` varchar(0) DEFAULT NULL,
  `ot` varchar(0) DEFAULT NULL,
  `total` varchar(0) DEFAULT NULL,
  `shift` varchar(0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labour_payment`
--

LOCK TABLES `labour_payment` WRITE;
/*!40000 ALTER TABLE `labour_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `labour_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ot`
--

DROP TABLE IF EXISTS `ot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ot` (
  `adate` varchar(0) DEFAULT NULL,
  `name` varchar(0) DEFAULT NULL,
  `hour` varchar(0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ot`
--

LOCK TABLES `ot` WRITE;
/*!40000 ALTER TABLE `ot` DISABLE KEYS */;
/*!40000 ALTER TABLE `ot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment` (
  `adate` varchar(0) DEFAULT NULL,
  `rs` smallint(6) DEFAULT NULL,
  `remark` varchar(2) DEFAULT NULL,
  `type` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES ('',545,'hh','payas');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production`
--

DROP TABLE IF EXISTS `production`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `production` (
  `adate` varchar(0) DEFAULT NULL,
  `tf` tinyint(4) DEFAULT NULL,
  `fh` tinyint(4) DEFAULT NULL,
  `ts` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production`
--

LOCK TABLES `production` WRITE;
/*!40000 ALTER TABLE `production` DISABLE KEYS */;
INSERT INTO `production` VALUES ('',0,0,0);
/*!40000 ALTER TABLE `production` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production_34gram`
--

DROP TABLE IF EXISTS `production_34gram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `production_34gram` (
  `adate` varchar(0) DEFAULT NULL,
  `tf` varchar(0) DEFAULT NULL,
  `fh` varchar(0) DEFAULT NULL,
  `ts` varchar(0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production_34gram`
--

LOCK TABLES `production_34gram` WRITE;
/*!40000 ALTER TABLE `production_34gram` DISABLE KEYS */;
/*!40000 ALTER TABLE `production_34gram` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production_oras`
--

DROP TABLE IF EXISTS `production_oras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `production_oras` (
  `adate` varchar(0) DEFAULT NULL,
  `tf` tinyint(4) DEFAULT NULL,
  `fh` smallint(6) DEFAULT NULL,
  `ts` mediumint(9) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production_oras`
--

LOCK TABLES `production_oras` WRITE;
/*!40000 ALTER TABLE `production_oras` DISABLE KEYS */;
INSERT INTO `production_oras` VALUES ('',33,4443,48479);
/*!40000 ALTER TABLE `production_oras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `production_payas`
--

DROP TABLE IF EXISTS `production_payas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `production_payas` (
  `adate` varchar(0) DEFAULT NULL,
  `tf` varchar(0) DEFAULT NULL,
  `fh` varchar(0) DEFAULT NULL,
  `ts` varchar(0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `production_payas`
--

LOCK TABLES `production_payas` WRITE;
/*!40000 ALTER TABLE `production_payas` DISABLE KEYS */;
/*!40000 ALTER TABLE `production_payas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `raw_material`
--

DROP TABLE IF EXISTS `raw_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raw_material` (
  `id` varchar(0) DEFAULT NULL,
  `adate` varchar(0) DEFAULT NULL,
  `raw` varchar(0) DEFAULT NULL,
  `type` varchar(0) DEFAULT NULL,
  `quantity` varchar(0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material`
--

LOCK TABLES `raw_material` WRITE;
/*!40000 ALTER TABLE `raw_material` DISABLE KEYS */;
/*!40000 ALTER TABLE `raw_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `raw_material_34gram`
--

DROP TABLE IF EXISTS `raw_material_34gram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raw_material_34gram` (
  `id` varchar(0) DEFAULT NULL,
  `adate` varchar(0) DEFAULT NULL,
  `raw` varchar(0) DEFAULT NULL,
  `type` varchar(0) DEFAULT NULL,
  `quantity` varchar(0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material_34gram`
--

LOCK TABLES `raw_material_34gram` WRITE;
/*!40000 ALTER TABLE `raw_material_34gram` DISABLE KEYS */;
/*!40000 ALTER TABLE `raw_material_34gram` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `raw_material_oras`
--

DROP TABLE IF EXISTS `raw_material_oras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raw_material_oras` (
  `id` tinyint(4) DEFAULT NULL,
  `adate` varchar(0) DEFAULT NULL,
  `raw` smallint(6) DEFAULT NULL,
  `type` varchar(4) DEFAULT NULL,
  `quantity` mediumint(9) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material_oras`
--

LOCK TABLES `raw_material_oras` WRITE;
/*!40000 ALTER TABLE `raw_material_oras` DISABLE KEYS */;
INSERT INTO `raw_material_oras` VALUES (1,'',1000,'caps',10000);
/*!40000 ALTER TABLE `raw_material_oras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `raw_material_payas`
--

DROP TABLE IF EXISTS `raw_material_payas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raw_material_payas` (
  `id` varchar(0) DEFAULT NULL,
  `adate` varchar(0) DEFAULT NULL,
  `raw` varchar(0) DEFAULT NULL,
  `type` varchar(0) DEFAULT NULL,
  `quantity` varchar(0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_material_payas`
--

LOCK TABLES `raw_material_payas` WRITE;
/*!40000 ALTER TABLE `raw_material_payas` DISABLE KEYS */;
/*!40000 ALTER TABLE `raw_material_payas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sell`
--

DROP TABLE IF EXISTS `sell`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sell` (
  `id` tinyint(4) DEFAULT NULL,
  `adate` varchar(0) DEFAULT NULL,
  `client` varchar(7) DEFAULT NULL,
  `item` smallint(6) DEFAULT NULL,
  `quantity` smallint(6) DEFAULT NULL,
  `rate` decimal(3,1) DEFAULT NULL,
  `total` decimal(5,1) DEFAULT NULL,
  `paid` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sell`
--

LOCK TABLES `sell` WRITE;
/*!40000 ALTER TABLE `sell` DISABLE KEYS */;
INSERT INTO `sell` VALUES (1,'','osffvne',250,222,10.0,2619.6,'paid');
/*!40000 ALTER TABLE `sell` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sqlite_sequence`
--

DROP TABLE IF EXISTS `sqlite_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sqlite_sequence` (
  `name` varchar(17) DEFAULT NULL,
  `seq` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sqlite_sequence`
--

LOCK TABLES `sqlite_sequence` WRITE;
/*!40000 ALTER TABLE `sqlite_sequence` DISABLE KEYS */;
INSERT INTO `sqlite_sequence` VALUES ('raw_material_oras',1),('clients',4),('expenses',3),('sell',1);
/*!40000 ALTER TABLE `sqlite_sequence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_maintenance`
--

DROP TABLE IF EXISTS `stock_maintenance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_maintenance` (
  `tf` mediumint(9) DEFAULT NULL,
  `fh` tinyint(4) DEFAULT NULL,
  `ts` tinyint(4) DEFAULT NULL,
  `preform250` tinyint(4) DEFAULT NULL,
  `preform500` tinyint(4) DEFAULT NULL,
  `preform1000` tinyint(4) DEFAULT NULL,
  `lable250` tinyint(4) DEFAULT NULL,
  `lable500` tinyint(4) DEFAULT NULL,
  `lable1000` tinyint(4) DEFAULT NULL,
  `caps250` tinyint(4) DEFAULT NULL,
  `caps500` tinyint(4) DEFAULT NULL,
  `caps1000` tinyint(4) DEFAULT NULL,
  `boxes250` tinyint(4) DEFAULT NULL,
  `boxes500` tinyint(4) DEFAULT NULL,
  `boxes1000` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_maintenance`
--

LOCK TABLES `stock_maintenance` WRITE;
/*!40000 ALTER TABLE `stock_maintenance` DISABLE KEYS */;
INSERT INTO `stock_maintenance` VALUES (-7770,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `stock_maintenance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_maintenance_34gram`
--

DROP TABLE IF EXISTS `stock_maintenance_34gram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_maintenance_34gram` (
  `tf` tinyint(4) DEFAULT NULL,
  `fh` tinyint(4) DEFAULT NULL,
  `ts` tinyint(4) DEFAULT NULL,
  `preform250` tinyint(4) DEFAULT NULL,
  `preform500` tinyint(4) DEFAULT NULL,
  `preform1000` tinyint(4) DEFAULT NULL,
  `lable250` tinyint(4) DEFAULT NULL,
  `lable500` tinyint(4) DEFAULT NULL,
  `lable1000` tinyint(4) DEFAULT NULL,
  `caps250` tinyint(4) DEFAULT NULL,
  `caps500` tinyint(4) DEFAULT NULL,
  `caps1000` tinyint(4) DEFAULT NULL,
  `boxes250` tinyint(4) DEFAULT NULL,
  `boxes500` tinyint(4) DEFAULT NULL,
  `boxes1000` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_maintenance_34gram`
--

LOCK TABLES `stock_maintenance_34gram` WRITE;
/*!40000 ALTER TABLE `stock_maintenance_34gram` DISABLE KEYS */;
INSERT INTO `stock_maintenance_34gram` VALUES (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `stock_maintenance_34gram` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_maintenance_oras`
--

DROP TABLE IF EXISTS `stock_maintenance_oras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_maintenance_oras` (
  `tf` tinyint(4) DEFAULT NULL,
  `fh` smallint(6) DEFAULT NULL,
  `ts` mediumint(9) DEFAULT NULL,
  `preform250` decimal(3,2) DEFAULT NULL,
  `preform500` decimal(4,2) DEFAULT NULL,
  `preform1000` decimal(5,2) DEFAULT NULL,
  `lable250` smallint(6) DEFAULT NULL,
  `lable500` mediumint(9) DEFAULT NULL,
  `lable1000` mediumint(9) DEFAULT NULL,
  `caps250` smallint(6) DEFAULT NULL,
  `caps500` mediumint(9) DEFAULT NULL,
  `caps1000` mediumint(9) DEFAULT NULL,
  `boxes250` tinyint(4) DEFAULT NULL,
  `boxes500` smallint(6) DEFAULT NULL,
  `boxes1000` mediumint(9) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_maintenance_oras`
--

LOCK TABLES `stock_maintenance_oras` WRITE;
/*!40000 ALTER TABLE `stock_maintenance_oras` DISABLE KEYS */;
INSERT INTO `stock_maintenance_oras` VALUES (33,4443,48479,-0.31,-63.47,-950.57,-33,-4443,-48479,-33,-4443,-38479,-1,-186,-4040);
/*!40000 ALTER TABLE `stock_maintenance_oras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_maintenance_payas`
--

DROP TABLE IF EXISTS `stock_maintenance_payas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_maintenance_payas` (
  `tf` tinyint(4) DEFAULT NULL,
  `fh` tinyint(4) DEFAULT NULL,
  `ts` tinyint(4) DEFAULT NULL,
  `preform250` tinyint(4) DEFAULT NULL,
  `preform500` tinyint(4) DEFAULT NULL,
  `preform1000` tinyint(4) DEFAULT NULL,
  `lable250` tinyint(4) DEFAULT NULL,
  `lable500` tinyint(4) DEFAULT NULL,
  `lable1000` tinyint(4) DEFAULT NULL,
  `caps250` tinyint(4) DEFAULT NULL,
  `caps500` tinyint(4) DEFAULT NULL,
  `caps1000` tinyint(4) DEFAULT NULL,
  `boxes250` tinyint(4) DEFAULT NULL,
  `boxes500` tinyint(4) DEFAULT NULL,
  `boxes1000` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_maintenance_payas`
--

LOCK TABLES `stock_maintenance_payas` WRITE;
/*!40000 ALTER TABLE `stock_maintenance_payas` DISABLE KEYS */;
INSERT INTO `stock_maintenance_payas` VALUES (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `stock_maintenance_payas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `username` varchar(5) DEFAULT NULL,
  `password` varchar(5) DEFAULT NULL,
  `question` varchar(26) DEFAULT NULL,
  `answer` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('admin','admin','What is your Birth Place ?','kudal');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-08-22 15:26:20
