CREATE DATABASE  IF NOT EXISTS `medface` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `medface`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: medface
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `session` (
  `sessionid` int NOT NULL AUTO_INCREMENT,
  `period` enum('1','2','3') DEFAULT NULL,
  `day` date DEFAULT NULL,
  `term` enum('1','2','3') DEFAULT '1',
  `year` enum('1','2','3','4','5','6') DEFAULT '3',
  `room` varchar(400) DEFAULT NULL,
  `course` varchar(400) DEFAULT NULL,
  `lecturer` varchar(400) DEFAULT NULL,
  `modifytime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sessionid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `session_student`
--

DROP TABLE IF EXISTS `session_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `session_student` (
  `session_id` int NOT NULL,
  `detected_regno` varchar(15) DEFAULT NULL,
  `detected_facebox` varchar(405) DEFAULT NULL,
  `detected_source` varchar(405) DEFAULT NULL,
  `is_correct` bit(1) DEFAULT NULL,
  `corrected_regno` varchar(15) DEFAULT NULL,
  `modifytime` varchar(45) DEFAULT 'CURRENT_TIMESTAMP',
  PRIMARY KEY (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session_student`
--

LOCK TABLES `session_student` WRITE;
/*!40000 ALTER TABLE `session_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `session_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `id` int NOT NULL AUTO_INCREMENT,
  `regno` varchar(15) DEFAULT NULL,
  `fullname` varchar(450) DEFAULT NULL,
  `year` enum('1','2','3','4','5','6') DEFAULT NULL,
  `modifytime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `regno_UNIQUE` (`regno`),
  KEY `regno` (`regno`)
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'211010869','Abd ElMasih Sabry','3','2023-10-11 13:25:53'),(2,'221003615','Abdallah ElShalkany','3','2023-10-11 13:25:53'),(3,'211002984','Abdallah Emad','3','2023-10-11 13:25:53'),(4,'211011276','Abdallah Hisham','3','2023-10-11 13:25:53'),(5,'211003335','Abdallah Saied','3','2023-10-11 13:25:53'),(6,'211003626','Abdallah Salman','3','2023-10-11 13:25:53'),(7,'211010967','Abdel Rahman El Hasafy','3','2023-10-11 13:25:53'),(8,'211011032','Abdel Rahman Farid','3','2023-10-11 13:25:53'),(9,'211003497','Abdel Rahman Hegazy','3','2023-10-11 13:25:53'),(10,'211011145','Abdel Rahman Saniour','3','2023-10-11 13:25:53'),(11,'211000778','Abdel Rahman Wael','3','2023-10-11 13:25:53'),(12,'211003707','Abdellatif Ahmed','3','2023-10-11 13:25:53'),(13,'212001003','Abdelrahamn Barbary','3','2023-10-11 13:25:53'),(14,'211011152','Abdelrahman Ashour','3','2023-10-11 13:25:53'),(15,'211011035','Abdelrahman Seddik','3','2023-10-11 13:25:53'),(16,'212000100','Adham Ahmed','3','2023-10-11 13:25:53'),(17,'211002588','Ahmed Abdel Moez','3','2023-10-11 13:25:53'),(18,'211000072','Ahmed Agawany','3','2023-10-11 13:25:53'),(19,'211002997','Ahmed Attiah','3','2023-10-11 13:25:53'),(20,'212001131','Ahmed El ashry','3','2023-10-11 13:25:54'),(21,'211008964','Ahmed Elfeel','3','2023-10-11 13:25:54'),(22,'211011153','Ahmed Gabr','3','2023-10-11 13:25:54'),(23,'211001436','Ahmed Hassan','3','2023-10-11 13:25:54'),(24,'212001074','Ahmed Ibrahim','3','2023-10-11 13:25:54'),(25,'211003523','Ahmed Khamis','3','2023-10-11 13:25:54'),(26,'211003745','Ahmed Medhat','3','2023-10-11 13:25:54'),(27,'211011225','Ahmed Sherief','3','2023-10-11 13:25:54'),(28,'20100297','Ahmed Yasser','3','2023-10-11 13:25:54'),(29,'211000559','Alaa Harraz','3','2023-10-11 13:25:54'),(30,'211002693','Alaa Hassan','3','2023-10-11 13:25:54'),(31,'211002591','Aliaa Hablas','3','2023-10-11 13:25:54'),(32,'211002785','Amal Arafa','3','2023-10-11 13:25:54'),(33,'211003775','Ammar Yasser','3','2023-10-11 13:25:54'),(34,'231001961','Amr Hablas','3','2023-10-11 13:25:54'),(35,'211010329','Antony Mamdouh','3','2023-10-11 13:25:54'),(36,'211010755','Arsany Fawzy','3','2023-10-11 13:25:54'),(37,'211001914','Arwah Ahmed','3','2023-10-11 13:25:54'),(38,'211010358','Arwah Saleh','3','2023-10-11 13:25:54'),(39,'211010773','Ashrakat Hussien','3','2023-10-11 13:25:54'),(40,'212001084','Assem Mohamed','3','2023-10-11 13:25:54'),(41,'211003094','Asser Mahmoud','3','2023-10-11 13:25:54'),(42,'211000266','Aya Hisham','3','2023-10-11 13:25:54'),(43,'211011174','Baraa Hamdy','3','2023-10-11 13:25:54'),(44,'211000151','Bassant Gamal Eldin','3','2023-10-11 13:25:54'),(45,'211011044','Bassem Nader','3','2023-10-11 13:25:54'),(46,'211002721','Bassmala El Hashimy','3','2023-10-11 13:25:54'),(47,'211011177','Bassmalah Farag','3','2023-10-11 13:25:54'),(48,'211000278','Belal Hany','3','2023-10-11 13:25:54'),(49,'211003183','Donia Mohamed','3','2023-10-11 13:25:54'),(50,'211003418','Ehab Saber','3','2023-10-11 13:25:54'),(51,'212001409','Enjy Emad','3','2023-10-11 13:25:54'),(52,'211010842','Eyad Gamal','3','2023-10-11 13:25:54'),(53,'211000551','Farah Alian','3','2023-10-11 13:25:55'),(54,'211010750','Faris Rabie','3','2023-10-11 13:25:55'),(55,'211010102','Fatma Elzahraa Emad','3','2023-10-11 13:25:55'),(56,'211000798','Fliopater Gadallah','3','2023-10-11 13:25:55'),(57,'211000718','Fredy Emad','3','2023-10-11 13:25:55'),(58,'211003660','Habiba Mohamed','3','2023-10-11 13:25:55'),(59,'211000099','Hajer Barakat','3','2023-10-11 13:25:55'),(60,'212001020','Hamza Badawy','3','2023-10-11 13:25:55'),(61,'212001278','Hamza Tawfik','3','2023-10-11 13:25:55'),(62,'211000422','Hana Elserafy','3','2023-10-11 13:25:55'),(63,'211001708','Hana Hesham','3','2023-10-11 13:25:55'),(64,'211000535','Hanaa Islam','3','2023-10-11 13:25:55'),(65,'211000531','Haneen Mesbah','3','2023-10-11 13:25:55'),(66,'211001927','Hanin Zahran','3','2023-10-11 13:25:55'),(67,'211000864','Hazem Elsayed','3','2023-10-11 13:25:55'),(68,'211000548','Hazim Mostafa','3','2023-10-11 13:25:55'),(69,'211001452','Heba Ehab','3','2023-10-11 13:25:55'),(70,'211010811','Heba Elsayem','3','2023-10-11 13:25:55'),(71,'211002717','Heba Hammam','3','2023-10-11 13:25:55'),(72,'212001217','Ibrahim Elmahdy','3','2023-10-11 13:25:55'),(73,'212001107','Islam Alaa Eldin','3','2023-10-11 13:25:55'),(74,'211011070','Jana Ossama','3','2023-10-11 13:25:55'),(75,'211011260','Janah Shady','3','2023-10-11 13:25:55'),(76,'211003548','Janna Younis','3','2023-10-11 13:25:55'),(77,'211003023','Jannah Walid','3','2023-10-11 13:25:55'),(78,'211002333','Jasmin Hassan','3','2023-10-11 13:25:55'),(79,'211003661','Jessica Mashally','3','2023-10-11 13:25:55'),(80,'211008843','John Nabil','3','2023-10-11 13:25:55'),(81,'211000800','Karim Elsamadisy','3','2023-10-11 13:25:55'),(82,'211001707','Karim Hashim','3','2023-10-11 13:25:55'),(83,'211010553','karim Mohsen','3','2023-10-11 13:25:55'),(84,'211002699','Karim Shaalan','3','2023-10-11 13:25:55'),(85,'211001676','Kerolous Youssef','3','2023-10-11 13:25:55'),(86,'211011119','Khalid Essam','3','2023-10-11 13:25:55'),(87,'211010944','Kirollos William','3','2023-10-11 13:25:55'),(88,'211002789','Lama Galal','3','2023-10-11 13:25:55'),(89,'212001270','Lina Sameh','3','2023-10-11 13:25:55'),(90,'211000539','Logyn Attify','3','2023-10-11 13:25:55'),(91,'211011261','Lougin Shady','3','2023-10-11 13:25:55'),(92,'211012090','Magda Mohamed','3','2023-10-11 13:25:56'),(93,'211000767','Mahmoud Attian','3','2023-10-11 13:25:56'),(94,'211003042','Mahmoud Ossama','3','2023-10-11 13:25:56'),(95,'211003889','Mahmoud Yehia','3','2023-10-11 13:25:56'),(96,'211003737','Manar Shahin','3','2023-10-11 13:25:56'),(97,'211000137','Marwan Elkordy','3','2023-10-11 13:25:56'),(98,'211000809','Maryam Elsayed','3','2023-10-11 13:25:56'),(99,'212001112','Maryam Hammam','3','2023-10-11 13:25:56'),(100,'211000898','Maryam Sabry','3','2023-10-11 13:25:56'),(101,'211011097','Maryam Shaltout','3','2023-10-11 13:25:56'),(102,'211000007','Maryam Tamer','3','2023-10-11 13:25:56'),(103,'211001921','Maya Abdo','3','2023-10-11 13:25:56'),(104,'211000712','Mazin Bahnasy','3','2023-10-11 13:25:56'),(105,'211000104','Menna Elswefy','3','2023-10-11 13:25:56'),(106,'211000593','Menna Refaat','3','2023-10-11 13:25:56'),(107,'211003011','Menna Sabry','3','2023-10-11 13:25:56'),(108,'211000157','Menna Shamsiya','3','2023-10-11 13:25:56'),(109,'211010129','Mennah Mostafa','3','2023-10-11 13:25:56'),(110,'211000547','Merna Khalid','3','2023-10-11 13:25:56'),(111,'211008767','Merna Nasser','3','2023-10-11 13:25:56'),(112,'211001669','Mina Louise','3','2023-10-11 13:25:56'),(113,'211002523','Moaz Abdel Raouf','3','2023-10-11 13:25:56'),(114,'211001178','Mohamed Elgazar','3','2023-10-11 13:25:56'),(115,'212001377','Mohamed Hatem','3','2023-10-11 13:25:56'),(116,'2211002624','Mohamed Magdy','3','2023-10-11 13:25:56'),(117,'211010638','Mohamed Nazieh','3','2023-10-11 13:25:56'),(118,'211000784','Mohamed Ossama','3','2023-10-11 13:25:56'),(119,'212001034','Mohamed Sabry','3','2023-10-11 13:25:56'),(120,'211000408','Mohamed Saleh','3','2023-10-11 13:25:56'),(121,'211000977','Mohamed Younis','3','2023-10-11 13:25:56'),(122,'211009356','Mostafa Abdel Halim','3','2023-10-11 13:25:56'),(123,'211001167','Mostafa Ashraf','3','2023-10-11 13:25:56'),(124,'211008839','Mostafa Serah','3','2023-10-11 13:25:56'),(125,'211002656','Nabil Oraby','3','2023-10-11 13:25:56'),(126,'211002119','Nada Ashoush','3','2023-10-11 13:25:56'),(127,'211000858','Nermine Essam','3','2023-10-11 13:25:56'),(128,'211008086','Nour Mohsen','3','2023-10-11 13:25:56'),(129,'211010731','Nouran Khaled','3','2023-10-11 13:25:56'),(130,'211000649','Nourhan Zanaty','3','2023-10-11 13:25:56'),(131,'211000795','Omar Amin','3','2023-10-11 13:25:56'),(132,'211011222','Omar El Dakkak','3','2023-10-11 13:25:56'),(133,'211008096','Omar Ossama','3','2023-10-11 13:25:56'),(134,'211010703','Omnia Shaaban','3','2023-10-11 13:25:57'),(135,'211000720','Ponsieh Samer','3','2023-10-11 13:25:57'),(136,'211000053','Rahaf Ibrahim','3','2023-10-11 13:25:57'),(137,'211000406','Rana Badr','3','2023-10-11 13:25:57'),(138,'211008088','Rana Yasser','3','2023-10-11 13:25:57'),(139,'211002669','Ranah Elsayed','3','2023-10-11 13:25:57'),(140,'211000378','Reem Hafez','3','2023-10-11 13:25:57'),(141,'211011237','Reeman Elsayed','3','2023-10-11 13:25:57'),(142,'211000768','Renad Ashraf','3','2023-10-11 13:25:57'),(143,'211000124','Retan Hazim','3','2023-10-11 13:25:57'),(144,'211000280','Rown Adil','3','2023-10-11 13:25:57'),(145,'211003470','Safa Alaa','3','2023-10-11 13:25:57'),(146,'211000370','Saif Zaky','3','2023-10-11 13:25:57'),(147,'211010161','Salah Koriem','3','2023-10-11 13:25:57'),(148,'211010960','Saleh Mohamed','3','2023-10-11 13:25:57'),(149,'211003629','Sama Yasser','3','2023-10-11 13:25:57'),(150,'212001215','Sara Alaa','3','2023-10-11 13:25:57'),(151,'211003760','Sarah El Kerdawi','3','2023-10-11 13:25:57'),(152,'211008694','Sarah Harmoush','3','2023-10-11 13:25:57'),(153,'211011273','Shahd Roushdy','3','2023-10-11 13:25:57'),(154,'211003252','Sherif Ashraf','3','2023-10-11 13:25:57'),(155,'211003336','Sherihan Hassan','3','2023-10-11 13:25:57'),(156,'211008759','Sief Atta','3','2023-10-11 13:25:57'),(157,'211002967','Solan Amgad','3','2023-10-11 13:25:57'),(158,'211001492','Tya Yasser','3','2023-10-11 13:25:57'),(159,'211000869','Walid Bahlol','3','2023-10-11 13:25:57'),(160,'211003768','Wesal Diyaa','3','2023-10-11 13:25:57'),(161,'211010753','Yassin Kafrawy','3','2023-10-11 13:25:57'),(162,'211003630','Yassmin Kandil','3','2023-10-11 13:25:57'),(163,'211002262','Yousef Imam','3','2023-10-11 13:25:57'),(164,'211010968','Youssef Ali','3','2023-10-11 13:25:57'),(165,'211007008','Youssef Ettman','3','2023-10-11 13:25:57'),(166,'211002432','Youssef Sherif','3','2023-10-11 13:25:57'),(167,'211003211','Youssef Tantawy','3','2023-10-11 13:25:57'),(168,'211010040','Zainab Ibrahim','3','2023-10-11 13:25:57'),(169,'211002299','Zayneb Soliman','3','2023-10-11 13:25:57'),(170,'211010973','Zina Fayez','3','2023-10-11 13:25:58');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-11 13:47:14
