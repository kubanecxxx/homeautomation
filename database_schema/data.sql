-- MySQL dump 10.15  Distrib 10.0.16-MariaDB, for Linux (x86_64)
--
-- Host: 192.168.1.1    Database: pisek
-- ------------------------------------------------------
-- Server version	5.1.53

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `programy`
--

LOCK TABLES `programy` WRITE;
/*!40000 ALTER TABLE `programy` DISABLE KEYS */;
INSERT INTO `programy` VALUES (3,15,'12:00:00','06:00:00',1,1,305),(3,26,'06:00:00','12:00:00',1,0,305),(3,17,'21:00:00','06:01:00',0,3,305),(3,16,'10:00:00','21:00:00',0,2,305),(3,15,'08:00:00','10:00:00',0,1,305),(2,43,'21:00:00','21:50:00',NULL,0,304),(2,43,'17:00:00','18:40:00',NULL,1,304),(1,25,'00:00:00','00:00:00',NULL,NULL,305),(3,10,'06:01:00','08:00:00',0,0,305),(4,100,'00:00:00','00:00:00',NULL,NULL,305),(0,-100,'00:00:00','00:00:00',NULL,NULL,305);
/*!40000 ALTER TABLE `programy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `programy_names`
--

LOCK TABLES `programy_names` WRITE;
/*!40000 ALTER TABLE `programy_names` DISABLE KEYS */;
INSERT INTO `programy_names` VALUES (0,'Vypnuto'),(1,'Manual'),(2,'Voda'),(3,'Topeni'),(4,'Zatop'),(100,'now'),(101,'previous'),(200,'teplota doma'),(201,'teplota voda'),(300,'jednotka zije'),(301,'opravdu topi - info z kotle'),(302,'cerpadlo v kotlu zapnuto'),(303,'chceme aby topil'),(304,'warm water temperature'),(305,'home temperature');
/*!40000 ALTER TABLE `programy_names` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-02-28 13:53:08
