-- MySQL dump 10.13  Distrib 5.5.44, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: Website
-- ------------------------------------------------------
-- Server version	5.5.44-0ubuntu0.14.04.1

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
-- Table structure for table `Info`
--

DROP TABLE IF EXISTS `Info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Info` (
  `Headers` varchar(200) DEFAULT NULL,
  `Info` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Info`
--

LOCK TABLES `Info` WRITE;
/*!40000 ALTER TABLE `Info` DISABLE KEYS */;
INSERT INTO `Info` VALUES ('Headers','Info'),('How to feed your Dino','This is some text0'),('Your Dino is gone, what to do','Your Dino is gone, what to do'),('Your Dino is gone, what to do','RUNN!!!');
/*!40000 ALTER TABLE `Info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Products`
--

DROP TABLE IF EXISTS `Products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Products` (
  `Text` varchar(200) DEFAULT NULL,
  `Price` varchar(8) DEFAULT NULL,
  `Img` varchar(100) DEFAULT NULL,
  `Quantity` varchar(3) DEFAULT NULL,
  `txid` varchar(10) DEFAULT NULL,
  `Proof_of_purchase` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Products`
--

LOCK TABLES `Products` WRITE;
/*!40000 ALTER TABLE `Products` DISABLE KEYS */;
INSERT INTO `Products` VALUES (' The first Dino for sale','5','photos/mammoth.png','3','12','null'),('THE RED  FLAG','1000000','photos/redflag.png','1','99','PLACE THE RED FLAG HERE'),('Just a regular old dinosour','50','photos/regular.jpeg','80','15412','null'),('WHAT IS NOT TO LIKE ABOUT A TREX','750','photos/trex.jpeg','900','15412','null');
/*!40000 ALTER TABLE `Products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Purchases`
--

DROP TABLE IF EXISTS `Purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Purchases` (
  `txid` varchar(20) DEFAULT NULL,
  `amount` varchar(20) DEFAULT NULL,
  `paid` varchar(20) DEFAULT NULL,
  `Proof_of_purchase` varchar(128) DEFAULT NULL,
  `Tracker` mediumint(9) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Tracker`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Purchases`
--

LOCK TABLES `Purchases` WRITE;
/*!40000 ALTER TABLE `Purchases` DISABLE KEYS */;
/*!40000 ALTER TABLE `Purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USER`
--

DROP TABLE IF EXISTS `USER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `USER` (
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USER`
--

LOCK TABLES `USER` WRITE;
/*!40000 ALTER TABLE `USER` DISABLE KEYS */;
INSERT INTO `USER` VALUES (NULL,NULL),('root','root'),('toor','root'),('secret','wordpass'),('charlie','hunter2'),('elon_gates','cdc'),('fred','bubbles'),('george','taco');
/*!40000 ALTER TABLE `USER` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-09-03 22:05:13
