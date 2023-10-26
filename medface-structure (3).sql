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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add medsession',7,'add_medsession'),(26,'Can change medsession',7,'change_medsession'),(27,'Can delete medsession',7,'delete_medsession'),(28,'Can view medsession',7,'view_medsession'),(29,'Can add person',8,'add_person'),(30,'Can change person',8,'change_person'),(31,'Can delete person',8,'delete_person'),(32,'Can view person',8,'view_person'),(33,'Can add image',9,'add_image'),(34,'Can change image',9,'change_image'),(35,'Can delete image',9,'delete_image'),(36,'Can view image',9,'view_image');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$g8p0rIg33AmCjtrBQJHa9x$0KXEO7d8ixPsYPX0GpeK/aHrC00sFL4IXHFzIrHjwLk=','2023-10-14 08:43:56.156946',1,'admin','','','ahmed.se@gmail.com',1,1,'2023-10-14 08:43:45.063490');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(9,'medapp','image'),(7,'medapp','medsession'),(8,'medapp','person'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-10-14 08:39:58.127023'),(2,'auth','0001_initial','2023-10-14 08:40:00.489340'),(3,'admin','0001_initial','2023-10-14 08:40:01.058471'),(4,'admin','0002_logentry_remove_auto_add','2023-10-14 08:40:01.090225'),(5,'admin','0003_logentry_add_action_flag_choices','2023-10-14 08:40:01.105847'),(6,'contenttypes','0002_remove_content_type_name','2023-10-14 08:40:01.306148'),(7,'auth','0002_alter_permission_name_max_length','2023-10-14 08:40:01.504900'),(8,'auth','0003_alter_user_email_max_length','2023-10-14 08:40:01.671860'),(9,'auth','0004_alter_user_username_opts','2023-10-14 08:40:01.688121'),(10,'auth','0005_alter_user_last_login_null','2023-10-14 08:40:01.822097'),(11,'auth','0006_require_contenttypes_0002','2023-10-14 08:40:01.872508'),(12,'auth','0007_alter_validators_add_error_messages','2023-10-14 08:40:01.905335'),(13,'auth','0008_alter_user_username_max_length','2023-10-14 08:40:02.152671'),(14,'auth','0009_alter_user_last_name_max_length','2023-10-14 08:40:02.302216'),(15,'auth','0010_alter_group_name_max_length','2023-10-14 08:40:02.368371'),(16,'auth','0011_update_proxy_permissions','2023-10-14 08:40:02.389882'),(17,'auth','0012_alter_user_first_name_max_length','2023-10-14 08:40:02.552209'),(18,'sessions','0001_initial','2023-10-14 08:40:02.700778'),(19,'medapp','0001_initial','2023-10-14 10:39:16.363943'),(20,'medapp','0002_image','2023-10-15 11:19:07.199674');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('khf15g6qghg5t039pl4j8bx90ofqa5yl','.eJxVjDsOwjAQBe_iGln-sPGakj5nsHa9NgmgRIqTCnF3iJQC2jcz76USbeuQtlaWNIq6KKtOvxtTfpRpB3Kn6TbrPE_rMrLeFX3QpvtZyvN6uH8HA7XhW3MoGZ1wjWSBO0fia2BvIAIbBzY4qR4RIdhsoyVTzyiuq4CdwWK8en8A53w3Rg:1qraFY:9Hn_4IsUkx-W8htDPY77F0ZNNjZ1SXrkop6RJEDeY94','2023-10-28 08:43:56.173226');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medapp_image`
--

DROP TABLE IF EXISTS `medapp_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medapp_image` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `medsession_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `medapp_image_medsession_id_68c43d35_fk_medapp_me` (`medsession_id`),
  CONSTRAINT `medapp_image_medsession_id_68c43d35_fk_medapp_me` FOREIGN KEY (`medsession_id`) REFERENCES `medapp_medsession` (`sessionid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medapp_image`
--

LOCK TABLES `medapp_image` WRITE;
/*!40000 ALTER TABLE `medapp_image` DISABLE KEYS */;
INSERT INTO `medapp_image` VALUES (1,'runs/3/1/2023-10-16/2/108/WhatsApp_Image_2023-10-15_at_12.45.30_PM.jpeg',7),(2,'runs/3/1/2023-10-16/1/108/WhatsApp_Image_2023-10-15_at_12.45.28_PM_1.jpeg',9),(3,'runs/3/1/2023-10-16/1/108/WhatsApp_Image_2023-10-15_at_12.45.29_PM_1.jpeg',10),(4,'runs/3/1/2023-10-16/1/108/WhatsApp_Image_2023-10-15_at_12.45.29_PM.jpeg',10),(5,'runs/3/1/2023-10-16/1/108/WhatsApp_Image_2023-10-15_at_12.45.28_PM.jpeg',10),(6,'runs/3/1/2023-10-16/1/607/WhatsApp_Image_2023-10-15_at_12.45.27_PM_1.jpeg',12),(7,'runs/3/1/2023-10-16/1/607/WhatsApp_Image_2023-10-15_at_12.45.27_PM.jpeg',12),(8,'runs/3/1/2023-10-16/1/607/WhatsApp_Image_2023-10-15_at_12.45.29_PM_1.jpeg',12),(9,'runs/3/1/2023-10-16/1/052/WhatsApp_Image_2023-10-07_at_9.49.47_AM_1.jpeg',13),(10,'runs/3/1/2023-10-16/1/052/WhatsApp_Image_2023-10-07_at_9.49.47_AM_1_IRy73U2.jpeg',13),(11,'runs/3/1/2023-10-16/1/052/WhatsApp_Image_2023-10-07_at_9.49.45_AM.jpeg',13),(12,'runs/3/1/2023-10-16/1/052/WhatsApp_Image_2023-10-15_at_12.45.29_PM.jpeg',13);
/*!40000 ALTER TABLE `medapp_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medapp_medsession`
--

DROP TABLE IF EXISTS `medapp_medsession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medapp_medsession` (
  `sessionid` int NOT NULL AUTO_INCREMENT,
  `period` varchar(1) NOT NULL,
  `day` date NOT NULL,
  `term` varchar(1) NOT NULL,
  `year` varchar(1) NOT NULL,
  `room` varchar(400) NOT NULL,
  `course` varchar(400) NOT NULL,
  `lecturer` varchar(400) NOT NULL,
  `modifytime` datetime(6) NOT NULL,
  PRIMARY KEY (`sessionid`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medapp_medsession`
--

LOCK TABLES `medapp_medsession` WRITE;
/*!40000 ALTER TABLE `medapp_medsession` DISABLE KEYS */;
INSERT INTO `medapp_medsession` VALUES (1,'1','2023-10-15','1','3','108','new course','any','2023-10-15 09:17:41.219490'),(3,'3','2023-10-16','2','3','052','Cell Biology','Dr. Ahmed -aa','2023-10-15 10:26:57.072311'),(4,'3','2023-10-15','2','3','607','Cell Biology','Dr. Ahmed','2023-10-15 10:26:47.544908'),(5,'3','2023-10-15','2','3','607','Cell Biology','Dr. Ahmed','2023-10-15 11:20:33.528293'),(6,'3','2023-10-15','1','3','052','any','Dr. Ahmed','2023-10-15 11:30:17.439724'),(7,'2','2023-10-16','1','3','108','any','any','2023-10-16 06:36:52.554531'),(8,'1','2023-10-16','1','3','607','new course','Dr. Ahmed','2023-10-16 06:45:09.304464'),(9,'1','2023-10-16','1','3','108','Cell Biology','Dr. Ahmed','2023-10-16 06:46:04.702319'),(10,'1','2023-10-16','1','3','108','Cell Biology','Dr. Ahmed','2023-10-16 06:46:48.444570'),(11,'1','2023-10-16','1','3','607','any','Dr. Ahmed -aa','2023-10-16 06:55:24.127988'),(12,'1','2023-10-16','1','3','607','Cell Biology','Dr. Ahmed -aa','2023-10-16 06:56:06.904873'),(13,'1','2023-10-16','1','3','052','Cell Biology','Dr. Ahmed -aa','2023-10-16 07:06:52.082934');
/*!40000 ALTER TABLE `medapp_medsession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medapp_person`
--

DROP TABLE IF EXISTS `medapp_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medapp_person` (
  `id` int NOT NULL AUTO_INCREMENT,
  `regno` varchar(15) NOT NULL,
  `fullname` varchar(450) NOT NULL,
  `year` varchar(1) NOT NULL,
  `modifytime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `regno` (`regno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medapp_person`
--

LOCK TABLES `medapp_person` WRITE;
/*!40000 ALTER TABLE `medapp_person` DISABLE KEYS */;
/*!40000 ALTER TABLE `medapp_person` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-16 11:09:10
