-- MySQL dump 10.13  Distrib 5.1.53, for openwrt-linux-gnu (mips)
--
-- Host: localhost    Database: pisek
-- ------------------------------------------------------
-- Server version	5.1.53

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
-- Table structure for table `program`
--

DROP TABLE IF EXISTS `program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `program` (
  `id_count` int(11) NOT NULL DEFAULT '0',
  `id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_count`,`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program`
--

LOCK TABLES `program` WRITE;
/*!40000 ALTER TABLE `program` DISABLE KEYS */;
INSERT INTO `program` VALUES (100,2),(101,0);
/*!40000 ALTER TABLE `program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programy`
--

DROP TABLE IF EXISTS `programy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `programy` (
  `id` int(11) NOT NULL,
  `teplota` float DEFAULT NULL,
  `start` time DEFAULT NULL,
  `stop` time DEFAULT NULL,
  `weekend` tinyint(1) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  UNIQUE KEY `moje` (`id`,`teplota`,`start`,`stop`,`weekend`,`number`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programy`
--

LOCK TABLES `programy` WRITE;
/*!40000 ALTER TABLE `programy` DISABLE KEYS */;
INSERT INTO `programy` VALUES (0,-100,'00:00:00','00:00:00',NULL,NULL),(1,25,'00:00:00','00:00:00',NULL,NULL),(2,100,'16:00:00','18:00:00',NULL,1),(2,100,'17:30:00','01:00:00',NULL,0),(3,25,'06:00:00','08:00:00',0,0),(3,25,'06:00:00','08:00:00',1,0),(3,26,'08:00:00','12:00:00',0,1),(3,26,'08:00:00','12:00:00',1,1),(3,27,'12:00:00','18:00:00',0,2),(3,29,'18:00:00','06:00:00',0,3),(4,100,'00:00:00','00:00:00',NULL,NULL);
/*!40000 ALTER TABLE `programy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programy_names`
--

DROP TABLE IF EXISTS `programy_names`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `programy_names` (
  `id` int(11) NOT NULL,
  `name` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programy_names`
--

LOCK TABLES `programy_names` WRITE;
/*!40000 ALTER TABLE `programy_names` DISABLE KEYS */;
INSERT INTO `programy_names` VALUES (0,'Vypnuto'),(1,'Manual'),(2,'Voda'),(3,'Topeni'),(4,'Zatop'),(100,'now'),(101,'previous'),(200,'teplota doma'),(201,'teplota voda');
/*!40000 ALTER TABLE `programy_names` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temperatures`
--

DROP TABLE IF EXISTS `temperatures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `temperatures` (
  `cas` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` float NOT NULL,
  `sensor` int(11) NOT NULL,
  PRIMARY KEY (`cas`,`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temperatures`
--

LOCK TABLES `temperatures` WRITE;
/*!40000 ALTER TABLE `temperatures` DISABLE KEYS */;
INSERT INTO `temperatures` VALUES ('2014-04-14 18:36:57',1,100,200),('2014-04-14 18:37:09',1,150,201),('2014-04-14 18:37:26',1,150,201),('2014-04-14 18:37:38',1,150,201),('2014-04-14 18:37:38',2,150,201),('2014-04-14 19:25:34',1,20,200);
/*!40000 ALTER TABLE `temperatures` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'pisek'
--
/*!50003 DROP FUNCTION IF EXISTS `sp_isweekend` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`kubanec`@`192.168.1.148`*/ /*!50003 FUNCTION `sp_isweekend`() RETURNS tinyint(1)
begin
	return dayofweek(now())	= 1 or dayofweek(now()) = 7;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `sp_program` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`kubanec`@`192.168.1.148`*/ /*!50003 FUNCTION `sp_program`() RETURNS int(11)
begin
	declare ja int;
	select id into ja from program where id_count = 100;
	return ja;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `sp_requestedTemperature` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`kubanec`@`192.168.1.148`*/ /*!50003 FUNCTION `sp_requestedTemperature`() RETURNS float
begin
	declare idd int;
	declare cant float;
	select id into idd from program where id_count = 100;
	select teplota into cant from programy where 
	if (start < stop , curtime() > start and curtime() < stop  ,
	curtime() > start and time_to_sec(curtime()) < time_to_sec(stop) + 86400)	
	and id = idd and (weekend is NULL or sp_isweekend() = weekend) order by teplota desc limit 1;
	return cant;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP FUNCTION IF EXISTS `sp_topit` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`kubanec`@`192.168.1.148`*/ /*!50003 FUNCTION `sp_topit`() RETURNS tinyint(1)
begin
	declare ja float;
	declare t float;
	select value into t from temperatures where sensor = 200 order by cas desc limit 1;
	select sp_requestedTemperature() into ja;
	if (ja > t) then return true; end if;	
	return false;
	
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_configureProgram` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`kubanec`@`192.168.1.148`*/ /*!50003 PROCEDURE `sp_configureProgram`(id int, temperature float, start time , stop time , weekend boolean, number int)
begin
	declare maximum int;
	set maximum=4;
	case id
		when 1 then update programy set teplota=temperature where programy.id=1;
		when 2 then update programy set programy.start = start, programy.stop = stop where programy.id=2 and programy.number = number;
		when 3 then 
			if (weekend) then set maximum=2; end if;
			update programy set teplota = temperature, programy.start = start where programy.id = 3 and programy.number = number and programy.weekend = weekend;
			update programy set programy.stop = start where programy.id = 3 and programy.weekend = weekend and 
			programy.number = (number - 1) + (!number * maximum);
	end case;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_getProgramyNames` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`kubanec`@`192.168.1.148`*/ /*!50003 PROCEDURE `sp_getProgramyNames`()
begin
select programy.id,name,teplota from programy inner join programy_names on programy.id = programy_names.id  where if (start < stop , curtime() > start and curtime() < stop  ,
        curtime() > start and time_to_sec(curtime()) < time_to_sec(stop) + 86400)
         and (weekend is NULL or sp_isweekend() = weekend)  group by name order by programy.id  ;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_isweekend` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`kubanec`@`192.168.1.148`*/ /*!50003 PROCEDURE `sp_isweekend`()
begin
	select dayofweek(now())	= 1 or dayofweek(now()) = 7;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_selectProgram` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`kubanec`@`192.168.1.148`*/ /*!50003 PROCEDURE `sp_selectProgram`(id int)
begin
	declare m int;
	select program.id into m from program where id_count= 100;
	
	if (id != m ) then
	update program set program.id = m where id_count = 101;
	update program set program.id = id where id_count = 100;
	end if;
	
	if (id = 4) then alter event prestan_topit on schedule at current_timestamp + interval 30 minute enable;
	else alter event prestan_topit disable;
	end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-23 17:54:02
