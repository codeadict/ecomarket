-- MySQL dump 10.13  Distrib 5.5.41, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ecomdb_0
-- ------------------------------------------------------
-- Server version	5.5.41-0ubuntu0.12.04.1

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
-- Table structure for table `accounts_emailnotification`
--

DROP TABLE IF EXISTS `accounts_emailnotification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_emailnotification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `site_updates_features` tinyint(1) NOT NULL DEFAULT '1',
  `stall_owner_tips` tinyint(1) NOT NULL DEFAULT '1',
  `follower_notifications` tinyint(1) NOT NULL DEFAULT '1',
  `products_you_might_like` tinyint(1) NOT NULL DEFAULT '1',
  `private_messages` tinyint(1) NOT NULL DEFAULT '1',
  `orders` tinyint(1) NOT NULL DEFAULT '1',
  `customer_reviews` tinyint(1) NOT NULL DEFAULT '1',
  `share_orders_in_activity_feed` tinyint(1) NOT NULL,
  `blogs_you_might_like` tinyint(1) NOT NULL,
  `product_discounts` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_702f6493f115fb86` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_emailnotification`
--

LOCK TABLES `accounts_emailnotification` WRITE;
/*!40000 ALTER TABLE `accounts_emailnotification` DISABLE KEYS */;
INSERT INTO `accounts_emailnotification` VALUES (1,2,1,1,1,1,1,1,1,1,1,1);
/*!40000 ALTER TABLE `accounts_emailnotification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_privacy`
--

DROP TABLE IF EXISTS `accounts_privacy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_privacy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `profile_public` tinyint(1) NOT NULL DEFAULT '1',
  `share_purchases_in_activity` tinyint(1) NOT NULL DEFAULT '1',
  `love_list_public` tinyint(1) NOT NULL DEFAULT '1',
  `share_love_list_in_activity` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_id_614c4b7392e8fe6b` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_privacy`
--

LOCK TABLES `accounts_privacy` WRITE;
/*!40000 ALTER TABLE `accounts_privacy` DISABLE KEYS */;
INSERT INTO `accounts_privacy` VALUES (1,2,1,1,1,1);
/*!40000 ALTER TABLE `accounts_privacy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_shippingaddress`
--

DROP TABLE IF EXISTS `accounts_shippingaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_shippingaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL DEFAULT '',
  `line1` varchar(255) NOT NULL,
  `line2` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(50) NOT NULL,
  `postal_code` varchar(15) NOT NULL,
  `created` date NOT NULL,
  `updated` date NOT NULL,
  `country_id` int(11),
  `last_select_date_time` datetime,
  PRIMARY KEY (`id`),
  KEY `purchase_shippingaddress_fbfc09f1` (`user_id`),
  KEY `accounts_shippingaddress_eebc3676` (`country_id`),
  CONSTRAINT `country_id_refs_id_1d0b210e735f5e6f` FOREIGN KEY (`country_id`) REFERENCES `marketplace_country` (`id`),
  CONSTRAINT `user_id_refs_id_591319aa7d5a1bee` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_shippingaddress`
--

LOCK TABLES `accounts_shippingaddress` WRITE;
/*!40000 ALTER TABLE `accounts_shippingaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_shippingaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_userprofile`
--

DROP TABLE IF EXISTS `accounts_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `gender` varchar(1) NOT NULL DEFAULT '',
  `birthday` date DEFAULT NULL,
  `about_me` longtext NOT NULL,
  `send_newsletters` tinyint(1) NOT NULL DEFAULT '0',
  `activation_key` varchar(40) NOT NULL DEFAULT '',
  `avatar` varchar(100) DEFAULT NULL,
  `address_1` varchar(255) NOT NULL DEFAULT '',
  `address_2` varchar(255) NOT NULL DEFAULT '',
  `city` varchar(100) NOT NULL DEFAULT '',
  `state` varchar(100) NOT NULL DEFAULT '',
  `zipcode` varchar(20) NOT NULL DEFAULT '',
  `country_id` int(11) DEFAULT NULL,
  `data` longtext NOT NULL,
  `social_auth` varchar(32),
  `activation_key_date` datetime NOT NULL,
  `last_activities_update` datetime,
  `preferred_currency` varchar(3) NOT NULL,
  `detected_country` varchar(2),
  `activities_last_checked_at` datetime,
  `phone_number` varchar(16),
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `accounts_userprofile_eebc3676` (`country_id`),
  KEY `accounts_userprofile_534dd89` (`country_id`),
  CONSTRAINT `country_id_refs_id_7f8c5b9d2c321aa1` FOREIGN KEY (`country_id`) REFERENCES `marketplace_country` (`id`),
  CONSTRAINT `user_id_refs_id_6280a4b981d7010f` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_userprofile`
--

LOCK TABLES `accounts_userprofile` WRITE;
/*!40000 ALTER TABLE `accounts_userprofile` DISABLE KEYS */;
INSERT INTO `accounts_userprofile` VALUES (1,2,'m',NULL,'Im a programmer',1,'','avatar/dairon/ima.jpg','Huachi','José H Figueroa','Quito, Ecuador','Pichincha','ec98765',1,'{\"image_crop\": [342, 613, 90, 360]}','','2015-05-09 15:51:30','2015-05-09 21:15:03','USD','GB',NULL,NULL);
/*!40000 ALTER TABLE `accounts_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_userprofile_used_discounts`
--

DROP TABLE IF EXISTS `accounts_userprofile_used_discounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_userprofile_used_discounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `discount_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_userprofile_used__userprofile_id_307affa2d7b14d21_uniq` (`userprofile_id`,`discount_id`),
  KEY `accounts_userprofile_used_discounts_1be3128f` (`userprofile_id`),
  KEY `accounts_userprofile_used_discounts_a3ac940d` (`discount_id`),
  CONSTRAINT `discount_id_refs_id_2491a8fa953d74aa` FOREIGN KEY (`discount_id`) REFERENCES `discounts_discount` (`id`),
  CONSTRAINT `userprofile_id_refs_id_1c7a2031ac11d58d` FOREIGN KEY (`userprofile_id`) REFERENCES `accounts_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_userprofile_used_discounts`
--

LOCK TABLES `accounts_userprofile_used_discounts` WRITE;
/*!40000 ALTER TABLE `accounts_userprofile_used_discounts` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_userprofile_used_discounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_video`
--

DROP TABLE IF EXISTS `accounts_video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `video_type_id` int(11) NOT NULL,
  `title` varchar(120) DEFAULT NULL,
  `video_guid` varchar(40) NOT NULL,
  `embed_url` varchar(120) DEFAULT NULL,
  `splash_url` varchar(120) DEFAULT NULL,
  `is_reference` tinyint(1) NOT NULL DEFAULT '1',
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `accounts_video_fbfc09f1` (`user_id`),
  KEY `accounts_video_f275ea9e` (`video_type_id`),
  CONSTRAINT `video_type_id_refs_id_ea2ee38288dfa3` FOREIGN KEY (`video_type_id`) REFERENCES `accounts_videotype` (`id`),
  CONSTRAINT `user_id_refs_id_2c4b2221709521ea` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_video`
--

LOCK TABLES `accounts_video` WRITE;
/*!40000 ALTER TABLE `accounts_video` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_video` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_videotype`
--

DROP TABLE IF EXISTS `accounts_videotype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_videotype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `time_limit` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_videotype`
--

LOCK TABLES `accounts_videotype` WRITE;
/*!40000 ALTER TABLE `accounts_videotype` DISABLE KEYS */;
INSERT INTO `accounts_videotype` VALUES (1,'video de tienda',5);
/*!40000 ALTER TABLE `accounts_videotype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `actstream_action`
--

DROP TABLE IF EXISTS `actstream_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `actstream_action` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `actor_content_type_id` int(11) NOT NULL,
  `actor_object_id` varchar(255) NOT NULL,
  `verb` varchar(255) NOT NULL,
  `description` longtext,
  `target_content_type_id` int(11) DEFAULT NULL,
  `target_object_id` varchar(255),
  `action_object_content_type_id` int(11) DEFAULT NULL,
  `action_object_object_id` varchar(255),
  `timestamp` datetime NOT NULL,
  `public` tinyint(1) NOT NULL DEFAULT '1',
  `data` longtext,
  PRIMARY KEY (`id`),
  KEY `actstream_action_331f64c6` (`actor_content_type_id`),
  KEY `actstream_action_a980ac01` (`target_content_type_id`),
  KEY `actstream_action_ad8f5e45` (`action_object_content_type_id`),
  CONSTRAINT `action_object_content_type_id_refs_id_6f0ab83d91e6073f` FOREIGN KEY (`action_object_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `actor_content_type_id_refs_id_6f0ab83d91e6073f` FOREIGN KEY (`actor_content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `target_content_type_id_refs_id_6f0ab83d91e6073f` FOREIGN KEY (`target_content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actstream_action`
--

LOCK TABLES `actstream_action` WRITE;
/*!40000 ALTER TABLE `actstream_action` DISABLE KEYS */;
INSERT INTO `actstream_action` VALUES (1,3,'1','wrote a new blog post',NULL,72,'1',72,'1','2015-05-09 20:23:13',1,NULL),(2,3,'2','commented on',NULL,72,'1',76,'1','2015-05-09 20:24:49',1,NULL),(3,3,'2','wrote a new blog post',NULL,72,'2',72,'2','2015-05-09 20:31:11',1,NULL),(4,3,'2','commented on',NULL,72,'2',76,'2','2015-05-09 20:31:42',1,NULL),(5,3,'1','wrote a new blog post',NULL,72,'3',72,'3','2015-05-09 20:34:47',1,NULL),(6,3,'2','wrote a new blog post',NULL,72,'4',72,'4','2015-05-09 20:37:38',1,NULL),(7,3,'2','listed a new product on',NULL,33,'1',37,'1','2015-05-09 20:54:00',1,NULL),(8,3,'2','created the love list',NULL,57,'1',63,'1','2015-05-09 20:57:57',1,NULL),(9,3,'2','added product to love list',NULL,63,'1',64,'1','2015-05-09 20:58:07',1,NULL);
/*!40000 ALTER TABLE `actstream_action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `actstream_follow`
--

DROP TABLE IF EXISTS `actstream_follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `actstream_follow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `object_id` varchar(255) NOT NULL,
  `actor_only` tinyint(1) NOT NULL,
  `started` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `actstream_follow_user_id_49f02cb6d67a13f2_uniq` (`user_id`,`content_type_id`,`object_id`),
  KEY `actstream_follow_fbfc09f1` (`user_id`),
  KEY `actstream_follow_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_45b2c87143220e98` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_88c60c63d8a2214` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actstream_follow`
--

LOCK TABLES `actstream_follow` WRITE;
/*!40000 ALTER TABLE `actstream_follow` DISABLE KEYS */;
/*!40000 ALTER TABLE `actstream_follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analytics_aggregatedata`
--

DROP TABLE IF EXISTS `analytics_aggregatedata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analytics_aggregatedata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `campaign` varchar(60) NOT NULL,
  `daily_acquired` smallint(5) unsigned NOT NULL,
  `campaign_cost` double NOT NULL,
  `customer_acquistion_cost` double NOT NULL,
  `gross_merchant_value` double NOT NULL,
  `revenue_after_commission` double NOT NULL,
  `order_count` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analytics_aggregatedata`
--

LOCK TABLES `analytics_aggregatedata` WRITE;
/*!40000 ALTER TABLE `analytics_aggregatedata` DISABLE KEYS */;
/*!40000 ALTER TABLE `analytics_aggregatedata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analytics_campaigntrack`
--

DROP TABLE IF EXISTS `analytics_campaigntrack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analytics_campaigntrack` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11),
  `created_at` datetime NOT NULL,
  `source` varchar(60),
  `name` varchar(200) NOT NULL,
  `medium` varchar(60),
  `term` varchar(100),
  `content` varchar(60),
  `utmz` varchar(1000) NOT NULL,
  `sent_to_sailthru` tinyint(1) NOT NULL DEFAULT '0',
  `query_string` varchar(1000),
  `email_lead_id` int(11),
  `cookie_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `analytics_campaigntrack_user_id_289e75deca8f6032_uniq` (`user_id`,`name`),
  KEY `analytics_campaigntrack_fbfc09f1` (`user_id`),
  KEY `analytics_campaigntrack_16db9c07` (`email_lead_id`),
  KEY `analytics_campaigntrack_1ccf3be4` (`cookie_id`),
  CONSTRAINT `cookie_id_refs_id_702d93f1d4645a8e` FOREIGN KEY (`cookie_id`) REFERENCES `analytics_lifetimetrack` (`id`),
  CONSTRAINT `email_lead_id_refs_id_56b38eab6752e8d2` FOREIGN KEY (`email_lead_id`) REFERENCES `mailing_lists_mailinglistsignup` (`id`),
  CONSTRAINT `user_id_refs_id_830768d3df7cdb` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analytics_campaigntrack`
--

LOCK TABLES `analytics_campaigntrack` WRITE;
/*!40000 ALTER TABLE `analytics_campaigntrack` DISABLE KEYS */;
/*!40000 ALTER TABLE `analytics_campaigntrack` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analytics_lifetimetrack`
--

DROP TABLE IF EXISTS `analytics_lifetimetrack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analytics_lifetimetrack` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cookie_key` varchar(60) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `email_lead_id` int(11) DEFAULT NULL,
  `status` smallint(5) unsigned NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL,
  `acquired_at` datetime DEFAULT NULL,
  `activated_at` datetime DEFAULT NULL,
  `retained_at` datetime DEFAULT NULL,
  `referred_at` datetime DEFAULT NULL,
  `purchased_at` datetime DEFAULT NULL,
  `url_count` smallint(5) unsigned NOT NULL,
  `actual_activated_at` datetime,
  `actual_retained_at` datetime,
  `actual_referred_at` datetime,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cookie_key` (`cookie_key`),
  KEY `analytics_lifetimetrack_fbfc09f1` (`user_id`),
  KEY `analytics_lifetimetrack_16db9c07` (`email_lead_id`),
  CONSTRAINT `email_lead_id_refs_id_50c076a03d3013e1` FOREIGN KEY (`email_lead_id`) REFERENCES `mailing_lists_mailinglistsignup` (`id`),
  CONSTRAINT `user_id_refs_id_3b866d7e113af040` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analytics_lifetimetrack`
--

LOCK TABLES `analytics_lifetimetrack` WRITE;
/*!40000 ALTER TABLE `analytics_lifetimetrack` DISABLE KEYS */;
INSERT INTO `analytics_lifetimetrack` VALUES (1,'608c04fe603b4035b2fa34b90ea8a385',2,NULL,4,'2015-05-09 16:37:14','2015-05-09 15:51:29','2015-05-09 16:10:42',NULL,NULL,NULL,0,'2015-05-09 16:10:42',NULL,NULL);
/*!40000 ALTER TABLE `analytics_lifetimetrack` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `analytics_productformerrors`
--

DROP TABLE IF EXISTS `analytics_productformerrors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analytics_productformerrors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stall_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `product_form_error` tinyint(1) NOT NULL DEFAULT '0',
  `price_form_error` tinyint(1) NOT NULL DEFAULT '0',
  `shipping_form_error` tinyint(1) NOT NULL DEFAULT '0',
  `images_formset_error` tinyint(1) NOT NULL DEFAULT '0',
  `description_error` tinyint(1) NOT NULL DEFAULT '0',
  `recipients_error` tinyint(1) NOT NULL DEFAULT '0',
  `title_error` tinyint(1) NOT NULL DEFAULT '0',
  `colors_error` tinyint(1) NOT NULL DEFAULT '0',
  `keywords_field_error` tinyint(1) NOT NULL DEFAULT '0',
  `primary_category_error` tinyint(1) NOT NULL DEFAULT '0',
  `shipping_profile_error` tinyint(1) NOT NULL DEFAULT '0',
  `amount_error` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL,
  `had_error` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `analytics_productformerrors_368109e5` (`stall_id`),
  KEY `analytics_productformerrors_bb420c12` (`product_id`),
  CONSTRAINT `product_id_refs_id_4af399cb770883f7` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`),
  CONSTRAINT `stall_id_refs_id_1c168662282459ce` FOREIGN KEY (`stall_id`) REFERENCES `marketplace_stall` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `analytics_productformerrors`
--

LOCK TABLES `analytics_productformerrors` WRITE;
/*!40000 ALTER TABLE `analytics_productformerrors` DISABLE KEYS */;
INSERT INTO `analytics_productformerrors` VALUES (1,1,NULL,1,0,0,0,0,1,0,0,0,1,0,0,'2015-05-09 20:45:51',1),(2,1,NULL,1,0,0,0,0,1,0,0,0,1,0,0,'2015-05-09 20:47:23',1),(3,1,NULL,1,0,0,0,0,0,0,0,0,1,0,0,'2015-05-09 20:47:40',1),(4,1,NULL,1,0,0,0,0,0,0,0,0,1,0,0,'2015-05-09 20:49:23',1),(5,1,1,0,0,0,0,0,0,0,0,0,0,0,0,'2015-05-09 20:53:50',0);
/*!40000 ALTER TABLE `analytics_productformerrors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_article`
--

DROP TABLE IF EXISTS `articles_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `status_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `keywords` longtext NOT NULL,
  `description` longtext NOT NULL,
  `markup` varchar(1) NOT NULL DEFAULT 'h',
  `content` longtext NOT NULL,
  `rendered_content` longtext NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `auto_tag` tinyint(1) NOT NULL DEFAULT '1',
  `publish_date` datetime NOT NULL DEFAULT '2015-05-09 15:16:04',
  `expiration_date` datetime DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `login_required` tinyint(1) NOT NULL DEFAULT '0',
  `use_addthis_button` tinyint(1) NOT NULL DEFAULT '0',
  `addthis_use_author` tinyint(1) NOT NULL DEFAULT '1',
  `addthis_username` varchar(50) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `custom_unique_id` varchar(100),
  `seo_keyword` varchar(255),
  `seo_meta_title` varchar(255),
  PRIMARY KEY (`id`),
  KEY `articles_article_a951d5d6` (`slug`),
  KEY `articles_article_44224078` (`status_id`),
  KEY `articles_article_cc846901` (`author_id`),
  KEY `articles_article_42dc49bc` (`category_id`),
  CONSTRAINT `author_id_refs_id_6612f51921e48f8a` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `category_id_refs_id_64ec1011fedb1c92` FOREIGN KEY (`category_id`) REFERENCES `articles_blogcategory` (`id`),
  CONSTRAINT `status_id_refs_id_35ec5af709b761db` FOREIGN KEY (`status_id`) REFERENCES `articles_articlestatus` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_article`
--

LOCK TABLES `articles_article` WRITE;
/*!40000 ALTER TABLE `articles_article` DISABLE KEYS */;
INSERT INTO `articles_article` VALUES (1,'Ministerio de Cultura implementa proyecto de transmisión de saberes del tejido del sombrero de paja ','ministerio-de-cultura-implementa-proyecto-de-trans',2,1,'','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	El viernes 6 de junio del 2014 se realiz&oacute; un evento en la plaza de la parroquia Picoaz&aacute;, como parte del proyecto de transmisi&oacute;n de saberes del tejido tradicional del&nbsp;<a href=\"http://goo.gl/oaqC8l\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\" target=\"_blank\">sombrero de paja toquilla</a>. El evento fue organizado por la Subsecretar&iacute;a de Patrimonio del Ministerio de Cultura y Patrimonio, con el apoyo de la Direcci&oacute;n Provincial de Manab&iacute;.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<img alt=\"DSC04637\" class=\"alignleft wp-image-3438 size-medium\" height=\"225\" src=\"http://www.ecuadorianhands.com/blog-es/wp-content/uploads/2014/06/DSC04637-300x225.jpg\" style=\"float: left; margin: 0px 10px 10px 0px; display: inline; padding: 0px; height: auto;\" width=\"300\" />Este evento a pesar de su car&aacute;cter festivo gracias a la banda que ...</p>','h','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	El viernes 6 de junio del 2014 se realiz&oacute; un evento en la plaza de la parroquia Picoaz&aacute;, como parte del proyecto de transmisi&oacute;n de saberes del tejido tradicional del&nbsp;<a href=\"http://goo.gl/oaqC8l\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\" target=\"_blank\">sombrero de paja toquilla</a>. El evento fue organizado por la Subsecretar&iacute;a de Patrimonio del Ministerio de Cultura y Patrimonio, con el apoyo de la Direcci&oacute;n Provincial de Manab&iacute;.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<img alt=\"DSC04637\" class=\"alignleft wp-image-3438 size-medium\" height=\"225\" src=\"http://www.ecuadorianhands.com/blog-es/wp-content/uploads/2014/06/DSC04637-300x225.jpg\" style=\"float: left; margin: 0px 10px 10px 0px; display: inline; padding: 0px; height: auto;\" width=\"300\" />Este evento a pesar de su car&aacute;cter festivo gracias a la banda que inaugur&oacute; la ceremonia, tuvo un objetivo m&aacute;s profundo que el de solo entretener, fue la representaci&oacute;n del &ldquo;diagn&oacute;stico econ&oacute;mico y cultural&rdquo; que se est&aacute; haciendo del tejido de la paja toquilla en la regi&oacute;n manabita.&nbsp; No solo se busca un reflejo del n&uacute;mero de personas que dependen de la actividad en la zona, sino tambi&eacute;n del &aacute;mbito de exportaci&oacute;n, la capacidad de producci&oacute;n, cuales son los competidores, entre otros puntos clave.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Como no pod&iacute;a faltar el p&uacute;blico tuvo la dicha de escuchar la famosa canci&oacute;n &ldquo;tejedora manabita&rdquo; y los populares amorfinos tan caracter&iacute;sticos de la regi&oacute;n.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<a href=\"http://www.ecuadorianhands.com/blog-es/wp-content/uploads/2014/06/DSC04642.jpg\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\"><img alt=\"DSC04642\" class=\"alignright wp-image-3439 size-medium\" height=\"225\" src=\"http://www.ecuadorianhands.com/blog-es/wp-content/uploads/2014/06/DSC04642-300x225.jpg\" style=\"border: 0px; float: right; margin: 0px 0px 10px 10px; display: inline; padding: 0px; height: auto;\" width=\"300\" /></a>Si bien la asistencia &nbsp;fue buena, el reconocimiento que se otorg&oacute; a la representante de los tejedores en Picoaz&aacute;, Margarita Garc&iacute;a, no parec&iacute;a el adecuado. Un Bolso de tela en lugar de una placa conmemorativa o algo similar, se ve&iacute;a fuera de lugar. Podr&iacute;a haber recibido una condecoraci&oacute;n m&aacute;s apropiada.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	La investigaci&oacute;n sobre el&nbsp;<a href=\"http://goo.gl/gJsf4r\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\" target=\"_blank\">tejido artesanal</a>&nbsp;no es reciente, el ministerio de cultura viene trabajando en el proyecto desde el a&ntilde;o 2010 y espera lograr un gran avance en la lucha por hacer de esta una actividad de inter&eacute;s para los j&oacute;venes. Uno de los principales problemas que enfrenta la ancestral tradici&oacute;n es la falta de nuevos tejedores.</p>\r\n<p>\r\n	<span style=\"color: rgb(51, 51, 51); font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 20px;\">- See more at: http://www.ecuadorianhands.com/blog-es/2014/06/18/ministerio-de-cultura-implementa-proyecto-de-transmision-de-saberes-del-tejido-del-sombrero-de-toquilla-en-manabi/#sthash.DeumYffa.dpuf</span></p>\r\n','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	El viernes 6 de junio del 2014 se realiz&oacute; un evento en la plaza de la parroquia Picoaz&aacute;, como parte del proyecto de transmisi&oacute;n de saberes del tejido tradicional del&nbsp;<a href=\"http://goo.gl/oaqC8l\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\" target=\"_blank\">sombrero de paja toquilla</a>. El evento fue organizado por la Subsecretar&iacute;a de Patrimonio del Ministerio de Cultura y Patrimonio, con el apoyo de la Direcci&oacute;n Provincial de Manab&iacute;.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<img alt=\"DSC04637\" class=\"alignleft wp-image-3438 size-medium\" height=\"225\" src=\"http://www.ecuadorianhands.com/blog-es/wp-content/uploads/2014/06/DSC04637-300x225.jpg\" style=\"float: left; margin: 0px 10px 10px 0px; display: inline; padding: 0px; height: auto;\" width=\"300\" />Este evento a pesar de su car&aacute;cter festivo gracias a la banda que inaugur&oacute; la ceremonia, tuvo un objetivo m&aacute;s profundo que el de solo entretener, fue la representaci&oacute;n del &ldquo;diagn&oacute;stico econ&oacute;mico y cultural&rdquo; que se est&aacute; haciendo del tejido de la paja toquilla en la regi&oacute;n manabita.&nbsp; No solo se busca un reflejo del n&uacute;mero de personas que dependen de la actividad en la zona, sino tambi&eacute;n del &aacute;mbito de exportaci&oacute;n, la capacidad de producci&oacute;n, cuales son los competidores, entre otros puntos clave.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Como no pod&iacute;a faltar el p&uacute;blico tuvo la dicha de escuchar la famosa canci&oacute;n &ldquo;tejedora manabita&rdquo; y los populares amorfinos tan caracter&iacute;sticos de la regi&oacute;n.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<a href=\"http://www.ecuadorianhands.com/blog-es/wp-content/uploads/2014/06/DSC04642.jpg\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\"><img alt=\"DSC04642\" class=\"alignright wp-image-3439 size-medium\" height=\"225\" src=\"http://www.ecuadorianhands.com/blog-es/wp-content/uploads/2014/06/DSC04642-300x225.jpg\" style=\"border: 0px; float: right; margin: 0px 0px 10px 10px; display: inline; padding: 0px; height: auto;\" width=\"300\" /></a>Si bien la asistencia &nbsp;fue buena, el reconocimiento que se otorg&oacute; a la representante de los tejedores en Picoaz&aacute;, Margarita Garc&iacute;a, no parec&iacute;a el adecuado. Un Bolso de tela en lugar de una placa conmemorativa o algo similar, se ve&iacute;a fuera de lugar. Podr&iacute;a haber recibido una condecoraci&oacute;n m&aacute;s apropiada.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	La investigaci&oacute;n sobre el&nbsp;<a href=\"http://goo.gl/gJsf4r\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\" target=\"_blank\">tejido artesanal</a>&nbsp;no es reciente, el ministerio de cultura viene trabajando en el proyecto desde el a&ntilde;o 2010 y espera lograr un gran avance en la lucha por hacer de esta una actividad de inter&eacute;s para los j&oacute;venes. Uno de los principales problemas que enfrenta la ancestral tradici&oacute;n es la falta de nuevos tejedores.</p>\r\n<p>\r\n	<span style=\"color: rgb(51, 51, 51); font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 20px;\">- See more at: http://www.ecuadorianhands.com/blog-es/2014/06/18/ministerio-de-cultura-implementa-proyecto-de-transmision-de-saberes-del-tejido-del-sombrero-de-toquilla-en-manabi/#sthash.DeumYffa.dpuf</span></p>\r\n',1,1,'2015-05-09 20:20:49',NULL,1,0,1,1,'codeadict','2015-05-09 20:23:13','2015-05-09 20:27:00','','',''),(2,'GANADOR Concurso Elaboracion Joyas Julio 2011 – Tocado Violet por Maria Jose Martinez','ganador-concurso-elaboracion-joyas-julio-2011-toca',2,2,'','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Hola Maria Jose, Felicitaciones por ser la ganadora del concurso. Con 63 votos! Te estaremos enviando tu premio a la brevedad. POr favor comparte con nuestros lectores los dise&ntilde;os que elabores con ellos. Muchas gracias por participar y que tengas lindo dia!</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Abrazos,<br />\r\n	Fabrizio</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	<img alt=\"Tocado Violet Maria Jose Concurso Abalorios Tagua\" class=\"aligncenter\" src=\"http://farm7.static.flickr.com/6125/5916300769_96138d5580.jpg\" style=\"display: block; margin-bottom: 10px; margin-left: auto; margin-right: auto; height: auto;\" /></p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Hola Amigos,</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Aqui tenemos otra concursante para el mes de Julio. Cada dia aprendemos mas sobre de&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">abalorios</a>&nbsp;y todas&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">la bisuteria</a>&nbsp;que podemos realizar con ellos (<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">bijuteria</a>,&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">pulseras</a>,&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">aretes ...</a></p>','h','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Hola Maria Jose, Felicitaciones por ser la ganadora del concurso. Con 63 votos! Te estaremos enviando tu premio a la brevedad. POr favor comparte con nuestros lectores los dise&ntilde;os que elabores con ellos. Muchas gracias por participar y que tengas lindo dia!</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Abrazos,<br />\r\n	Fabrizio</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	<img alt=\"Tocado Violet Maria Jose Concurso Abalorios Tagua\" class=\"aligncenter\" src=\"http://farm7.static.flickr.com/6125/5916300769_96138d5580.jpg\" style=\"display: block; margin-bottom: 10px; margin-left: auto; margin-right: auto; height: auto;\" /></p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Hola Amigos,</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Aqui tenemos otra concursante para el mes de Julio. Cada dia aprendemos mas sobre de&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">abalorios</a>&nbsp;y todas&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">la bisuteria</a>&nbsp;que podemos realizar con ellos (<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">bijuteria</a>,&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">pulseras</a>,&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">aretes</a>, tocados, etc.)</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Nuestra amiga participante se llama Mar&iacute;a Jos&eacute; Mart&iacute;nez Grimaldo, y ella tampoco ha conocido los&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">abalorios de tagua</a>&nbsp;personalmente. En que se diferencian los abalorios de las&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">cuentas de tagua</a>? Alguien puede por favor explicarme? Creo que es lo mismo, o me equivoco? Cuentas para contar? Abalorios para armar&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">bisuteria</a>?</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	He aqui la informacion que nos ha dado de su hermoso diseno:</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Maria Jose:</span><br />\r\n	&ldquo;&hellip;Buenos d&iacute;as amigos.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Tengo la gran alegr&iacute;a de enviaros mi aportaci&oacute;n al concurso del mes de Julio. Es un tocado de ceremonia, que yo he titulado &ldquo;TOCADO VIOLET&rdquo;.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	El nombre, evidentemente, le viene dado por su tono berenjena. Es un tocado fino sobrio y muy elegante. He quedado muy satisfecha con el resultado.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Para hacerlo he utilizado un casquete de rafia, sobre el que he pegado amatistas de diferentes tama&ntilde;os. La lazada tambi&eacute;n es de rafia, del mismo color y en su interior igualmenten lleva otro pu&ntilde;ado de amatistas de diferentes rama&ntilde;os. El tocado se completa con un velo a dos caras, del mismo tono y unas plumas rizadas, que le dan movimiento al conjunto.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	He hecho bastantes fotos para elegir la mejor, siempre bajo vuestra recomendaci&oacute;n de usar un papel blanco como fondo. A pesar de haber seguido las indicaciones el color de obtenido no ha salido blanco, sino en un rom&aacute;ntico color sepia. Es entre todas las que he hecho la que m&aacute;s me ha gustado, precisamente por ese misterioso color. Han aparecido unas sombras que a mi me parece que le dan mucho car&aacute;cter a la foto. Si no os parece bien, me lo hac&eacute;is saber e inmediatamente env&iacute;o otra.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Como yo no entiendo mucho de tama&ntilde;os ni de p&iacute;xeles, ignoro si el que env&iacute;o es el adecuado. Yo tengo un truquito para aumentar o disminuir las fotos y es que las copio y las llevo a un programa que se llama Paint, all&iacute; las amplio o las disminuyo seg&uacute;n me convenga.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Si tengo que facilitar m&aacute;s datos sobre mi o mi trabajo, me lo dec&iacute;s que con mucho gusto lo facilito.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Tengo un &aacute;lbum donde voy insertando &aacute;lbums con algunos de mis trabajos donde tengo desde esculturas a jabones, tocados o collares fotos y dise&ntilde;os y esta es la direcci&oacute;n: http://www.flickr.com/photos/sepisismapepa/</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Espero que os guste mi trabajo y que pueda entrar en el conjurso de este mes de Julio.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Recibir un abrazo</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Mar&iacute;a Jos&eacute; Mart&iacute;nez Grimaldo</p>\r\n<p>\r\n	<span style=\"color: rgb(51, 51, 51); font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 20px;\">- See more at: http://www.ecuadorianhands.com/blog-es/2011/10/01/ganador-concurso-elaboracion-joyas-julio-2011-tocado-violet-por-maria-jose-martinez/#sthash.1ffiYwqi.dpuf</span></p>\r\n','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Hola Maria Jose, Felicitaciones por ser la ganadora del concurso. Con 63 votos! Te estaremos enviando tu premio a la brevedad. POr favor comparte con nuestros lectores los dise&ntilde;os que elabores con ellos. Muchas gracias por participar y que tengas lindo dia!</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Abrazos,<br />\r\n	Fabrizio</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	<img alt=\"Tocado Violet Maria Jose Concurso Abalorios Tagua\" class=\"aligncenter\" src=\"http://farm7.static.flickr.com/6125/5916300769_96138d5580.jpg\" style=\"display: block; margin-bottom: 10px; margin-left: auto; margin-right: auto; height: auto;\" /></p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Hola Amigos,</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Aqui tenemos otra concursante para el mes de Julio. Cada dia aprendemos mas sobre de&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">abalorios</a>&nbsp;y todas&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">la bisuteria</a>&nbsp;que podemos realizar con ellos (<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">bijuteria</a>,&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">pulseras</a>,&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">aretes</a>, tocados, etc.)</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Nuestra amiga participante se llama Mar&iacute;a Jos&eacute; Mart&iacute;nez Grimaldo, y ella tampoco ha conocido los&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">abalorios de tagua</a>&nbsp;personalmente. En que se diferencian los abalorios de las&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">cuentas de tagua</a>? Alguien puede por favor explicarme? Creo que es lo mismo, o me equivoco? Cuentas para contar? Abalorios para armar&nbsp;<a href=\"http://www.ecuadorianhands.com/abalorios-cuentas-c-70.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">bisuteria</a>?</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	He aqui la informacion que nos ha dado de su hermoso diseno:</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Maria Jose:</span><br />\r\n	&ldquo;&hellip;Buenos d&iacute;as amigos.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Tengo la gran alegr&iacute;a de enviaros mi aportaci&oacute;n al concurso del mes de Julio. Es un tocado de ceremonia, que yo he titulado &ldquo;TOCADO VIOLET&rdquo;.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	El nombre, evidentemente, le viene dado por su tono berenjena. Es un tocado fino sobrio y muy elegante. He quedado muy satisfecha con el resultado.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Para hacerlo he utilizado un casquete de rafia, sobre el que he pegado amatistas de diferentes tama&ntilde;os. La lazada tambi&eacute;n es de rafia, del mismo color y en su interior igualmenten lleva otro pu&ntilde;ado de amatistas de diferentes rama&ntilde;os. El tocado se completa con un velo a dos caras, del mismo tono y unas plumas rizadas, que le dan movimiento al conjunto.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	He hecho bastantes fotos para elegir la mejor, siempre bajo vuestra recomendaci&oacute;n de usar un papel blanco como fondo. A pesar de haber seguido las indicaciones el color de obtenido no ha salido blanco, sino en un rom&aacute;ntico color sepia. Es entre todas las que he hecho la que m&aacute;s me ha gustado, precisamente por ese misterioso color. Han aparecido unas sombras que a mi me parece que le dan mucho car&aacute;cter a la foto. Si no os parece bien, me lo hac&eacute;is saber e inmediatamente env&iacute;o otra.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Como yo no entiendo mucho de tama&ntilde;os ni de p&iacute;xeles, ignoro si el que env&iacute;o es el adecuado. Yo tengo un truquito para aumentar o disminuir las fotos y es que las copio y las llevo a un programa que se llama Paint, all&iacute; las amplio o las disminuyo seg&uacute;n me convenga.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Si tengo que facilitar m&aacute;s datos sobre mi o mi trabajo, me lo dec&iacute;s que con mucho gusto lo facilito.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Tengo un &aacute;lbum donde voy insertando &aacute;lbums con algunos de mis trabajos donde tengo desde esculturas a jabones, tocados o collares fotos y dise&ntilde;os y esta es la direcci&oacute;n: http://www.flickr.com/photos/sepisismapepa/</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Espero que os guste mi trabajo y que pueda entrar en el conjurso de este mes de Julio.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Recibir un abrazo</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px;\">\r\n	Mar&iacute;a Jos&eacute; Mart&iacute;nez Grimaldo</p>\r\n<p>\r\n	<span style=\"color: rgb(51, 51, 51); font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 20px;\">- See more at: http://www.ecuadorianhands.com/blog-es/2011/10/01/ganador-concurso-elaboracion-joyas-julio-2011-tocado-violet-por-maria-jose-martinez/#sthash.1ffiYwqi.dpuf</span></p>\r\n',1,1,'2015-05-09 20:29:44',NULL,1,0,1,1,'dairon','2015-05-09 20:31:11','2015-05-09 20:32:36','','',''),(3,'AROMATERAPIA, una alternativa saludable','aromaterapia-una-alternativa-saludable',2,1,'','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	La aromaterapia es un antiguo arte que aporta un uso&nbsp;terap&eacute;utico de los aromas en un tratamiento natural que ayuda a restablecer nuestro equilibrio y armon&iacute;a.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Este arte, practicado hace tiempos remotos por todas las culturas y religiones, en la actualidad se convierte en un remedio para muchas dolencias, sobretodo las que tienen que ver con el estr&eacute;s.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	El modo de actuar de la aromaterapia es trav&eacute;s del olfato armonizando los ...</p>','h','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	La aromaterapia es un antiguo arte que aporta un uso&nbsp;terap&eacute;utico de los aromas en un tratamiento natural que ayuda a restablecer nuestro equilibrio y armon&iacute;a.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Este arte, practicado hace tiempos remotos por todas las culturas y religiones, en la actualidad se convierte en un remedio para muchas dolencias, sobretodo las que tienen que ver con el estr&eacute;s.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	El modo de actuar de la aromaterapia es trav&eacute;s del olfato armonizando los estados ps&iacute;quicos emocionales y espirituales, el sentido del olfato esta relacionado a las emociones, cuando se huele algo se evoca la memoria emocional, se puede relacional las emociones.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	El componente principal para esta pr&aacute;ctica es el uso de&nbsp;<a href=\"http://www.ecuadorianhands.com/aceites-esenciales-inciensos-aceites-esenciales-c-85_154.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">aceites esenciales</a>, mismo que poseen propiedades que estimulan al ser humano conllev&aacute;ndole al bienestar.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Principales aceites esenciales</span><br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Albahaca:</span>&nbsp;se utiliza para el dolor de cabeza y migra&ntilde;as, tambi&eacute;n para la fatiga mental.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Ang&eacute;lica:</span>&nbsp;ayuda a contactarse con lo Divino.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Bergamota:&nbsp;</span>eleva el esp&iacute;ritu, refresca y relaja. Es muy &uacute;til para casos de depresi&oacute;n, ansiedad y tensi&oacute;n.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Canela:</span>&nbsp;es afrodis&iacute;aco y estimulante mental.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Cedro:</span>&nbsp;efecto sedante indicado para el estr&eacute;s.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Cipr&eacute;s:&nbsp;</span>se usa en duelos como en otras etapas de cambio.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Clavo de olor:&nbsp;</span>agotamiento mental para dejar de fumar.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Enebro:&nbsp;</span>act&uacute;a sobre los planos mentales, emocionales y f&iacute;sico, alivia situaciones de confusi&oacute;n y cansancio.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Eucalipto:</span>&nbsp;act&uacute;a en el aparato respiratorio es descongestivo.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Geranio:</span>&nbsp;antidepresivo, relajante y para restaurar y estabilizar emociones.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Jengibre:</span>&nbsp;dolores reum&aacute;ticos y musculares, agotamiento sexual y f&iacute;sico.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Lavanda:</span>&nbsp;es un sedante muy efectivo, se utiliza en problemas de insomnio. Ayuda a balancear estados emocionales como histerias depresiones, calma, relaja.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Lemongrass:&nbsp;</span>se usa en la fatiga mental es un estimulante mental<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Lim&oacute;n:</span>&nbsp;estimulante mental, antis&eacute;ptico, astringente, cicatrizante.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Mandarina:</span>&nbsp;calmante y sedante, brinda alegr&iacute;a. Mejorana: act&uacute;a mejorando estados de soledad, ansiedad.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Menta:</span>&nbsp;estimula el cerebro ayuda a despejar los pensamientos.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Naranja:&nbsp;</span>es antidepresivo y restaura elevando el esp&iacute;ritu. Pino: estimulante del sistema nervioso, brinda energ&iacute;a y bienestar.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<img alt=\"palosanto masaje\" class=\"alignleft\" height=\"240\" src=\"http://farm6.static.flickr.com/5051/5583668599_b6abe4a287_m.jpg\" style=\"float: left; margin: 0px 10px 10px 0px; display: inline; padding: 0px; height: auto;\" width=\"248\" /></p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<a href=\"http://www.ecuadorianhands.com/essential-oils-incense-essential-oils-c-85_154.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\"><span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Palo Santo:</span>&nbsp;propiedades de relajaci&oacute;n, muy usado para calmar dolores de cabeza.</a><br />\r\n	<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Romero:</span>&nbsp;estimula la memoria, la claridad mental, procesos creativos es un protector ps&iacute;quico y un estimulante f&iacute;sico.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Salvia:</span>&nbsp;relajante, armoniza la sexualidad por relajante y distiende la energ&iacute;a sexual. S&aacute;ndalo: propiedades sensuales, meditaci&oacute;n, aquieta los pensamientos, es ansiol&iacute;tico y antidepresivo.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Tomillo:&nbsp;</span>antis&eacute;ptico de vias respiratorias y antitusivo. Es t&oacute;nico y energizante en el nivel f&iacute;sico, mental y emocional, mejora la memoria. Vetiver: es un relajante profundo, balancea energ&iacute;a de grupo puede ser afrodis&iacute;aco.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Ylang-Ylang:</span>&nbsp;antidepresivo y sedante, act&uacute;a sobre dificultades sexuales, por stress y ansiedad, es utilizado en estados de tensi&oacute;n nerviosa, insomnio e hiperactividad.</p>\r\n<p>\r\n	<span style=\"color: rgb(51, 51, 51); font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 20px;\">- See more at: http://www.ecuadorianhands.com/blog-es/2012/06/22/aromaterapia-una-alternativa-saludable/#sthash.ahOYZZig.dpuf</span></p>\r\n','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	La aromaterapia es un antiguo arte que aporta un uso&nbsp;terap&eacute;utico de los aromas en un tratamiento natural que ayuda a restablecer nuestro equilibrio y armon&iacute;a.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Este arte, practicado hace tiempos remotos por todas las culturas y religiones, en la actualidad se convierte en un remedio para muchas dolencias, sobretodo las que tienen que ver con el estr&eacute;s.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	El modo de actuar de la aromaterapia es trav&eacute;s del olfato armonizando los estados ps&iacute;quicos emocionales y espirituales, el sentido del olfato esta relacionado a las emociones, cuando se huele algo se evoca la memoria emocional, se puede relacional las emociones.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	El componente principal para esta pr&aacute;ctica es el uso de&nbsp;<a href=\"http://www.ecuadorianhands.com/aceites-esenciales-inciensos-aceites-esenciales-c-85_154.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\">aceites esenciales</a>, mismo que poseen propiedades que estimulan al ser humano conllev&aacute;ndole al bienestar.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Principales aceites esenciales</span><br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Albahaca:</span>&nbsp;se utiliza para el dolor de cabeza y migra&ntilde;as, tambi&eacute;n para la fatiga mental.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Ang&eacute;lica:</span>&nbsp;ayuda a contactarse con lo Divino.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Bergamota:&nbsp;</span>eleva el esp&iacute;ritu, refresca y relaja. Es muy &uacute;til para casos de depresi&oacute;n, ansiedad y tensi&oacute;n.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Canela:</span>&nbsp;es afrodis&iacute;aco y estimulante mental.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Cedro:</span>&nbsp;efecto sedante indicado para el estr&eacute;s.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Cipr&eacute;s:&nbsp;</span>se usa en duelos como en otras etapas de cambio.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Clavo de olor:&nbsp;</span>agotamiento mental para dejar de fumar.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Enebro:&nbsp;</span>act&uacute;a sobre los planos mentales, emocionales y f&iacute;sico, alivia situaciones de confusi&oacute;n y cansancio.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Eucalipto:</span>&nbsp;act&uacute;a en el aparato respiratorio es descongestivo.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Geranio:</span>&nbsp;antidepresivo, relajante y para restaurar y estabilizar emociones.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Jengibre:</span>&nbsp;dolores reum&aacute;ticos y musculares, agotamiento sexual y f&iacute;sico.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Lavanda:</span>&nbsp;es un sedante muy efectivo, se utiliza en problemas de insomnio. Ayuda a balancear estados emocionales como histerias depresiones, calma, relaja.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Lemongrass:&nbsp;</span>se usa en la fatiga mental es un estimulante mental<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Lim&oacute;n:</span>&nbsp;estimulante mental, antis&eacute;ptico, astringente, cicatrizante.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Mandarina:</span>&nbsp;calmante y sedante, brinda alegr&iacute;a. Mejorana: act&uacute;a mejorando estados de soledad, ansiedad.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Menta:</span>&nbsp;estimula el cerebro ayuda a despejar los pensamientos.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Naranja:&nbsp;</span>es antidepresivo y restaura elevando el esp&iacute;ritu. Pino: estimulante del sistema nervioso, brinda energ&iacute;a y bienestar.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<img alt=\"palosanto masaje\" class=\"alignleft\" height=\"240\" src=\"http://farm6.static.flickr.com/5051/5583668599_b6abe4a287_m.jpg\" style=\"float: left; margin: 0px 10px 10px 0px; display: inline; padding: 0px; height: auto;\" width=\"248\" /></p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	<a href=\"http://www.ecuadorianhands.com/essential-oils-incense-essential-oils-c-85_154.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\"><span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Palo Santo:</span>&nbsp;propiedades de relajaci&oacute;n, muy usado para calmar dolores de cabeza.</a><br />\r\n	<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Romero:</span>&nbsp;estimula la memoria, la claridad mental, procesos creativos es un protector ps&iacute;quico y un estimulante f&iacute;sico.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Salvia:</span>&nbsp;relajante, armoniza la sexualidad por relajante y distiende la energ&iacute;a sexual. S&aacute;ndalo: propiedades sensuales, meditaci&oacute;n, aquieta los pensamientos, es ansiol&iacute;tico y antidepresivo.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Tomillo:&nbsp;</span>antis&eacute;ptico de vias respiratorias y antitusivo. Es t&oacute;nico y energizante en el nivel f&iacute;sico, mental y emocional, mejora la memoria. Vetiver: es un relajante profundo, balancea energ&iacute;a de grupo puede ser afrodis&iacute;aco.<br />\r\n	<span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">Ylang-Ylang:</span>&nbsp;antidepresivo y sedante, act&uacute;a sobre dificultades sexuales, por stress y ansiedad, es utilizado en estados de tensi&oacute;n nerviosa, insomnio e hiperactividad.</p>\r\n<p>\r\n	<span style=\"color: rgb(51, 51, 51); font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 20px;\">- See more at: http://www.ecuadorianhands.com/blog-es/2012/06/22/aromaterapia-una-alternativa-saludable/#sthash.ahOYZZig.dpuf</span></p>\r\n',1,1,'2015-05-07 20:33:37',NULL,1,0,0,1,'','2015-05-09 20:34:47','2015-05-09 20:34:47','','',''),(4,'Hidromiel, la bebida de los Dioses','hidromiel-la-bebida-de-los-dioses',2,2,'','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Se considera que es la primera bebida alcoh&oacute;lica que consumi&oacute; el hombre y que es precursora de la&nbsp;<a href=\"http://www.ecuadorianhands.com/cerveza-artesanal-umina-6pack-330cc-p-1161.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\" title=\"Cerveza Artesanal Umiña\">cerveza</a>.&nbsp; La hidromiel se consigue gracias a la fermentaci&oacute;n de una mezcla de agua y miel y alcanza una graduaci&oacute;n alcoh&oacute;lica cercana a los 13&deg;.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Esta bebida es popular sobretodo debido a que era el &uacute;nico alimento del Dios n&oacute;rdico Odin que gobernaba el&nbsp;Valhalla, un enorme sal&oacute;n donde los muertos ...</p>','h','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Se considera que es la primera bebida alcoh&oacute;lica que consumi&oacute; el hombre y que es precursora de la&nbsp;<a href=\"http://www.ecuadorianhands.com/cerveza-artesanal-umina-6pack-330cc-p-1161.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\" title=\"Cerveza Artesanal Umiña\">cerveza</a>.&nbsp; La hidromiel se consigue gracias a la fermentaci&oacute;n de una mezcla de agua y miel y alcanza una graduaci&oacute;n alcoh&oacute;lica cercana a los 13&deg;.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Esta bebida es popular sobretodo debido a que era el &uacute;nico alimento del Dios n&oacute;rdico Odin que gobernaba el&nbsp;Valhalla, un enorme sal&oacute;n donde los muertos en batalla resid&iacute;an tomando la hidromiel y descansando a la espera de la batalla del Ragnarok o fin del mundo.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Era considerada la bebida de los Dioses en la mitolog&iacute;a n&oacute;rdica y era muy popular sobretodo entre los vikingos, debido a que el clima en el que viv&iacute;an no era propicio para la cosecha de uvas destinadas a la elaboraci&oacute;n de vino.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Hoy en d&iacute;a se sigue fabricando hidromiel y se la puede hacer artesanalmente al igual que la cerveza, de esta manera se logra un sabor &uacute;nico, pero cabe destacar que la cerveza artesanal est&aacute; mas difundida mundialmente debido a que un ligero error en el proceso de fabricaci&oacute;n de la hidromiel la transforma en una bebida con un sabor terriblemente desagradable, hay que tener mucho cuidado en su preparaci&oacute;n.</p>\r\n<div class=\"wp-caption alignright\" id=\"attachment_3227\" style=\"border: 1px solid rgb(230, 230, 230); font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px 0px 10px 10px; outline: 0px; padding: 4px 0px 5px; vertical-align: baseline; float: right; text-align: center; color: rgb(51, 51, 51); line-height: 20px; width: 310px; background: rgb(247, 247, 247);\">\r\n	<a href=\"http://www.ecuadorianhands.com/blog-es/wp-content/uploads/2013/10/asgard-thor-movie-2.jpg\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\"><img alt=\"asgard-thor-movie-2\" class=\"size-medium wp-image-3227 \" height=\"127\" src=\"http://www.ecuadorianhands.com/blog-es/wp-content/uploads/2013/10/asgard-thor-movie-2-300x127.jpg\" style=\"border: 0px; margin: 0px 5px 5px; padding: 0px; height: auto;\" width=\"300\" /></a>\r\n	<p class=\"wp-caption-text\" style=\"border: 0px; font-family: inherit; font-size: 11px; font-style: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; line-height: 12px;\">\r\n		Thor en &ldquo;Asgard&rdquo; uno de los nueve reinos dela mitolog&iacute;a n&oacute;rdica en los que se consum&iacute;a hidromiel</p>\r\n</div>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	En la actualidad la mitolog&iacute;a n&oacute;rdica est&aacute; tomando popularidad nuevamente gracias a las pel&iacute;culas &ldquo;Thor&rdquo;, &ldquo;Los Vengadores&rdquo; y &ldquo;Thor: The Dark World&rdquo; &nbsp;que se estrena este 8 de noviembre, en las que aparece el Dios n&oacute;rdico del Trueno &ldquo;Thor&rdquo; y el de las travesuras &ldquo;Loki&rdquo;. Es un buen momento para probar la hidromiel si nunca lo ha hecho o una buena&nbsp;<a href=\"http://www.ecuadorianhands.com/craft-beer-c-195.html?language=es\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\" title=\"Cerveza Artesanal Umiña\"><span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">cerveza artesanal</span></a>&nbsp;y comparar la&nbsp; diferencia de sabores, puede ser toda una nueva experiencia.</p>\r\n<p>\r\n	<span style=\"color: rgb(51, 51, 51); font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 20px;\">- See more at: http://www.ecuadorianhands.com/blog-es/2013/10/07/hidromiel-la-bebida-de-los-dioses/#sthash.aIGqkWd0.dpuf</span></p>\r\n','<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Se considera que es la primera bebida alcoh&oacute;lica que consumi&oacute; el hombre y que es precursora de la&nbsp;<a href=\"http://www.ecuadorianhands.com/cerveza-artesanal-umina-6pack-330cc-p-1161.html\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\" title=\"Cerveza Artesanal Umiña\">cerveza</a>.&nbsp; La hidromiel se consigue gracias a la fermentaci&oacute;n de una mezcla de agua y miel y alcanza una graduaci&oacute;n alcoh&oacute;lica cercana a los 13&deg;.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Esta bebida es popular sobretodo debido a que era el &uacute;nico alimento del Dios n&oacute;rdico Odin que gobernaba el&nbsp;Valhalla, un enorme sal&oacute;n donde los muertos en batalla resid&iacute;an tomando la hidromiel y descansando a la espera de la batalla del Ragnarok o fin del mundo.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Era considerada la bebida de los Dioses en la mitolog&iacute;a n&oacute;rdica y era muy popular sobretodo entre los vikingos, debido a que el clima en el que viv&iacute;an no era propicio para la cosecha de uvas destinadas a la elaboraci&oacute;n de vino.</p>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	Hoy en d&iacute;a se sigue fabricando hidromiel y se la puede hacer artesanalmente al igual que la cerveza, de esta manera se logra un sabor &uacute;nico, pero cabe destacar que la cerveza artesanal est&aacute; mas difundida mundialmente debido a que un ligero error en el proceso de fabricaci&oacute;n de la hidromiel la transforma en una bebida con un sabor terriblemente desagradable, hay que tener mucho cuidado en su preparaci&oacute;n.</p>\r\n<div class=\"wp-caption alignright\" id=\"attachment_3227\" style=\"border: 1px solid rgb(230, 230, 230); font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px 0px 10px 10px; outline: 0px; padding: 4px 0px 5px; vertical-align: baseline; float: right; text-align: center; color: rgb(51, 51, 51); line-height: 20px; width: 310px; background: rgb(247, 247, 247);\">\r\n	<a href=\"http://www.ecuadorianhands.com/blog-es/wp-content/uploads/2013/10/asgard-thor-movie-2.jpg\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\"><img alt=\"asgard-thor-movie-2\" class=\"size-medium wp-image-3227 \" height=\"127\" src=\"http://www.ecuadorianhands.com/blog-es/wp-content/uploads/2013/10/asgard-thor-movie-2-300x127.jpg\" style=\"border: 0px; margin: 0px 5px 5px; padding: 0px; height: auto;\" width=\"300\" /></a>\r\n	<p class=\"wp-caption-text\" style=\"border: 0px; font-family: inherit; font-size: 11px; font-style: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; line-height: 12px;\">\r\n		Thor en &ldquo;Asgard&rdquo; uno de los nueve reinos dela mitolog&iacute;a n&oacute;rdica en los que se consum&iacute;a hidromiel</p>\r\n</div>\r\n<p style=\"border: 0px; font-family: Arial, Helvetica, sans-serif; font-size: 12px; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; color: rgb(51, 51, 51); line-height: 20px; text-align: justify;\">\r\n	En la actualidad la mitolog&iacute;a n&oacute;rdica est&aacute; tomando popularidad nuevamente gracias a las pel&iacute;culas &ldquo;Thor&rdquo;, &ldquo;Los Vengadores&rdquo; y &ldquo;Thor: The Dark World&rdquo; &nbsp;que se estrena este 8 de noviembre, en las que aparece el Dios n&oacute;rdico del Trueno &ldquo;Thor&rdquo; y el de las travesuras &ldquo;Loki&rdquo;. Es un buen momento para probar la hidromiel si nunca lo ha hecho o una buena&nbsp;<a href=\"http://www.ecuadorianhands.com/craft-beer-c-195.html?language=es\" style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline; text-decoration: none; color: rgb(0, 136, 0);\" title=\"Cerveza Artesanal Umiña\"><span style=\"border: 0px; font-family: inherit; font-size: 12px; font-style: inherit; font-weight: inherit; margin: 0px; outline: 0px; padding: 0px; vertical-align: baseline;\">cerveza artesanal</span></a>&nbsp;y comparar la&nbsp; diferencia de sabores, puede ser toda una nueva experiencia.</p>\r\n<p>\r\n	<span style=\"color: rgb(51, 51, 51); font-family: Arial, Helvetica, sans-serif; font-size: 12px; line-height: 20px;\">- See more at: http://www.ecuadorianhands.com/blog-es/2013/10/07/hidromiel-la-bebida-de-los-dioses/#sthash.aIGqkWd0.dpuf</span></p>\r\n',2,1,'2015-05-06 20:36:13',NULL,1,0,0,1,'','2015-05-09 20:37:38','2015-05-09 20:37:49','','','');
/*!40000 ALTER TABLE `articles_article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_article_followup_for`
--

DROP TABLE IF EXISTS `articles_article_followup_for`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_article_followup_for` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_article_id` int(11) NOT NULL,
  `to_article_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `articles_article_followup_from_article_id_48ae772720da3481_uniq` (`from_article_id`,`to_article_id`),
  KEY `articles_article_followup_for_55dc30a7` (`from_article_id`),
  KEY `articles_article_followup_for_4ae5b0ca` (`to_article_id`),
  CONSTRAINT `to_article_id_refs_id_1bf7090e87599599` FOREIGN KEY (`to_article_id`) REFERENCES `articles_article` (`id`),
  CONSTRAINT `from_article_id_refs_id_1bf7090e87599599` FOREIGN KEY (`from_article_id`) REFERENCES `articles_article` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_article_followup_for`
--

LOCK TABLES `articles_article_followup_for` WRITE;
/*!40000 ALTER TABLE `articles_article_followup_for` DISABLE KEYS */;
/*!40000 ALTER TABLE `articles_article_followup_for` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_article_related_articles`
--

DROP TABLE IF EXISTS `articles_article_related_articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_article_related_articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_article_id` int(11) NOT NULL,
  `to_article_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `articles_article_related__from_article_id_242e5577cb2613a2_uniq` (`from_article_id`,`to_article_id`),
  KEY `articles_article_related_articles_55dc30a7` (`from_article_id`),
  KEY `articles_article_related_articles_4ae5b0ca` (`to_article_id`),
  CONSTRAINT `to_article_id_refs_id_4fe177d23bb1e638` FOREIGN KEY (`to_article_id`) REFERENCES `articles_article` (`id`),
  CONSTRAINT `from_article_id_refs_id_4fe177d23bb1e638` FOREIGN KEY (`from_article_id`) REFERENCES `articles_article` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_article_related_articles`
--

LOCK TABLES `articles_article_related_articles` WRITE;
/*!40000 ALTER TABLE `articles_article_related_articles` DISABLE KEYS */;
/*!40000 ALTER TABLE `articles_article_related_articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_article_related_products`
--

DROP TABLE IF EXISTS `articles_article_related_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_article_related_products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `articles_article_related_produ_article_id_37bc3955fa035d1d_uniq` (`article_id`,`product_id`),
  KEY `articles_article_related_products_30525a19` (`article_id`),
  KEY `articles_article_related_products_bb420c12` (`product_id`),
  CONSTRAINT `product_id_refs_id_704ffbf88a34023` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`),
  CONSTRAINT `article_id_refs_id_5f761a0fbcb8f8d3` FOREIGN KEY (`article_id`) REFERENCES `articles_article` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_article_related_products`
--

LOCK TABLES `articles_article_related_products` WRITE;
/*!40000 ALTER TABLE `articles_article_related_products` DISABLE KEYS */;
/*!40000 ALTER TABLE `articles_article_related_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_article_tags`
--

DROP TABLE IF EXISTS `articles_article_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_article_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `articles_article_tags_article_id_5919f2cbef69a9dd_uniq` (`article_id`,`tag_id`),
  KEY `articles_article_tags_30525a19` (`article_id`),
  KEY `articles_article_tags_3747b463` (`tag_id`),
  CONSTRAINT `tag_id_refs_id_44e3b8e865127384` FOREIGN KEY (`tag_id`) REFERENCES `articles_tag` (`id`),
  CONSTRAINT `article_id_refs_id_6d7bc685fd7e477a` FOREIGN KEY (`article_id`) REFERENCES `articles_article` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_article_tags`
--

LOCK TABLES `articles_article_tags` WRITE;
/*!40000 ALTER TABLE `articles_article_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `articles_article_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_articlestatus`
--

DROP TABLE IF EXISTS `articles_articlestatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_articlestatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `ordering` int(11) NOT NULL DEFAULT '0',
  `is_live` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_articlestatus`
--

LOCK TABLES `articles_articlestatus` WRITE;
/*!40000 ALTER TABLE `articles_articlestatus` DISABLE KEYS */;
INSERT INTO `articles_articlestatus` VALUES (1,'Draft',0,0),(2,'Finished',1,1),(3,'Live',0,1);
/*!40000 ALTER TABLE `articles_articlestatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_attachment`
--

DROP TABLE IF EXISTS `articles_attachment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_attachment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) NOT NULL,
  `attachment` varchar(255) NOT NULL,
  `caption` varchar(255) NOT NULL,
  `is_featured` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `articles_attachment_30525a19` (`article_id`),
  CONSTRAINT `article_id_refs_id_7f652d00bbffbc2d` FOREIGN KEY (`article_id`) REFERENCES `articles_article` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_attachment`
--

LOCK TABLES `articles_attachment` WRITE;
/*!40000 ALTER TABLE `articles_attachment` DISABLE KEYS */;
INSERT INTO `articles_attachment` VALUES (1,1,'attach/2015/ministerio-de-cultura-implementa-proyecto-de-trans/DSC04612-1024x768.jpg','Sombrero Panama Hat',1),(2,2,'attach/2015/ganador-concurso-elaboracion-joyas-julio-2011-toca/5916300769_96138d5580.jpg','Avalorios de tagua',1),(3,3,'attach/2015/aromaterapia-una-alternativa-saludable/7409221388_a05157b915_m.jpg','Aromaterapia',1),(4,4,'attach/2015/hidromiel-la-bebida-de-los-dioses/220px-Sima.jpg','miel',1);
/*!40000 ALTER TABLE `articles_attachment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_blogcategory`
--

DROP TABLE IF EXISTS `articles_blogcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_blogcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `product_category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `articles_blogcategory_a951d5d6` (`slug`),
  KEY `articles_blogcategory_af7958e4` (`product_category_id`),
  CONSTRAINT `product_category_id_refs_id_2fd43a5ecfbf47ba` FOREIGN KEY (`product_category_id`) REFERENCES `marketplace_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_blogcategory`
--

LOCK TABLES `articles_blogcategory` WRITE;
/*!40000 ALTER TABLE `articles_blogcategory` DISABLE KEYS */;
INSERT INTO `articles_blogcategory` VALUES (1,'Prendas de Vestir','prendas-de-vestir',2),(2,'Alimentos','alimentos',4);
/*!40000 ALTER TABLE `articles_blogcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles_tag`
--

DROP TABLE IF EXISTS `articles_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `slug` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles_tag`
--

LOCK TABLES `articles_tag` WRITE;
/*!40000 ALTER TABLE `articles_tag` DISABLE KEYS */;
INSERT INTO `articles_tag` VALUES (1,'noticias','noticias'),(2,'ecología','ecologa'),(3,'comunidades','comunidades');
/*!40000 ALTER TABLE `articles_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_a7792de1` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=290 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add flat page',8,'add_flatpage'),(23,'Can change flat page',8,'change_flatpage'),(24,'Can delete flat page',8,'delete_flatpage'),(25,'Can add comment',9,'add_comment'),(26,'Can change comment',9,'change_comment'),(27,'Can delete comment',9,'delete_comment'),(28,'Can moderate comments',9,'can_moderate'),(29,'Can add comment flag',10,'add_commentflag'),(30,'Can change comment flag',10,'change_commentflag'),(31,'Can delete comment flag',10,'delete_commentflag'),(32,'Can add migration history',11,'add_migrationhistory'),(33,'Can change migration history',11,'change_migrationhistory'),(34,'Can delete migration history',11,'delete_migrationhistory'),(35,'Can add todo',12,'add_todo'),(36,'Can change todo',12,'change_todo'),(37,'Can delete todo',12,'delete_todo'),(38,'Can add metadata (Path)',13,'add_metadatapath'),(39,'Can change metadata (Path)',13,'change_metadatapath'),(40,'Can delete metadata (Path)',13,'delete_metadatapath'),(41,'Can add metadata (Model Instance)',14,'add_metadatamodelinstance'),(42,'Can change metadata (Model Instance)',14,'change_metadatamodelinstance'),(43,'Can delete metadata (Model Instance)',14,'delete_metadatamodelinstance'),(44,'Can add metadata (Model)',15,'add_metadatamodel'),(45,'Can change metadata (Model)',15,'change_metadatamodel'),(46,'Can delete metadata (Model)',15,'delete_metadatamodel'),(47,'Can add metadata (View)',16,'add_metadataview'),(48,'Can change metadata (View)',16,'change_metadataview'),(49,'Can delete metadata (View)',16,'delete_metadataview'),(50,'Can add user social auth',17,'add_usersocialauth'),(51,'Can change user social auth',17,'change_usersocialauth'),(52,'Can delete user social auth',17,'delete_usersocialauth'),(53,'Can add nonce',18,'add_nonce'),(54,'Can change nonce',18,'change_nonce'),(55,'Can delete nonce',18,'delete_nonce'),(56,'Can add association',19,'add_association'),(57,'Can change association',19,'change_association'),(58,'Can delete association',19,'delete_association'),(59,'Can add source',20,'add_source'),(60,'Can change source',20,'change_source'),(61,'Can delete source',20,'delete_source'),(62,'Can add thumbnail',21,'add_thumbnail'),(63,'Can change thumbnail',21,'change_thumbnail'),(64,'Can delete thumbnail',21,'delete_thumbnail'),(65,'Can add cron job log',22,'add_cronjoblog'),(66,'Can change cron job log',22,'change_cronjoblog'),(67,'Can delete cron job log',22,'delete_cronjoblog'),(68,'Can add category',23,'add_category'),(69,'Can change category',23,'change_category'),(70,'Can delete category',23,'delete_category'),(71,'Can add cause',24,'add_cause'),(72,'Can change cause',24,'change_cause'),(73,'Can delete cause',24,'delete_cause'),(74,'Can add certificate',25,'add_certificate'),(75,'Can change certificate',25,'change_certificate'),(76,'Can delete certificate',25,'delete_certificate'),(77,'Can add color',26,'add_color'),(78,'Can change color',26,'change_color'),(79,'Can delete color',26,'delete_color'),(80,'Can add ingredient',27,'add_ingredient'),(81,'Can change ingredient',27,'change_ingredient'),(82,'Can delete ingredient',27,'delete_ingredient'),(83,'Can add material',28,'add_material'),(84,'Can change material',28,'change_material'),(85,'Can delete material',28,'delete_material'),(86,'Can add keyword',29,'add_keyword'),(87,'Can change keyword',29,'change_keyword'),(88,'Can delete keyword',29,'delete_keyword'),(89,'Can add occasion',30,'add_occasion'),(90,'Can change occasion',30,'change_occasion'),(91,'Can delete occasion',30,'delete_occasion'),(92,'Can add recipient',31,'add_recipient'),(93,'Can change recipient',31,'change_recipient'),(94,'Can delete recipient',31,'delete_recipient'),(95,'Can add stall category',32,'add_stallcategory'),(96,'Can change stall category',32,'change_stallcategory'),(97,'Can delete stall category',32,'delete_stallcategory'),(98,'Can add stall',33,'add_stall'),(99,'Can change stall',33,'change_stall'),(100,'Can delete stall',33,'delete_stall'),(101,'Can add stall old style phone number',34,'add_stalloldstylephonenumber'),(102,'Can change stall old style phone number',34,'change_stalloldstylephonenumber'),(103,'Can delete stall old style phone number',34,'delete_stalloldstylephonenumber'),(104,'Can add stall video',35,'add_stallvideo'),(105,'Can change stall video',35,'change_stallvideo'),(106,'Can delete stall video',35,'delete_stallvideo'),(107,'Can add price',36,'add_price'),(108,'Can change price',36,'change_price'),(109,'Can delete price',36,'delete_price'),(110,'Can add product',37,'add_product'),(111,'Can change product',37,'change_product'),(112,'Can delete product',37,'delete_product'),(113,'Can add product image',38,'add_productimage'),(114,'Can change product image',38,'change_productimage'),(115,'Can delete product image',38,'delete_productimage'),(116,'Can add shipping profile',39,'add_shippingprofile'),(117,'Can change shipping profile',39,'change_shippingprofile'),(118,'Can delete shipping profile',39,'delete_shippingprofile'),(119,'Can add shipping rule',40,'add_shippingrule'),(120,'Can change shipping rule',40,'change_shippingrule'),(121,'Can delete shipping rule',40,'delete_shippingrule'),(122,'Can add country',41,'add_country'),(123,'Can change country',41,'change_country'),(124,'Can delete country',41,'delete_country'),(125,'Can add suggested certificate',42,'add_suggestedcertificate'),(126,'Can change suggested certificate',42,'change_suggestedcertificate'),(127,'Can delete suggested certificate',42,'delete_suggestedcertificate'),(128,'Can add currency exchange rate',43,'add_currencyexchangerate'),(129,'Can change currency exchange rate',43,'change_currencyexchangerate'),(130,'Can delete currency exchange rate',43,'delete_currencyexchangerate'),(131,'Can add stall status log',44,'add_stallstatuslog'),(132,'Can change stall status log',44,'change_stallstatuslog'),(133,'Can delete stall status log',44,'delete_stallstatuslog'),(134,'Can add Stall Suspension',33,'add_stallsuspendproxy'),(135,'Can change Stall Suspension',33,'change_stallsuspendproxy'),(136,'Can delete Stall Suspension',33,'delete_stallsuspendproxy'),(137,'Can add stall call notes',45,'add_stallcallnotes'),(138,'Can change stall call notes',45,'change_stallcallnotes'),(139,'Can delete stall call notes',45,'delete_stallcallnotes'),(140,'Can add cart',47,'add_cart'),(141,'Can change cart',47,'change_cart'),(142,'Can delete cart',47,'delete_cart'),(143,'Can add cart stall',48,'add_cartstall'),(144,'Can change cart stall',48,'change_cartstall'),(145,'Can delete cart stall',48,'delete_cartstall'),(146,'Can add cart product',49,'add_cartproduct'),(147,'Can change cart product',49,'change_cartproduct'),(148,'Can delete cart product',49,'delete_cartproduct'),(149,'Can add payment attempt',50,'add_paymentattempt'),(150,'Can change payment attempt',50,'change_paymentattempt'),(151,'Can delete payment attempt',50,'delete_paymentattempt'),(152,'Can add order',51,'add_order'),(153,'Can change order',51,'change_order'),(154,'Can delete order',51,'delete_order'),(155,'Can add order feedback',52,'add_orderfeedback'),(156,'Can change order feedback',52,'change_orderfeedback'),(157,'Can delete order feedback',52,'delete_orderfeedback'),(158,'Can add line item',53,'add_lineitem'),(159,'Can change line item',53,'change_lineitem'),(160,'Can delete line item',53,'delete_lineitem'),(161,'Can add refund',54,'add_refund'),(162,'Can change refund',54,'change_refund'),(163,'Can delete refund',54,'delete_refund'),(164,'Can add payment',55,'add_payment'),(165,'Can change payment',55,'change_payment'),(166,'Can delete payment',55,'delete_payment'),(167,'Can add payment return redirect',56,'add_paymentreturnredirect'),(168,'Can change payment return redirect',56,'change_paymentreturnredirect'),(169,'Can delete payment return redirect',56,'delete_paymentreturnredirect'),(170,'Can add user profile',57,'add_userprofile'),(171,'Can change user profile',57,'change_userprofile'),(172,'Can delete user profile',57,'delete_userprofile'),(173,'Can add email notification',58,'add_emailnotification'),(174,'Can change email notification',58,'change_emailnotification'),(175,'Can delete email notification',58,'delete_emailnotification'),(176,'Can add privacy',59,'add_privacy'),(177,'Can change privacy',59,'change_privacy'),(178,'Can delete privacy',59,'delete_privacy'),(179,'Can add shipping address',60,'add_shippingaddress'),(180,'Can change shipping address',60,'change_shippingaddress'),(181,'Can delete shipping address',60,'delete_shippingaddress'),(182,'Can add video type',61,'add_videotype'),(183,'Can change video type',61,'change_videotype'),(184,'Can delete video type',61,'delete_videotype'),(185,'Can add video',62,'add_video'),(186,'Can change video',62,'change_video'),(187,'Can delete video',62,'delete_video'),(188,'Can add love list',63,'add_lovelist'),(189,'Can change love list',63,'change_lovelist'),(190,'Can delete love list',63,'delete_lovelist'),(191,'Can add love list product',64,'add_lovelistproduct'),(192,'Can change love list product',64,'change_lovelistproduct'),(193,'Can delete love list product',64,'delete_lovelistproduct'),(194,'Can add promotion scheduler',65,'add_promotionscheduler'),(195,'Can change promotion scheduler',65,'change_promotionscheduler'),(196,'Can delete promotion scheduler',65,'delete_promotionscheduler'),(197,'Can add Message',66,'add_message'),(198,'Can change Message',66,'change_message'),(199,'Can delete Message',66,'delete_message'),(200,'Can add Thread',67,'add_messagethread'),(201,'Can change Thread',67,'change_messagethread'),(202,'Can delete Thread',67,'delete_messagethread'),(203,'Can add thread user state',68,'add_threaduserstate'),(204,'Can change thread user state',68,'change_threaduserstate'),(205,'Can delete thread user state',68,'delete_threaduserstate'),(206,'Can add blog category',69,'add_blogcategory'),(207,'Can change blog category',69,'change_blogcategory'),(208,'Can delete blog category',69,'delete_blogcategory'),(209,'Can add tag',70,'add_tag'),(210,'Can change tag',70,'change_tag'),(211,'Can delete tag',70,'delete_tag'),(212,'Can add article status',71,'add_articlestatus'),(213,'Can change article status',71,'change_articlestatus'),(214,'Can delete article status',71,'delete_articlestatus'),(215,'Can add article',72,'add_article'),(216,'Can change article',72,'change_article'),(217,'Can delete article',72,'delete_article'),(218,'Can add attachment',73,'add_attachment'),(219,'Can change attachment',73,'change_attachment'),(220,'Can delete attachment',73,'delete_attachment'),(221,'Can add temp image',74,'add_tempimage'),(222,'Can change temp image',74,'change_tempimage'),(223,'Can delete temp image',74,'delete_tempimage'),(224,'Can add banned word',75,'add_bannedword'),(225,'Can change banned word',75,'change_bannedword'),(226,'Can delete banned word',75,'delete_bannedword'),(227,'Can add threaded comment',76,'add_threadedcomment'),(228,'Can change threaded comment',76,'change_threadedcomment'),(229,'Can delete threaded comment',76,'delete_threadedcomment'),(230,'Can add threaded comment flag',77,'add_threadedcommentflag'),(231,'Can change threaded comment flag',77,'change_threadedcommentflag'),(232,'Can delete threaded comment flag',77,'delete_threadedcommentflag'),(233,'Can add mailing list signup',78,'add_mailinglistsignup'),(234,'Can change mailing list signup',78,'change_mailinglistsignup'),(235,'Can delete mailing list signup',78,'delete_mailinglistsignup'),(236,'Can add batch job',79,'add_batchjob'),(237,'Can change batch job',79,'change_batchjob'),(238,'Can delete batch job',79,'delete_batchjob'),(239,'Can add deleted email',80,'add_deletedemail'),(240,'Can change deleted email',80,'change_deletedemail'),(241,'Can delete deleted email',80,'delete_deletedemail'),(242,'Can add user follow',81,'add_userfollow'),(243,'Can change user follow',81,'change_userfollow'),(244,'Can delete user follow',81,'delete_userfollow'),(245,'Can add campaign track',82,'add_campaigntrack'),(246,'Can change campaign track',82,'change_campaigntrack'),(247,'Can delete campaign track',82,'delete_campaigntrack'),(248,'Can add aggregate data',83,'add_aggregatedata'),(249,'Can change aggregate data',83,'change_aggregatedata'),(250,'Can delete aggregate data',83,'delete_aggregatedata'),(251,'Can add lifetime track',84,'add_lifetimetrack'),(252,'Can change lifetime track',84,'change_lifetimetrack'),(253,'Can delete lifetime track',84,'delete_lifetimetrack'),(254,'Can add product form errors',85,'add_productformerrors'),(255,'Can change product form errors',85,'change_productformerrors'),(256,'Can delete product form errors',85,'delete_productformerrors'),(257,'Can add UTM URL for XML Feed',86,'add_placampaign'),(258,'Can change UTM URL for XML Feed',86,'change_placampaign'),(259,'Can delete UTM URL for XML Feed',86,'delete_placampaign'),(260,'Can add curebit site',87,'add_curebitsite'),(261,'Can change curebit site',87,'change_curebitsite'),(262,'Can delete curebit site',87,'delete_curebitsite'),(263,'Can add UTM code for Curebit site',88,'add_utmcode'),(264,'Can change UTM code for Curebit site',88,'change_utmcode'),(265,'Can delete UTM code for Curebit site',88,'delete_utmcode'),(266,'Can add Discount coupon codes',89,'add_discount'),(267,'Can change Discount coupon codes',89,'change_discount'),(268,'Can delete Discount coupon codes',89,'delete_discount'),(269,'Can add free shipping',90,'add_freeshipping'),(270,'Can change free shipping',90,'change_freeshipping'),(271,'Can delete free shipping',90,'delete_freeshipping'),(272,'Can add product ad words',91,'add_productadwords'),(273,'Can change product ad words',91,'change_productadwords'),(274,'Can delete product ad words',91,'delete_productadwords'),(275,'Can add active campaign id',92,'add_activecampaignid'),(276,'Can change active campaign id',92,'change_activecampaignid'),(277,'Can delete active campaign id',92,'delete_activecampaignid'),(278,'Can add old category',93,'add_oldcategory'),(279,'Can change old category',93,'change_oldcategory'),(280,'Can delete old category',93,'delete_oldcategory'),(281,'Can add temp product',94,'add_tempproduct'),(282,'Can change temp product',94,'change_tempproduct'),(283,'Can delete temp product',94,'delete_tempproduct'),(284,'Can add follow',95,'add_follow'),(285,'Can change follow',95,'change_follow'),(286,'Can delete follow',95,'delete_follow'),(287,'Can add action',96,'add_action'),(288,'Can change action',96,'change_action'),(289,'Can delete action',96,'delete_action');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'codeadict','','','dairon.medina@gmail.com','pbkdf2_sha256$10000$tGEQ0cZSkKCp$ye4dwE1YN62dmJvXCMdu0s/UxvE38V2++61/KG7spNw=',0,1,0,'2015-04-17 17:55:19','2015-04-17 17:55:19'),(2,'dairon','','','dairon.medina@gmail.com','pbkdf2_sha256$10000$hYdJRkwne9IW$Hf7/TIPhTmO4mvpGiHEUcHZH8RIWytAEBMsEHkwc+8Q=',1,1,1,'2015-05-09 16:38:44','2015-05-09 15:51:29');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_f0ee9890` (`group_id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_67e79cb` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discounts_curebitsite`
--

DROP TABLE IF EXISTS `discounts_curebitsite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discounts_curebitsite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slug` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts_curebitsite`
--

LOCK TABLES `discounts_curebitsite` WRITE;
/*!40000 ALTER TABLE `discounts_curebitsite` DISABLE KEYS */;
/*!40000 ALTER TABLE `discounts_curebitsite` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discounts_discount`
--

DROP TABLE IF EXISTS `discounts_discount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discounts_discount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(100) NOT NULL,
  `percent_discount` smallint(6) NOT NULL DEFAULT '0',
  `price_discount` decimal(5,2) NOT NULL DEFAULT '0.00',
  `expires` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts_discount`
--

LOCK TABLES `discounts_discount` WRITE;
/*!40000 ALTER TABLE `discounts_discount` DISABLE KEYS */;
/*!40000 ALTER TABLE `discounts_discount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discounts_freeshipping`
--

DROP TABLE IF EXISTS `discounts_freeshipping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discounts_freeshipping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) NOT NULL,
  `percent_discount` decimal(5,2) NOT NULL DEFAULT '10.00',
  `date_start` datetime DEFAULT NULL,
  `date_end` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts_freeshipping`
--

LOCK TABLES `discounts_freeshipping` WRITE;
/*!40000 ALTER TABLE `discounts_freeshipping` DISABLE KEYS */;
/*!40000 ALTER TABLE `discounts_freeshipping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discounts_freeshipping_shipping_to`
--

DROP TABLE IF EXISTS `discounts_freeshipping_shipping_to`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discounts_freeshipping_shipping_to` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `freeshipping_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `discounts_freeshipping_sh_freeshipping_id_583dd6a96d2f7773_uniq` (`freeshipping_id`,`country_id`),
  KEY `discounts_freeshipping_shipping_to_66fd12a4` (`freeshipping_id`),
  KEY `discounts_freeshipping_shipping_to_534dd89` (`country_id`),
  CONSTRAINT `country_id_refs_id_2482cf33f59bd522` FOREIGN KEY (`country_id`) REFERENCES `marketplace_country` (`id`),
  CONSTRAINT `freeshipping_id_refs_id_5ed9ac3fc19e9d66` FOREIGN KEY (`freeshipping_id`) REFERENCES `discounts_freeshipping` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts_freeshipping_shipping_to`
--

LOCK TABLES `discounts_freeshipping_shipping_to` WRITE;
/*!40000 ALTER TABLE `discounts_freeshipping_shipping_to` DISABLE KEYS */;
/*!40000 ALTER TABLE `discounts_freeshipping_shipping_to` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discounts_placampaign`
--

DROP TABLE IF EXISTS `discounts_placampaign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discounts_placampaign` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `utm_source` varchar(127) NOT NULL,
  `utm_medium` varchar(127) NOT NULL,
  `utm_campaign` varchar(127) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts_placampaign`
--

LOCK TABLES `discounts_placampaign` WRITE;
/*!40000 ALTER TABLE `discounts_placampaign` DISABLE KEYS */;
/*!40000 ALTER TABLE `discounts_placampaign` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discounts_placampaign_countries`
--

DROP TABLE IF EXISTS `discounts_placampaign_countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discounts_placampaign_countries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `placampaign_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `discounts_placampaign_count_placampaign_id_e9ef724e227baf1_uniq` (`placampaign_id`,`country_id`),
  KEY `discounts_placampaign_countries_584ee6e4` (`placampaign_id`),
  KEY `discounts_placampaign_countries_534dd89` (`country_id`),
  CONSTRAINT `country_id_refs_id_6a4967caf5564642` FOREIGN KEY (`country_id`) REFERENCES `marketplace_country` (`id`),
  CONSTRAINT `placampaign_id_refs_id_71ad099aa594d65c` FOREIGN KEY (`placampaign_id`) REFERENCES `discounts_placampaign` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts_placampaign_countries`
--

LOCK TABLES `discounts_placampaign_countries` WRITE;
/*!40000 ALTER TABLE `discounts_placampaign_countries` DISABLE KEYS */;
/*!40000 ALTER TABLE `discounts_placampaign_countries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discounts_placampaign_products`
--

DROP TABLE IF EXISTS `discounts_placampaign_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discounts_placampaign_products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `placampaign_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `discounts_placampaign_prod_placampaign_id_3d601720f9487c6d_uniq` (`placampaign_id`,`product_id`),
  KEY `discounts_placampaign_products_584ee6e4` (`placampaign_id`),
  KEY `discounts_placampaign_products_bb420c12` (`product_id`),
  CONSTRAINT `product_id_refs_id_1fac9a048bd4958a` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`),
  CONSTRAINT `placampaign_id_refs_id_7bcae90caea61bbd` FOREIGN KEY (`placampaign_id`) REFERENCES `discounts_placampaign` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts_placampaign_products`
--

LOCK TABLES `discounts_placampaign_products` WRITE;
/*!40000 ALTER TABLE `discounts_placampaign_products` DISABLE KEYS */;
/*!40000 ALTER TABLE `discounts_placampaign_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discounts_utmcode`
--

DROP TABLE IF EXISTS `discounts_utmcode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discounts_utmcode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(127) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `discounts_utmcode_6223029` (`site_id`),
  CONSTRAINT `site_id_refs_id_561883f3c421d045` FOREIGN KEY (`site_id`) REFERENCES `discounts_curebitsite` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discounts_utmcode`
--

LOCK TABLES `discounts_utmcode` WRITE;
/*!40000 ALTER TABLE `discounts_utmcode` DISABLE KEYS */;
/*!40000 ALTER TABLE `discounts_utmcode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_type_id_refs_id_288599e6` (`content_type_id`),
  KEY `user_id_refs_id_c8665aa` (`user_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2015-05-09 17:56:15',2,71,'3','Live (live)',1,''),(2,'2015-05-09 19:53:17',2,8,'1','/work-for-us/ -- Jobs',1,''),(3,'2015-05-09 19:56:37',2,26,'1','Green',1,''),(4,'2015-05-09 19:56:52',2,26,'2','Red',1,''),(5,'2015-05-09 19:57:17',2,32,'1','Joyería',1,''),(6,'2015-05-09 19:57:33',2,32,'2','Alimentos',1,''),(7,'2015-05-09 19:57:41',2,32,'3','Fashion',1,''),(8,'2015-05-09 19:57:48',2,32,'4','Diseño',1,''),(9,'2015-05-09 19:57:57',2,32,'5','Decoración',1,''),(10,'2015-05-09 19:59:06',2,33,'1','dairon:tagua-heaven',2,'Changed chat_stall_uri, chat_operator_uri and is_in_video_beta.'),(11,'2015-05-09 20:01:02',2,61,'1','VideoType object',1,''),(12,'2015-05-09 20:02:48',2,61,'1','VideoType object',2,'Changed time_limit.'),(13,'2015-05-09 20:05:44',2,35,'1','tagua-heaven: Our products',1,''),(14,'2015-05-09 20:06:06',2,29,'1','tagua',1,''),(15,'2015-05-09 20:06:12',2,29,'2','andes',1,''),(16,'2015-05-09 20:06:16',2,29,'3','ecuador',1,''),(17,'2015-05-09 20:06:22',2,29,'4','jewlery',1,''),(18,'2015-05-09 20:07:46',2,28,'1','tagua',1,''),(19,'2015-05-09 20:07:53',2,28,'2','Madera',1,''),(20,'2015-05-09 20:07:58',2,28,'3','Piedra',1,''),(21,'2015-05-09 20:08:05',2,28,'1','Tagua',2,'Changed title.'),(22,'2015-05-09 20:08:09',2,28,'4','Tela',1,''),(23,'2015-05-09 20:08:48',2,27,'1','Tagua',1,''),(24,'2015-05-09 20:08:52',2,27,'2','Agua',1,''),(25,'2015-05-09 20:09:00',2,27,'3','Madera',1,''),(26,'2015-05-09 20:09:15',2,30,'1','Salidas',1,''),(27,'2015-05-09 20:09:20',2,30,'2','Formal',1,''),(28,'2015-05-09 20:09:26',2,30,'3','Para Comer',1,''),(29,'2015-05-09 20:12:08',2,24,'1','Smart Products',1,''),(30,'2015-05-09 20:12:17',2,25,'1','Certificado Producto Smart',1,''),(31,'2015-05-09 20:14:35',2,35,'1','tagua-heaven: Our products',2,'Changed is_welcome.'),(32,'2015-05-09 20:15:35',2,23,'1','Joyería',1,''),(33,'2015-05-09 20:15:46',2,23,'2','Ropa',1,''),(34,'2015-05-09 20:16:07',2,23,'3','Hogar y Decoración',1,''),(35,'2015-05-09 20:17:14',2,39,'1','Envío USA',1,''),(36,'2015-05-09 20:17:39',2,40,'1','ShippingRule object',1,''),(37,'2015-05-09 20:22:28',2,69,'1','Prendas de Vestir',1,''),(38,'2015-05-09 20:23:13',2,72,'1','Ministerio de Cultura implementa proyecto de transmisión de saberes del tejido del sombrero de paja ',1,''),(39,'2015-05-09 20:23:43',2,72,'1','Ministerio de Cultura implementa proyecto de transmisión de saberes del tejido del sombrero de paja ',2,'Changed status.'),(40,'2015-05-09 20:27:00',2,72,'1','Ministerio de Cultura implementa proyecto de transmisión de saberes del tejido del sombrero de paja ',2,'Changed status and use_addthis_button.'),(41,'2015-05-09 20:27:21',2,70,'1','noticias',1,''),(42,'2015-05-09 20:27:27',2,70,'2','ecología',1,''),(43,'2015-05-09 20:27:32',2,70,'3','comunidades',1,''),(44,'2015-05-09 20:31:11',2,72,'2','GANADOR Concurso Elaboracion Joyas Julio 2011 – Tocado Violet por Maria Jose Martinez',1,''),(45,'2015-05-09 20:32:36',2,72,'2','GANADOR Concurso Elaboracion Joyas Julio 2011 – Tocado Violet por Maria Jose Martinez',2,'Changed use_addthis_button.'),(46,'2015-05-09 20:34:47',2,72,'3','AROMATERAPIA, una alternativa saludable',1,''),(47,'2015-05-09 20:37:05',2,23,'4','Comestibles',1,''),(48,'2015-05-09 20:37:07',2,69,'2','Alimentos',1,''),(49,'2015-05-09 20:37:38',2,72,'4','Hidromiel, la bebida de los Dioses',1,''),(50,'2015-05-09 20:37:49',2,72,'4','Hidromiel, la bebida de los Dioses',2,'Changed status.'),(51,'2015-05-09 20:46:51',2,23,'1','Joyeria',2,'Changed name.'),(52,'2015-05-09 20:47:07',2,31,'1','Mujeres',1,''),(53,'2015-05-09 20:47:12',2,31,'2','Chicas',1,''),(54,'2015-05-09 20:52:05',2,37,'1','tagua-heaven:OJALILLO COLLAR ABALORIOS TAGUA (45 UNIDADES)',1,''),(55,'2015-05-09 20:55:45',2,37,'1','tagua-heaven:OJALILLO COLLAR ABALORIOS TAGUA (45 UNIDADES)',2,'Changed stock.'),(56,'2015-05-09 20:57:57',2,63,'1','Cosas que me gustan',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_comment_flags`
--

DROP TABLE IF EXISTS `django_comment_flags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_comment_flags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `comment_id` int(11) NOT NULL,
  `flag` varchar(30) NOT NULL,
  `flag_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`comment_id`,`flag`),
  KEY `comment_id_refs_id_373a05f7` (`comment_id`),
  CONSTRAINT `comment_id_refs_id_373a05f7` FOREIGN KEY (`comment_id`) REFERENCES `django_comments` (`id`),
  CONSTRAINT `user_id_refs_id_603c4dcb` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_comment_flags`
--

LOCK TABLES `django_comment_flags` WRITE;
/*!40000 ALTER TABLE `django_comment_flags` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_comment_flags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_comments`
--

DROP TABLE IF EXISTS `django_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content_type_id` int(11) NOT NULL,
  `object_pk` longtext NOT NULL,
  `site_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_email` varchar(75) NOT NULL,
  `user_url` varchar(200) NOT NULL,
  `comment` longtext NOT NULL,
  `submit_date` datetime NOT NULL,
  `ip_address` char(15) DEFAULT NULL,
  `is_public` tinyint(1) NOT NULL,
  `is_removed` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `content_type_id_refs_id_f2a7975b` (`content_type_id`),
  KEY `user_id_refs_id_81622011` (`user_id`),
  KEY `site_id_refs_id_8db720f8` (`site_id`),
  CONSTRAINT `content_type_id_refs_id_f2a7975b` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `site_id_refs_id_8db720f8` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`),
  CONSTRAINT `user_id_refs_id_81622011` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_comments`
--

LOCK TABLES `django_comments` WRITE;
/*!40000 ALTER TABLE `django_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'flat page','flatpages','flatpage'),(9,'comment','comments','comment'),(10,'comment flag','comments','commentflag'),(11,'migration history','south','migrationhistory'),(12,'todo','todos','todo'),(13,'metadata (Path)','seo','metadatapath'),(14,'metadata (Model Instance)','seo','metadatamodelinstance'),(15,'metadata (Model)','seo','metadatamodel'),(16,'metadata (View)','seo','metadataview'),(17,'user social auth','social_auth','usersocialauth'),(18,'nonce','social_auth','nonce'),(19,'association','social_auth','association'),(20,'source','easy_thumbnails','source'),(21,'thumbnail','easy_thumbnails','thumbnail'),(22,'cron job log','django_cron','cronjoblog'),(23,'category','marketplace','category'),(24,'cause','marketplace','cause'),(25,'certificate','marketplace','certificate'),(26,'color','marketplace','color'),(27,'ingredient','marketplace','ingredient'),(28,'material','marketplace','material'),(29,'keyword','marketplace','keyword'),(30,'occasion','marketplace','occasion'),(31,'recipient','marketplace','recipient'),(32,'stall category','marketplace','stallcategory'),(33,'stall','marketplace','stall'),(34,'stall old style phone number','marketplace','stalloldstylephonenumber'),(35,'stall video','marketplace','stallvideo'),(36,'price','marketplace','price'),(37,'product','marketplace','product'),(38,'product image','marketplace','productimage'),(39,'shipping profile','marketplace','shippingprofile'),(40,'shipping rule','marketplace','shippingrule'),(41,'country','marketplace','country'),(42,'suggested certificate','marketplace','suggestedcertificate'),(43,'currency exchange rate','marketplace','currencyexchangerate'),(44,'stall status log','marketplace','stallstatuslog'),(45,'stall call notes','marketplace','stallcallnotes'),(46,'Stall Suspension','marketplace','stallsuspendproxy'),(47,'cart','purchase','cart'),(48,'cart stall','purchase','cartstall'),(49,'cart product','purchase','cartproduct'),(50,'payment attempt','purchase','paymentattempt'),(51,'order','purchase','order'),(52,'order feedback','purchase','orderfeedback'),(53,'line item','purchase','lineitem'),(54,'refund','purchase','refund'),(55,'payment','purchase','payment'),(56,'payment return redirect','purchase','paymentreturnredirect'),(57,'user profile','accounts','userprofile'),(58,'email notification','accounts','emailnotification'),(59,'privacy','accounts','privacy'),(60,'shipping address','accounts','shippingaddress'),(61,'video type','accounts','videotype'),(62,'video','accounts','video'),(63,'love list','lovelists','lovelist'),(64,'love list product','lovelists','lovelistproduct'),(65,'promotion scheduler','lovelists','promotionscheduler'),(66,'Message','messaging','message'),(67,'Thread','messaging','messagethread'),(68,'thread user state','messaging','threaduserstate'),(69,'blog category','articles','blogcategory'),(70,'tag','articles','tag'),(71,'article status','articles','articlestatus'),(72,'article','articles','article'),(73,'attachment','articles','attachment'),(74,'temp image','image_crop','tempimage'),(75,'banned word','spamish','bannedword'),(76,'threaded comment','threadedcomments','threadedcomment'),(77,'threaded comment flag','threadedcomments','threadedcommentflag'),(78,'mailing list signup','mailing_lists','mailinglistsignup'),(79,'batch job','mailing_lists','batchjob'),(80,'deleted email','mailing_lists','deletedemail'),(81,'user follow','social_network','userfollow'),(82,'campaign track','analytics','campaigntrack'),(83,'aggregate data','analytics','aggregatedata'),(84,'lifetime track','analytics','lifetimetrack'),(85,'product form errors','analytics','productformerrors'),(86,'UTM URL for XML Feed','discounts','placampaign'),(87,'curebit site','discounts','curebitsite'),(88,'UTM code for Curebit site','discounts','utmcode'),(89,'Discount coupon codes','discounts','discount'),(90,'free shipping','discounts','freeshipping'),(91,'product ad words','sem','productadwords'),(92,'active campaign id','sem','activecampaignid'),(93,'old category','product_tmp','oldcategory'),(94,'temp product','product_tmp','tempproduct'),(95,'follow','actstream','follow'),(96,'action','actstream','action');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_cron_cronjoblog`
--

DROP TABLE IF EXISTS `django_cron_cronjoblog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_cron_cronjoblog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(64) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `is_success` tinyint(1) NOT NULL DEFAULT '0',
  `message` longtext NOT NULL,
  `ran_at_time` time,
  PRIMARY KEY (`id`),
  KEY `django_cron_cronjoblog_65da3d2c` (`code`),
  KEY `django_cron_cronjoblog_effd9ef` (`start_time`),
  KEY `django_cron_cronjoblog_e89eac35` (`ran_at_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_cron_cronjoblog`
--

LOCK TABLES `django_cron_cronjoblog` WRITE;
/*!40000 ALTER TABLE `django_cron_cronjoblog` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_cron_cronjoblog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_flatpage`
--

DROP TABLE IF EXISTS `django_flatpage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_flatpage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `enable_comments` tinyint(1) NOT NULL,
  `template_name` varchar(70) NOT NULL,
  `registration_required` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_flatpage`
--

LOCK TABLES `django_flatpage` WRITE;
/*!40000 ALTER TABLE `django_flatpage` DISABLE KEYS */;
INSERT INTO `django_flatpage` VALUES (1,'/work-for-us/','Jobs','Jobshere',0,'',0);
/*!40000 ALTER TABLE `django_flatpage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_flatpage_sites`
--

DROP TABLE IF EXISTS `django_flatpage_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_flatpage_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flatpage_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `flatpage_id` (`flatpage_id`,`site_id`),
  KEY `site_id_refs_id_4e3eeb57` (`site_id`),
  CONSTRAINT `flatpage_id_refs_id_c0e84f5a` FOREIGN KEY (`flatpage_id`) REFERENCES `django_flatpage` (`id`),
  CONSTRAINT `site_id_refs_id_4e3eeb57` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_flatpage_sites`
--

LOCK TABLES `django_flatpage_sites` WRITE;
/*!40000 ALTER TABLE `django_flatpage_sites` DISABLE KEYS */;
INSERT INTO `django_flatpage_sites` VALUES (1,1,1);
/*!40000 ALTER TABLE `django_flatpage_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('fae52eed4ca7bbc71d70031d3ce170a8','ODE5ZGI3ZTlhNjUzMTM3MjA3MzI0NGQ1ZTEwNGE4OWQ1NzE3OTJlZDqAAn1xAShVDmZhY2Vib29r\nX3N0YXRlVSBQVjFlcklKTUdXdHZ5bnhRV3FFbTJVRHAyVDFMWDRIblUEbmV4dHECWGgAAAAvYWN0\naXZpdGllcy90cnlfYmVjb21lX2ZyaWVuZHMvMi8/Zm9sbG93PS9wcm9kdWN0cy81OTAwNDE0Mi9v\namFsaWxsby1jb2xsYXItYWJhbG9yaW9zLXRhZ3VhLTQ1LXVuaWRhZGVzL3EDdS4=\n','2015-05-23 21:15:51');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'localhost:8000','localhost:8000'),(2,'stage.ecomarket.com','stage.ecomarket.com'),(3,'www.ecomarket.com','www.ecomarket.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `easy_thumbnails_source`
--

DROP TABLE IF EXISTS `easy_thumbnails_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `easy_thumbnails_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `modified` datetime NOT NULL DEFAULT '2009-11-22 21:16:23',
  `storage_hash` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `easy_thumbnails_source_name_7549c98cc6dd6969_uniq` (`name`,`storage_hash`),
  KEY `easy_thumbnails_source_52094d6e` (`name`),
  KEY `easy_thumbnails_source_3a997c55` (`storage_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easy_thumbnails_source`
--

LOCK TABLES `easy_thumbnails_source` WRITE;
/*!40000 ALTER TABLE `easy_thumbnails_source` DISABLE KEYS */;
/*!40000 ALTER TABLE `easy_thumbnails_source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `easy_thumbnails_thumbnail`
--

DROP TABLE IF EXISTS `easy_thumbnails_thumbnail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `easy_thumbnails_thumbnail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `modified` datetime NOT NULL DEFAULT '2009-11-22 21:16:23',
  `source_id` int(11) NOT NULL,
  `storage_hash` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `easy_thumbnails_thumbnail_source_id_1f50d53db8191480_uniq` (`source_id`,`name`,`storage_hash`),
  KEY `easy_thumbnails_thumbnail_89f89e85` (`source_id`),
  KEY `easy_thumbnails_thumbnail_52094d6e` (`name`),
  KEY `easy_thumbnails_thumbnail_3a997c55` (`storage_hash`),
  CONSTRAINT `source_id_refs_id_38c628a45bffe8f5` FOREIGN KEY (`source_id`) REFERENCES `easy_thumbnails_source` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easy_thumbnails_thumbnail`
--

LOCK TABLES `easy_thumbnails_thumbnail` WRITE;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnail` DISABLE KEYS */;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image_crop_tempimage`
--

DROP TABLE IF EXISTS `image_crop_tempimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image_crop_tempimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `filename` varchar(255) NOT NULL DEFAULT '',
  `original` varchar(255) NOT NULL,
  `data` longtext NOT NULL,
  `standard` varchar(255),
  `uuid` varchar(36) NOT NULL,
  `tag` varchar(255) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `image_crop_tempimage_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_6ccd3b76ab4728e8` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_crop_tempimage`
--

LOCK TABLES `image_crop_tempimage` WRITE;
/*!40000 ALTER TABLE `image_crop_tempimage` DISABLE KEYS */;
INSERT INTO `image_crop_tempimage` VALUES (1,2,'bd88914f-4e6e-4677-9750-f24ff542fb51_10494582_794684563897752_5880787750844003534_n.jpg','image_crop/original/bd88914f-4e6e-4677-9750-f24ff542fb51_10494582_794684563897752_5880787750844003534_n.jpg','{\"coords\": {\"xr\": 277, \"yb\": 315, \"yt\": 38, \"xl\": 0}}','image_crop/standard/bd88914f-4e6e-4677-9750-f24ff542fb51_10494582_794684563897752_5880787750844003534_n.jpg','bd88914f-4e6e-4677-9750-f24ff542fb51','','2015-05-09 16:29:59'),(2,2,'773dd665-64b0-4ee1-91a7-09a219488d05_1920193_707276079305268_1347085210_n.jpg','image_crop/original/773dd665-64b0-4ee1-91a7-09a219488d05_1920193_707276079305268_1347085210_n.jpg','{\"coords\": {\"xr\": 613, \"yb\": 360, \"yt\": 90, \"xl\": 342}}','image_crop/standard/773dd665-64b0-4ee1-91a7-09a219488d05_1920193_707276079305268_1347085210_n.jpg','773dd665-64b0-4ee1-91a7-09a219488d05','','2015-05-09 16:31:07'),(3,2,'e29396d8-918d-4d6a-8f08-cd6aafdacf23_pu-8-ovalo-doble-acabado2.jpg','image_crop/original/e29396d8-918d-4d6a-8f08-cd6aafdacf23_pu-8-ovalo-doble-acabado2.jpg','{\"coords\": {\"xr\": 1327, \"yb\": 1070, \"yt\": 0, \"xl\": 256}}','image_crop/standard/e29396d8-918d-4d6a-8f08-cd6aafdacf23_pu-8-ovalo-doble-acabado2.jpg','e29396d8-918d-4d6a-8f08-cd6aafdacf23','','2015-05-09 20:44:21'),(4,2,'6545a296-58e8-4f29-9d42-cceabc265978_pu-8-ovalo-doble-acabado2.jpg','image_crop/original/6545a296-58e8-4f29-9d42-cceabc265978_pu-8-ovalo-doble-acabado2.jpg','{\"coords\": {\"xr\": 1343, \"yb\": 1070, \"yt\": 0, \"xl\": 272}}','image_crop/standard/6545a296-58e8-4f29-9d42-cceabc265978_pu-8-ovalo-doble-acabado2.jpg','6545a296-58e8-4f29-9d42-cceabc265978','','2015-05-09 20:53:12');
/*!40000 ALTER TABLE `image_crop_tempimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lovelists_lovelist`
--

DROP TABLE IF EXISTS `lovelists_lovelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lovelists_lovelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `primary_category_id` int(11) NOT NULL,
  `secondary_category_id` int(11) DEFAULT NULL,
  `tertiary_category_id` int(11) DEFAULT NULL,
  `title` varchar(155) NOT NULL,
  `description` longtext,
  `slug` varchar(50) NOT NULL,
  `is_public` tinyint(1) NOT NULL DEFAULT '0',
  `identifier` int(11) NOT NULL DEFAULT '0',
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `promoted` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `identifier` (`identifier`),
  KEY `lovelists_lovelist_fbfc09f1` (`user_id`),
  KEY `lovelists_lovelist_8ede101f` (`primary_category_id`),
  KEY `lovelists_lovelist_9fbb9bdd` (`secondary_category_id`),
  KEY `lovelists_lovelist_8348d4e0` (`tertiary_category_id`),
  KEY `lovelists_lovelist_a951d5d6` (`slug`),
  CONSTRAINT `primary_category_id_refs_id_34323950aaaaa65d` FOREIGN KEY (`primary_category_id`) REFERENCES `marketplace_category` (`id`),
  CONSTRAINT `secondary_category_id_refs_id_34323950aaaaa65d` FOREIGN KEY (`secondary_category_id`) REFERENCES `marketplace_category` (`id`),
  CONSTRAINT `tertiary_category_id_refs_id_34323950aaaaa65d` FOREIGN KEY (`tertiary_category_id`) REFERENCES `marketplace_category` (`id`),
  CONSTRAINT `user_id_refs_id_27f54260362e2360` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lovelists_lovelist`
--

LOCK TABLES `lovelists_lovelist` WRITE;
/*!40000 ALTER TABLE `lovelists_lovelist` DISABLE KEYS */;
INSERT INTO `lovelists_lovelist` VALUES (1,2,1,NULL,NULL,'Cosas que me gustan','','cosas-que-me-gustan',1,26441156,'2015-05-09 20:57:57','2015-05-09 20:58:07',NULL);
/*!40000 ALTER TABLE `lovelists_lovelist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lovelists_lovelistproduct`
--

DROP TABLE IF EXISTS `lovelists_lovelistproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lovelists_lovelistproduct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `love_list_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `weight` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lovelists_lovelistproduct_love_list_id_16885bdf0a6ea1c_uniq` (`love_list_id`,`product_id`),
  KEY `lovelists_lovelistproduct_1df41f8e` (`love_list_id`),
  KEY `lovelists_lovelistproduct_bb420c12` (`product_id`),
  CONSTRAINT `product_id_refs_id_7524686fca621295` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`),
  CONSTRAINT `love_list_id_refs_id_68c769e83af71a5d` FOREIGN KEY (`love_list_id`) REFERENCES `lovelists_lovelist` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lovelists_lovelistproduct`
--

LOCK TABLES `lovelists_lovelistproduct` WRITE;
/*!40000 ALTER TABLE `lovelists_lovelistproduct` DISABLE KEYS */;
INSERT INTO `lovelists_lovelistproduct` VALUES (1,1,1,0);
/*!40000 ALTER TABLE `lovelists_lovelistproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lovelists_promotionscheduler`
--

DROP TABLE IF EXISTS `lovelists_promotionscheduler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lovelists_promotionscheduler` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `love_list_id` int(11) NOT NULL,
  `actioned` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `lovelists_promotionscheduler_1df41f8e` (`love_list_id`),
  CONSTRAINT `love_list_id_refs_id_7fdfac352bc3e601` FOREIGN KEY (`love_list_id`) REFERENCES `lovelists_lovelist` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lovelists_promotionscheduler`
--

LOCK TABLES `lovelists_promotionscheduler` WRITE;
/*!40000 ALTER TABLE `lovelists_promotionscheduler` DISABLE KEYS */;
/*!40000 ALTER TABLE `lovelists_promotionscheduler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mailing_lists_batchjob`
--

DROP TABLE IF EXISTS `mailing_lists_batchjob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailing_lists_batchjob` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `remote_id` varchar(24) DEFAULT NULL,
  `status` smallint(6) NOT NULL DEFAULT '0',
  `submitted` datetime DEFAULT NULL,
  `completed` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mailing_lists_batchjob`
--

LOCK TABLES `mailing_lists_batchjob` WRITE;
/*!40000 ALTER TABLE `mailing_lists_batchjob` DISABLE KEYS */;
/*!40000 ALTER TABLE `mailing_lists_batchjob` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mailing_lists_batchjob_created`
--

DROP TABLE IF EXISTS `mailing_lists_batchjob_created`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailing_lists_batchjob_created` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `batchjob_id` int(11) NOT NULL,
  `mailinglistsignup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mailing_lists_batchjob_create_batchjob_id_3793fb83d3dd186b_uniq` (`batchjob_id`,`mailinglistsignup_id`),
  KEY `mailing_lists_batchjob_created_6ec36f7d` (`batchjob_id`),
  KEY `mailing_lists_batchjob_created_6828c7b2` (`mailinglistsignup_id`),
  CONSTRAINT `mailinglistsignup_id_refs_id_17a0193992bd08d3` FOREIGN KEY (`mailinglistsignup_id`) REFERENCES `mailing_lists_mailinglistsignup` (`id`),
  CONSTRAINT `batchjob_id_refs_id_1b23152463208ed8` FOREIGN KEY (`batchjob_id`) REFERENCES `mailing_lists_batchjob` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mailing_lists_batchjob_created`
--

LOCK TABLES `mailing_lists_batchjob_created` WRITE;
/*!40000 ALTER TABLE `mailing_lists_batchjob_created` DISABLE KEYS */;
/*!40000 ALTER TABLE `mailing_lists_batchjob_created` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mailing_lists_batchjob_updated`
--

DROP TABLE IF EXISTS `mailing_lists_batchjob_updated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailing_lists_batchjob_updated` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `batchjob_id` int(11) NOT NULL,
  `mailinglistsignup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mailing_lists_batchjob_update_batchjob_id_291d1b008b3dcc68_uniq` (`batchjob_id`,`mailinglistsignup_id`),
  KEY `mailing_lists_batchjob_updated_6ec36f7d` (`batchjob_id`),
  KEY `mailing_lists_batchjob_updated_6828c7b2` (`mailinglistsignup_id`),
  CONSTRAINT `mailinglistsignup_id_refs_id_1e41545569cc5370` FOREIGN KEY (`mailinglistsignup_id`) REFERENCES `mailing_lists_mailinglistsignup` (`id`),
  CONSTRAINT `batchjob_id_refs_id_4775d3e41bb3925b` FOREIGN KEY (`batchjob_id`) REFERENCES `mailing_lists_batchjob` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mailing_lists_batchjob_updated`
--

LOCK TABLES `mailing_lists_batchjob_updated` WRITE;
/*!40000 ALTER TABLE `mailing_lists_batchjob_updated` DISABLE KEYS */;
/*!40000 ALTER TABLE `mailing_lists_batchjob_updated` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mailing_lists_deletedemail`
--

DROP TABLE IF EXISTS `mailing_lists_deletedemail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailing_lists_deletedemail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) NOT NULL,
  `email_address` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_address` (`email_address`),
  KEY `mailing_lists_deletedemail_751f44ae` (`job_id`),
  CONSTRAINT `job_id_refs_id_73496ebe30f4c1b3` FOREIGN KEY (`job_id`) REFERENCES `mailing_lists_batchjob` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mailing_lists_deletedemail`
--

LOCK TABLES `mailing_lists_deletedemail` WRITE;
/*!40000 ALTER TABLE `mailing_lists_deletedemail` DISABLE KEYS */;
/*!40000 ALTER TABLE `mailing_lists_deletedemail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mailing_lists_mailinglistsignup`
--

DROP TABLE IF EXISTS `mailing_lists_mailinglistsignup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mailing_lists_mailinglistsignup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email_address` varchar(255) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `category_id` int(11),
  `telephone_number` varchar(255) DEFAULT NULL,
  `country_id` int(11) DEFAULT NULL,
  `source` varchar(2) NOT NULL,
  `date_added` datetime NOT NULL,
  `member_type` smallint(6),
  `is_seller_lead` tinyint(1) NOT NULL,
  `ip_address` char(15),
  `marketing_optin` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_address` (`email_address`),
  KEY `mailing_lists_mailinglistsignup_fbfc09f1` (`user_id`),
  KEY `mailing_lists_mailinglistsignup_534dd89` (`country_id`),
  KEY `mailing_lists_mailinglistsignup_42dc49bc` (`category_id`),
  CONSTRAINT `category_id_refs_id_3372784cc2696149` FOREIGN KEY (`category_id`) REFERENCES `marketplace_category` (`id`),
  CONSTRAINT `country_id_refs_id_6f80e450ca583924` FOREIGN KEY (`country_id`) REFERENCES `marketplace_country` (`id`),
  CONSTRAINT `user_id_refs_id_3b05c6e9195a4134` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mailing_lists_mailinglistsignup`
--

LOCK TABLES `mailing_lists_mailinglistsignup` WRITE;
/*!40000 ALTER TABLE `mailing_lists_mailinglistsignup` DISABLE KEYS */;
/*!40000 ALTER TABLE `mailing_lists_mailinglistsignup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_category`
--

DROP TABLE IF EXISTS `marketplace_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  `description` varchar(511),
  `image_src` varchar(255),
  `seo_title` varchar(511),
  `navigation_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `marketplace_category_63f17a16` (`parent_id`),
  KEY `marketplace_category_a951d5d6` (`slug`),
  KEY `marketplace_category_42b06ff6` (`lft`),
  KEY `marketplace_category_91543e5a` (`rght`),
  KEY `marketplace_category_efd07f28` (`tree_id`),
  KEY `marketplace_category_2a8f42e8` (`level`),
  CONSTRAINT `parent_id_refs_id_4e26385001453153` FOREIGN KEY (`parent_id`) REFERENCES `marketplace_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_category`
--

LOCK TABLES `marketplace_category` WRITE;
/*!40000 ALTER TABLE `marketplace_category` DISABLE KEYS */;
INSERT INTO `marketplace_category` VALUES (1,NULL,'Joyeria','joyeria',1,1,2,3,0,'','','','Joyas'),(2,NULL,'Ropa','ropa',1,1,2,4,0,'','','','Ropa'),(3,NULL,'Hogar y Decoración','hogar-y-decoracion',1,1,2,2,0,'','','','Hogar y Decoración'),(4,NULL,'Comestibles','comestibles',1,1,2,1,0,'','','','Comestibles');
/*!40000 ALTER TABLE `marketplace_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_cause`
--

DROP TABLE IF EXISTS `marketplace_cause`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_cause` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `seo_title` varchar(511),
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_cause_title_2107cd90b6308eb2_uniq` (`title`),
  KEY `marketplace_cause_a951d5d6` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_cause`
--

LOCK TABLES `marketplace_cause` WRITE;
/*!40000 ALTER TABLE `marketplace_cause` DISABLE KEYS */;
INSERT INTO `marketplace_cause` VALUES (1,'Smart Products','smart-products','','');
/*!40000 ALTER TABLE `marketplace_cause` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_certificate`
--

DROP TABLE IF EXISTS `marketplace_certificate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_certificate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `url` varchar(200) NOT NULL,
  `cause_id` int(11) NOT NULL,
  `image` varchar(255),
  `seo_title` varchar(511),
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_certificate_title_3f5baae43a410534_uniq` (`title`),
  KEY `marketplace_certificate_a951d5d6` (`slug`),
  KEY `marketplace_certificate_bf6f82dc` (`cause_id`),
  CONSTRAINT `cause_id_refs_id_4d504e14509fc1bf` FOREIGN KEY (`cause_id`) REFERENCES `marketplace_cause` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_certificate`
--

LOCK TABLES `marketplace_certificate` WRITE;
/*!40000 ALTER TABLE `marketplace_certificate` DISABLE KEYS */;
INSERT INTO `marketplace_certificate` VALUES (1,'Certificado Producto Smart','certificado-producto-smart','','http://github.com/codeadict',1,'product/certificates/logo_noTM-mini2.jpg','');
/*!40000 ALTER TABLE `marketplace_certificate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_color`
--

DROP TABLE IF EXISTS `marketplace_color`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_color` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `seo_title` varchar(511),
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_color_title_5158c0ddf0c35922_uniq` (`title`),
  KEY `marketplace_color_a951d5d6` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_color`
--

LOCK TABLES `marketplace_color` WRITE;
/*!40000 ALTER TABLE `marketplace_color` DISABLE KEYS */;
INSERT INTO `marketplace_color` VALUES (1,'Green','green','Green Color','Green '),(2,'Red','red','Red Products','Red');
/*!40000 ALTER TABLE `marketplace_color` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_country`
--

DROP TABLE IF EXISTS `marketplace_country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL,
  `title` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_country`
--

LOCK TABLES `marketplace_country` WRITE;
/*!40000 ALTER TABLE `marketplace_country` DISABLE KEYS */;
INSERT INTO `marketplace_country` VALUES (1,'GB','United Kingdom');
/*!40000 ALTER TABLE `marketplace_country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_currencyexchangerate`
--

DROP TABLE IF EXISTS `marketplace_currencyexchangerate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_currencyexchangerate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `base_currency` varchar(3) NOT NULL,
  `currency` varchar(3) NOT NULL,
  `date_time` datetime NOT NULL,
  `exchange_rate` decimal(15,6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_currencyexchangerate`
--

LOCK TABLES `marketplace_currencyexchangerate` WRITE;
/*!40000 ALTER TABLE `marketplace_currencyexchangerate` DISABLE KEYS */;
/*!40000 ALTER TABLE `marketplace_currencyexchangerate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_ingredient`
--

DROP TABLE IF EXISTS `marketplace_ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_ingredient` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `seo_title` varchar(511),
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_ingredient_title_68b1146718a70343_uniq` (`title`),
  KEY `marketplace_ingredient_a951d5d6` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_ingredient`
--

LOCK TABLES `marketplace_ingredient` WRITE;
/*!40000 ALTER TABLE `marketplace_ingredient` DISABLE KEYS */;
INSERT INTO `marketplace_ingredient` VALUES (1,'Tagua','tagua','',''),(2,'Agua','agua','',''),(3,'Madera','madera','','');
/*!40000 ALTER TABLE `marketplace_ingredient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_keyword`
--

DROP TABLE IF EXISTS `marketplace_keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_keyword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `seo_title` varchar(511),
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_keyword_title_4c5d481ffb1dff2c_uniq` (`title`),
  KEY `marketplace_keyword_a951d5d6` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_keyword`
--

LOCK TABLES `marketplace_keyword` WRITE;
/*!40000 ALTER TABLE `marketplace_keyword` DISABLE KEYS */;
INSERT INTO `marketplace_keyword` VALUES (1,'tagua','tagua','',''),(2,'andes','andes','',''),(3,'ecuador','ecuador','',''),(4,'jewlery','jewlery','','');
/*!40000 ALTER TABLE `marketplace_keyword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_material`
--

DROP TABLE IF EXISTS `marketplace_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_material` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `seo_title` varchar(511),
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_material_title_75fb432ce5f45b97_uniq` (`title`),
  KEY `marketplace_material_a951d5d6` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_material`
--

LOCK TABLES `marketplace_material` WRITE;
/*!40000 ALTER TABLE `marketplace_material` DISABLE KEYS */;
INSERT INTO `marketplace_material` VALUES (1,'Tagua','tagua','',''),(2,'Madera','madera','',''),(3,'Piedra','piedra','',''),(4,'Tela','tela','','');
/*!40000 ALTER TABLE `marketplace_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_occasion`
--

DROP TABLE IF EXISTS `marketplace_occasion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_occasion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `seo_title` varchar(511),
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_occasion_title_2b040a1fb466f271_uniq` (`title`),
  KEY `marketplace_occasion_a951d5d6` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_occasion`
--

LOCK TABLES `marketplace_occasion` WRITE;
/*!40000 ALTER TABLE `marketplace_occasion` DISABLE KEYS */;
INSERT INTO `marketplace_occasion` VALUES (1,'Salidas','salidas','',''),(2,'Formal','formal','',''),(3,'Para Comer','para-comer','','');
/*!40000 ALTER TABLE `marketplace_occasion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_price`
--

DROP TABLE IF EXISTS `marketplace_price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_price` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `amount` decimal(6,2) NOT NULL,
  `amount_currency` varchar(3) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `marketplace_price_bb420c12` (`product_id`),
  CONSTRAINT `product_id_refs_id_16c73a6b9e118ae7` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_price`
--

LOCK TABLES `marketplace_price` WRITE;
/*!40000 ALTER TABLE `marketplace_price` DISABLE KEYS */;
INSERT INTO `marketplace_price` VALUES (1,1,19.00,'GBP');
/*!40000 ALTER TABLE `marketplace_price` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_product`
--

DROP TABLE IF EXISTS `marketplace_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stall_id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `slug` varchar(50) NOT NULL,
  `stock` int(11) DEFAULT NULL,
  `primary_category_id` int(11) DEFAULT NULL,
  `secondary_category_id` int(11) DEFAULT NULL,
  `status` varchar(1) NOT NULL DEFAULT 'd',
  `created` datetime NOT NULL,
  `updated` datetime NOT NULL,
  `shipping_profile_id` int(11) DEFAULT NULL,
  `publication_date` datetime,
  `number_of_sales` int(11) NOT NULL,
  `number_of_recent_sales` smallint(6) NOT NULL,
  `flag` int(10) unsigned,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  KEY `marketplace_product_368109e5` (`stall_id`),
  KEY `marketplace_product_a951d5d6` (`slug`),
  KEY `marketplace_product_8ede101f` (`primary_category_id`),
  KEY `marketplace_product_9fbb9bdd` (`secondary_category_id`),
  KEY `marketplace_product_e68d316c` (`shipping_profile_id`),
  CONSTRAINT `primary_category_id_refs_id_784a64fa0aa0157` FOREIGN KEY (`primary_category_id`) REFERENCES `marketplace_category` (`id`),
  CONSTRAINT `secondary_category_id_refs_id_784a64fa0aa0157` FOREIGN KEY (`secondary_category_id`) REFERENCES `marketplace_category` (`id`),
  CONSTRAINT `shipping_profile_id_refs_id_73804f42888991af` FOREIGN KEY (`shipping_profile_id`) REFERENCES `marketplace_shippingprofile` (`id`),
  CONSTRAINT `stall_id_refs_id_31d9259ee583b52c` FOREIGN KEY (`stall_id`) REFERENCES `marketplace_stall` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_product`
--

LOCK TABLES `marketplace_product` WRITE;
/*!40000 ALTER TABLE `marketplace_product` DISABLE KEYS */;
INSERT INTO `marketplace_product` VALUES (1,1,'OJALILLO COLLAR ABALORIOS TAGUA (45 UNIDADES)','Gracias a su delicado diseño estos productos de bisuteria se ven perfectos en aretes y tambien como dijes o colgantes en collares y pulseras. Puedes confeccionar cualquier pieza de bisuteria o las manualidades que desees con estos divertidos diseños. Nuestros abalorios premium no se decoloran, destiñen ni manchan la ropa ni la piel. Usamos tintes libres de toxico en nuestros abalorios premium, 100% garantizado. Las medidas pueden variar. Hecho en Ecuador.','ojalillo-collar-abalorios-tagua-45-unidades',10,1,2,'l','2015-05-09 20:52:04','2015-05-09 20:55:45',1,NULL,0,0,NULL);
/*!40000 ALTER TABLE `marketplace_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_product_causes`
--

DROP TABLE IF EXISTS `marketplace_product_causes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_product_causes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `cause_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_product_causes_product_id_2f8d2749559a2dae_uniq` (`product_id`,`cause_id`),
  KEY `marketplace_product_causes_bb420c12` (`product_id`),
  KEY `marketplace_product_causes_bf6f82dc` (`cause_id`),
  CONSTRAINT `cause_id_refs_id_21c75276f7ddef19` FOREIGN KEY (`cause_id`) REFERENCES `marketplace_cause` (`id`),
  CONSTRAINT `product_id_refs_id_7e2c6160164245cb` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_product_causes`
--

LOCK TABLES `marketplace_product_causes` WRITE;
/*!40000 ALTER TABLE `marketplace_product_causes` DISABLE KEYS */;
INSERT INTO `marketplace_product_causes` VALUES (3,1,1);
/*!40000 ALTER TABLE `marketplace_product_causes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_product_certificates`
--

DROP TABLE IF EXISTS `marketplace_product_certificates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_product_certificates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `certificate_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_product_certificat_product_id_5af69a07a596386a_uniq` (`product_id`,`certificate_id`),
  KEY `marketplace_product_certificates_bb420c12` (`product_id`),
  KEY `marketplace_product_certificates_5be8d0ce` (`certificate_id`),
  CONSTRAINT `certificate_id_refs_id_509272c041f736c9` FOREIGN KEY (`certificate_id`) REFERENCES `marketplace_certificate` (`id`),
  CONSTRAINT `product_id_refs_id_26e62ca4b2ab4dab` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_product_certificates`
--

LOCK TABLES `marketplace_product_certificates` WRITE;
/*!40000 ALTER TABLE `marketplace_product_certificates` DISABLE KEYS */;
INSERT INTO `marketplace_product_certificates` VALUES (3,1,1);
/*!40000 ALTER TABLE `marketplace_product_certificates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_product_colors`
--

DROP TABLE IF EXISTS `marketplace_product_colors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_product_colors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `color_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_product_colors_product_id_3f8ae98ecb6f3d72_uniq` (`product_id`,`color_id`),
  KEY `marketplace_product_colors_bb420c12` (`product_id`),
  KEY `marketplace_product_colors_eab7fe80` (`color_id`),
  CONSTRAINT `color_id_refs_id_48369a53f1bce11f` FOREIGN KEY (`color_id`) REFERENCES `marketplace_color` (`id`),
  CONSTRAINT `product_id_refs_id_5a32f0b10345f5d9` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_product_colors`
--

LOCK TABLES `marketplace_product_colors` WRITE;
/*!40000 ALTER TABLE `marketplace_product_colors` DISABLE KEYS */;
INSERT INTO `marketplace_product_colors` VALUES (5,1,1),(6,1,2);
/*!40000 ALTER TABLE `marketplace_product_colors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_product_ingredients`
--

DROP TABLE IF EXISTS `marketplace_product_ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_product_ingredients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `ingredient_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_product_ingredient_product_id_56997544e23690e8_uniq` (`product_id`,`ingredient_id`),
  KEY `marketplace_product_ingredients_bb420c12` (`product_id`),
  KEY `marketplace_product_ingredients_78058839` (`ingredient_id`),
  CONSTRAINT `ingredient_id_refs_id_53d048012fdb2f83` FOREIGN KEY (`ingredient_id`) REFERENCES `marketplace_ingredient` (`id`),
  CONSTRAINT `product_id_refs_id_102b81aef6dca812` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_product_ingredients`
--

LOCK TABLES `marketplace_product_ingredients` WRITE;
/*!40000 ALTER TABLE `marketplace_product_ingredients` DISABLE KEYS */;
INSERT INTO `marketplace_product_ingredients` VALUES (4,1,1),(5,1,2),(6,1,3);
/*!40000 ALTER TABLE `marketplace_product_ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_product_keywords`
--

DROP TABLE IF EXISTS `marketplace_product_keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_product_keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `keyword_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_product_keywords_product_id_1ff87e556631790a_uniq` (`product_id`,`keyword_id`),
  KEY `marketplace_product_keywords_bb420c12` (`product_id`),
  KEY `marketplace_product_keywords_a6434082` (`keyword_id`),
  CONSTRAINT `keyword_id_refs_id_29430ecfa7b01b67` FOREIGN KEY (`keyword_id`) REFERENCES `marketplace_keyword` (`id`),
  CONSTRAINT `product_id_refs_id_70b70abeb748a6c3` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_product_keywords`
--

LOCK TABLES `marketplace_product_keywords` WRITE;
/*!40000 ALTER TABLE `marketplace_product_keywords` DISABLE KEYS */;
INSERT INTO `marketplace_product_keywords` VALUES (9,1,1),(10,1,2),(11,1,3),(12,1,4);
/*!40000 ALTER TABLE `marketplace_product_keywords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_product_materials`
--

DROP TABLE IF EXISTS `marketplace_product_materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_product_materials` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `material_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_product_materials_product_id_2d462845508eb4e8_uniq` (`product_id`,`material_id`),
  KEY `marketplace_product_materials_bb420c12` (`product_id`),
  KEY `marketplace_product_materials_fab9ba43` (`material_id`),
  CONSTRAINT `material_id_refs_id_33000a808726d5ab` FOREIGN KEY (`material_id`) REFERENCES `marketplace_material` (`id`),
  CONSTRAINT `product_id_refs_id_834d777a3893d32` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_product_materials`
--

LOCK TABLES `marketplace_product_materials` WRITE;
/*!40000 ALTER TABLE `marketplace_product_materials` DISABLE KEYS */;
INSERT INTO `marketplace_product_materials` VALUES (4,1,1),(5,1,2),(6,1,4);
/*!40000 ALTER TABLE `marketplace_product_materials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_product_occasions`
--

DROP TABLE IF EXISTS `marketplace_product_occasions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_product_occasions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `occasion_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_product_occasions_product_id_5dd3850b075a086c_uniq` (`product_id`,`occasion_id`),
  KEY `marketplace_product_occasions_bb420c12` (`product_id`),
  KEY `marketplace_product_occasions_d66a9f35` (`occasion_id`),
  CONSTRAINT `occasion_id_refs_id_2ce16bb89e116ae5` FOREIGN KEY (`occasion_id`) REFERENCES `marketplace_occasion` (`id`),
  CONSTRAINT `product_id_refs_id_73d1c252df5622b0` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_product_occasions`
--

LOCK TABLES `marketplace_product_occasions` WRITE;
/*!40000 ALTER TABLE `marketplace_product_occasions` DISABLE KEYS */;
INSERT INTO `marketplace_product_occasions` VALUES (2,1,2);
/*!40000 ALTER TABLE `marketplace_product_occasions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_product_recipients`
--

DROP TABLE IF EXISTS `marketplace_product_recipients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_product_recipients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `recipient_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_product_recipients_product_id_6fe55689d21be0fa_uniq` (`product_id`,`recipient_id`),
  KEY `marketplace_product_recipients_bb420c12` (`product_id`),
  KEY `marketplace_product_recipients_fcd09624` (`recipient_id`),
  CONSTRAINT `recipient_id_refs_id_318d035740e7fc71` FOREIGN KEY (`recipient_id`) REFERENCES `marketplace_recipient` (`id`),
  CONSTRAINT `product_id_refs_id_2da387fc6d5b134d` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_product_recipients`
--

LOCK TABLES `marketplace_product_recipients` WRITE;
/*!40000 ALTER TABLE `marketplace_product_recipients` DISABLE KEYS */;
INSERT INTO `marketplace_product_recipients` VALUES (5,1,1),(6,1,2);
/*!40000 ALTER TABLE `marketplace_product_recipients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_productimage`
--

DROP TABLE IF EXISTS `marketplace_productimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_productimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL DEFAULT '',
  `filename` varchar(255) NOT NULL DEFAULT '',
  `image` varchar(255) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `data` longtext NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `created` date NOT NULL,
  `updated` date NOT NULL,
  `thumbnail` varchar(255),
  PRIMARY KEY (`id`),
  KEY `marketplace_productimage_bb420c12` (`product_id`),
  KEY `marketplace_productimage_a951d5d6` (`slug`),
  CONSTRAINT `product_id_refs_id_e0f992f41297023` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_productimage`
--

LOCK TABLES `marketplace_productimage` WRITE;
/*!40000 ALTER TABLE `marketplace_productimage` DISABLE KEYS */;
INSERT INTO `marketplace_productimage` VALUES (1,1,'Imagen Principal','imagen-principal.jpg','product/59004142/ojalillo-collar-abalorios-tagua-45-unidades/pu-8-ovalo-doble-acabado2.jpg','imagen-principal','{\"image_crop\": [272, 1343, 0, 1070]}',1,'2015-05-09','2015-05-09','product/59004142/ojalillo-collar-abalorios-tagua-45-unidades/thumbs/imagen-principal.jpg');
/*!40000 ALTER TABLE `marketplace_productimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_recipient`
--

DROP TABLE IF EXISTS `marketplace_recipient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_recipient` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `seo_title` varchar(511),
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_recipient_title_4b94c38e38e4e5de_uniq` (`title`),
  KEY `marketplace_recipient_a951d5d6` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_recipient`
--

LOCK TABLES `marketplace_recipient` WRITE;
/*!40000 ALTER TABLE `marketplace_recipient` DISABLE KEYS */;
INSERT INTO `marketplace_recipient` VALUES (1,'Mujeres','mujeres','',''),(2,'Chicas','chicas','','');
/*!40000 ALTER TABLE `marketplace_recipient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_shippingprofile`
--

DROP TABLE IF EXISTS `marketplace_shippingprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_shippingprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stall_id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `shipping_country_id` int(11) DEFAULT NULL,
  `shipping_postcode` varchar(20),
  `others_price` decimal(6,2),
  `others_price_extra` decimal(6,2),
  `others_price_currency` varchar(3) NOT NULL,
  `others_price_extra_currency` varchar(3) NOT NULL,
  `others_delivery_time` int(11),
  `others_delivery_time_max` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_shippingprofile_stall_id_6792ecc210690f61_uniq` (`stall_id`,`title`),
  KEY `marketplace_shippingprofile_368109e5` (`stall_id`),
  KEY `marketplace_shippingprofile_a951d5d6` (`slug`),
  KEY `marketplace_shippingprofile_fea5e43f` (`shipping_country_id`),
  CONSTRAINT `shipping_country_id_refs_id_2994eed70380318e` FOREIGN KEY (`shipping_country_id`) REFERENCES `marketplace_country` (`id`),
  CONSTRAINT `stall_id_refs_id_1d5688385b862fc` FOREIGN KEY (`stall_id`) REFERENCES `marketplace_stall` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_shippingprofile`
--

LOCK TABLES `marketplace_shippingprofile` WRITE;
/*!40000 ALTER TABLE `marketplace_shippingprofile` DISABLE KEYS */;
INSERT INTO `marketplace_shippingprofile` VALUES (1,1,'Envío USA','envio-usa',1,'',NULL,NULL,'GBP','GBP',NULL,NULL);
/*!40000 ALTER TABLE `marketplace_shippingprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_shippingrule`
--

DROP TABLE IF EXISTS `marketplace_shippingrule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_shippingrule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `profile_id` int(11) NOT NULL,
  `rule_price` decimal(6,2) NOT NULL DEFAULT '0.00',
  `rule_price_extra` decimal(6,2) NOT NULL DEFAULT '0.00',
  `rule_price_currency` varchar(3) NOT NULL,
  `rule_price_extra_currency` varchar(3) NOT NULL,
  `despatch_time` int(11) NOT NULL,
  `delivery_time` int(11) NOT NULL,
  `delivery_time_max` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `marketplace_shippingrule_141c6eec` (`profile_id`),
  CONSTRAINT `profile_id_refs_id_2a7d221e87d25a8b` FOREIGN KEY (`profile_id`) REFERENCES `marketplace_shippingprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_shippingrule`
--

LOCK TABLES `marketplace_shippingrule` WRITE;
/*!40000 ALTER TABLE `marketplace_shippingrule` DISABLE KEYS */;
INSERT INTO `marketplace_shippingrule` VALUES (1,1,0.00,0.00,'GBP','GBP',4,6,10);
/*!40000 ALTER TABLE `marketplace_shippingrule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_shippingrule_countries`
--

DROP TABLE IF EXISTS `marketplace_shippingrule_countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_shippingrule_countries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shippingrule_id` int(11) NOT NULL,
  `country_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_shippingrule__shippingrule_id_782d1d3e3863501a_uniq` (`shippingrule_id`,`country_id`),
  KEY `marketplace_shippingrule_countries_645271bc` (`shippingrule_id`),
  KEY `marketplace_shippingrule_countries_534dd89` (`country_id`),
  CONSTRAINT `country_id_refs_id_665b7d7b439c04f9` FOREIGN KEY (`country_id`) REFERENCES `marketplace_country` (`id`),
  CONSTRAINT `shippingrule_id_refs_id_1e34bff531503df2` FOREIGN KEY (`shippingrule_id`) REFERENCES `marketplace_shippingrule` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_shippingrule_countries`
--

LOCK TABLES `marketplace_shippingrule_countries` WRITE;
/*!40000 ALTER TABLE `marketplace_shippingrule_countries` DISABLE KEYS */;
INSERT INTO `marketplace_shippingrule_countries` VALUES (6,1,1);
/*!40000 ALTER TABLE `marketplace_shippingrule_countries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_stall`
--

DROP TABLE IF EXISTS `marketplace_stall`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_stall` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `title` varchar(60) NOT NULL DEFAULT '',
  `slug` varchar(50) NOT NULL,
  `description_short` varchar(255) NOT NULL DEFAULT '',
  `description_full` longtext NOT NULL,
  `paypal_email` varchar(255) NOT NULL DEFAULT '',
  `twitter_username` varchar(255) NOT NULL DEFAULT '',
  `message_after_purchasing` longtext NOT NULL,
  `refunds_policy` longtext NOT NULL,
  `returns_policy` longtext NOT NULL,
  `holiday_mode` tinyint(1) NOT NULL DEFAULT '0',
  `holiday_message` longtext NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `created` date NOT NULL,
  `updated` date NOT NULL DEFAULT '2015-05-09',
  `is_chat_enabled` tinyint(1) NOT NULL,
  `identifier` int(11) NOT NULL,
  `chat_stall_uri` varchar(200) NOT NULL,
  `chat_operator_uri` varchar(200) NOT NULL,
  `email_opt_in` tinyint(1) NOT NULL,
  `phone_landline` varchar(16),
  `phone_mobile` varchar(16),
  `renewal_tier` smallint(5) unsigned NOT NULL,
  `is_suspended` tinyint(1) NOT NULL,
  `reason_for_suspension` smallint(5) unsigned,
  `last_stock_checked_at` datetime NOT NULL,
  `total_gmv_till_yesterday` decimal(10,2) NOT NULL,
  `total_orders_till_yesterday` smallint(5) unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `total_suspensions_till_yesterday` smallint(5) unsigned NOT NULL,
  `is_closed` tinyint(1) NOT NULL,
  `total_products_till_yesterday` smallint(5) unsigned NOT NULL,
  `total_live_products_till_yesterday` smallint(5) unsigned NOT NULL,
  `total_messages_received_till_yesterday` smallint(5) unsigned NOT NULL,
  `number_of_calls` smallint(5) unsigned NOT NULL,
  `days_to_next_stockcheck_till_yesterday` smallint(5) unsigned NOT NULL,
  `is_in_video_beta` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `marketplace_stall_slug_465474e3a0e846bf_uniq` (`slug`),
  KEY `marketplace_stall_a951d5d6` (`slug`),
  KEY `marketplace_stall_42dc49bc` (`category_id`),
  CONSTRAINT `category_id_refs_id_66940a19f2b1d275` FOREIGN KEY (`category_id`) REFERENCES `marketplace_stallcategory` (`id`),
  CONSTRAINT `user_id_refs_id_7b637730f6cd8215` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_stall`
--

LOCK TABLES `marketplace_stall` WRITE;
/*!40000 ALTER TABLE `marketplace_stall` DISABLE KEYS */;
INSERT INTO `marketplace_stall` VALUES (1,2,'tagua-heaven','tagua-heaven','We sell tagua nuts jewlwry','We sell natural ecologic jewlery made with products from South America.','dairon.medina@gmail.com','@codeadict','','','',0,'',NULL,'2015-05-09','2015-05-09',0,59004142,'','',1,'+44987612278','+44987612278',3,0,NULL,'2015-05-09 16:35:45',0.00,0,0,0,0,0,0,0,0,0,1);
/*!40000 ALTER TABLE `marketplace_stall` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_stallcallnotes`
--

DROP TABLE IF EXISTS `marketplace_stallcallnotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_stallcallnotes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stall_id` int(11) NOT NULL,
  `notes` longtext,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `marketplace_stallcallnotes_368109e5` (`stall_id`),
  CONSTRAINT `stall_id_refs_id_6596de3cd5677579` FOREIGN KEY (`stall_id`) REFERENCES `marketplace_stall` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_stallcallnotes`
--

LOCK TABLES `marketplace_stallcallnotes` WRITE;
/*!40000 ALTER TABLE `marketplace_stallcallnotes` DISABLE KEYS */;
/*!40000 ALTER TABLE `marketplace_stallcallnotes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_stallcategory`
--

DROP TABLE IF EXISTS `marketplace_stallcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_stallcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `marketplace_stallcategory_63f17a16` (`parent_id`),
  KEY `marketplace_stallcategory_a951d5d6` (`slug`),
  KEY `marketplace_stallcategory_42b06ff6` (`lft`),
  KEY `marketplace_stallcategory_91543e5a` (`rght`),
  KEY `marketplace_stallcategory_efd07f28` (`tree_id`),
  KEY `marketplace_stallcategory_2a8f42e8` (`level`),
  CONSTRAINT `parent_id_refs_id_7d922586e7b55605` FOREIGN KEY (`parent_id`) REFERENCES `marketplace_stallcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_stallcategory`
--

LOCK TABLES `marketplace_stallcategory` WRITE;
/*!40000 ALTER TABLE `marketplace_stallcategory` DISABLE KEYS */;
INSERT INTO `marketplace_stallcategory` VALUES (1,NULL,'Joyería','joyeria',1,1,2,5,0),(2,NULL,'Alimentos','alimentos',1,1,2,1,0),(3,NULL,'Fashion','fashion',1,1,2,4,0),(4,NULL,'Diseño','diseno',1,1,2,3,0),(5,NULL,'Decoración','decoracion',1,1,2,2,0);
/*!40000 ALTER TABLE `marketplace_stallcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_stalloldstylephonenumber`
--

DROP TABLE IF EXISTS `marketplace_stalloldstylephonenumber`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_stalloldstylephonenumber` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stall_id` int(11) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stall_id` (`stall_id`),
  CONSTRAINT `stall_id_refs_id_1d4f2d29b5e15497` FOREIGN KEY (`stall_id`) REFERENCES `marketplace_stall` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_stalloldstylephonenumber`
--

LOCK TABLES `marketplace_stalloldstylephonenumber` WRITE;
/*!40000 ALTER TABLE `marketplace_stalloldstylephonenumber` DISABLE KEYS */;
/*!40000 ALTER TABLE `marketplace_stalloldstylephonenumber` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_stallstatuslog`
--

DROP TABLE IF EXISTS `marketplace_stallstatuslog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_stallstatuslog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stall_id` int(11) NOT NULL,
  `renewal_tier` smallint(5) unsigned NOT NULL DEFAULT '2',
  `is_suspended` tinyint(1) NOT NULL DEFAULT '0',
  `reason_for_suspension` smallint(5) unsigned,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `marketplace_stallstatuslog_368109e5` (`stall_id`),
  CONSTRAINT `stall_id_refs_id_2fa3cf545e88cf06` FOREIGN KEY (`stall_id`) REFERENCES `marketplace_stall` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_stallstatuslog`
--

LOCK TABLES `marketplace_stallstatuslog` WRITE;
/*!40000 ALTER TABLE `marketplace_stallstatuslog` DISABLE KEYS */;
/*!40000 ALTER TABLE `marketplace_stallstatuslog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_stallvideo`
--

DROP TABLE IF EXISTS `marketplace_stallvideo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_stallvideo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stall_id` int(11) NOT NULL,
  `title` varchar(60) NOT NULL,
  `url` varchar(255) NOT NULL,
  `is_welcome` tinyint(1) NOT NULL DEFAULT '0',
  `is_published` tinyint(1) NOT NULL DEFAULT '0',
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `marketplace_stallvideo_368109e5` (`stall_id`),
  CONSTRAINT `stall_id_refs_id_3521f9119e18832d` FOREIGN KEY (`stall_id`) REFERENCES `marketplace_stall` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_stallvideo`
--

LOCK TABLES `marketplace_stallvideo` WRITE;
/*!40000 ALTER TABLE `marketplace_stallvideo` DISABLE KEYS */;
INSERT INTO `marketplace_stallvideo` VALUES (1,1,'Our products','https://www.youtube.com/watch?v=HdMGGjNaTtg',0,1,'2015-05-09 20:05:44');
/*!40000 ALTER TABLE `marketplace_stallvideo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marketplace_suggestedcertificate`
--

DROP TABLE IF EXISTS `marketplace_suggestedcertificate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marketplace_suggestedcertificate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `product_id` int(11) NOT NULL,
  `url` varchar(200) NOT NULL,
  `seo_title` varchar(511),
  PRIMARY KEY (`id`),
  UNIQUE KEY `marketplace_suggestedcertificate_title_492e48b3c5887420_uniq` (`title`),
  KEY `marketplace_suggestedcertificate_a951d5d6` (`slug`),
  KEY `marketplace_suggestedcertificate_bb420c12` (`product_id`),
  CONSTRAINT `product_id_refs_id_1b59fc0be49eeec7` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marketplace_suggestedcertificate`
--

LOCK TABLES `marketplace_suggestedcertificate` WRITE;
/*!40000 ALTER TABLE `marketplace_suggestedcertificate` DISABLE KEYS */;
/*!40000 ALTER TABLE `marketplace_suggestedcertificate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_message`
--

DROP TABLE IF EXISTS `messaging_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messaging_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thread_id` int(11) NOT NULL,
  `subject` varchar(120) NOT NULL,
  `body` longtext NOT NULL,
  `sender_id` int(11) NOT NULL,
  `recipient_id` int(11) DEFAULT NULL,
  `parent_msg_id` int(11) DEFAULT NULL,
  `sent_at` datetime DEFAULT NULL,
  `read_at` datetime DEFAULT NULL,
  `replied_at` datetime DEFAULT NULL,
  `sender_deleted_at` datetime DEFAULT NULL,
  `recipient_deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `messaging_message_9a6ed576` (`thread_id`),
  KEY `messaging_message_901f59e9` (`sender_id`),
  KEY `messaging_message_fcd09624` (`recipient_id`),
  KEY `messaging_message_dfe57a2c` (`parent_msg_id`),
  CONSTRAINT `parent_msg_id_refs_id_4649f58c0a0fc19b` FOREIGN KEY (`parent_msg_id`) REFERENCES `messaging_message` (`id`),
  CONSTRAINT `recipient_id_refs_id_212e9dc3969e1af1` FOREIGN KEY (`recipient_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `sender_id_refs_id_212e9dc3969e1af1` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `thread_id_refs_id_75f91b17f42a9439` FOREIGN KEY (`thread_id`) REFERENCES `messaging_messagethread` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_message`
--

LOCK TABLES `messaging_message` WRITE;
/*!40000 ALTER TABLE `messaging_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_messagethread`
--

DROP TABLE IF EXISTS `messaging_messagethread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messaging_messagethread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `resolved_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_messagethread`
--

LOCK TABLES `messaging_messagethread` WRITE;
/*!40000 ALTER TABLE `messaging_messagethread` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_messagethread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messaging_threaduserstate`
--

DROP TABLE IF EXISTS `messaging_threaduserstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messaging_threaduserstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `thread_id` int(11) NOT NULL,
  `read_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `messaging_threaduserstate_user_id_2cac415bd1078d49_uniq` (`user_id`,`thread_id`),
  KEY `messaging_threaduserstate_fbfc09f1` (`user_id`),
  KEY `messaging_threaduserstate_9a6ed576` (`thread_id`),
  CONSTRAINT `thread_id_refs_id_2ccb1c387ffe17c2` FOREIGN KEY (`thread_id`) REFERENCES `messaging_messagethread` (`id`),
  CONSTRAINT `user_id_refs_id_4402111bdad25c88` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messaging_threaduserstate`
--

LOCK TABLES `messaging_threaduserstate` WRITE;
/*!40000 ALTER TABLE `messaging_threaduserstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `messaging_threaduserstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_tmp_oldcategory`
--

DROP TABLE IF EXISTS `product_tmp_oldcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_tmp_oldcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_tmp_oldcategory_63f17a16` (`parent_id`),
  KEY `product_tmp_oldcategory_a951d5d6` (`slug`),
  KEY `product_tmp_oldcategory_42b06ff6` (`lft`),
  KEY `product_tmp_oldcategory_91543e5a` (`rght`),
  KEY `product_tmp_oldcategory_efd07f28` (`tree_id`),
  KEY `product_tmp_oldcategory_2a8f42e8` (`level`),
  CONSTRAINT `parent_id_refs_id_34879e18ce0da7b9` FOREIGN KEY (`parent_id`) REFERENCES `product_tmp_oldcategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_tmp_oldcategory`
--

LOCK TABLES `product_tmp_oldcategory` WRITE;
/*!40000 ALTER TABLE `product_tmp_oldcategory` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_tmp_oldcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_tmp_tempproduct`
--

DROP TABLE IF EXISTS `product_tmp_tempproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_tmp_tempproduct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `slug` longtext NOT NULL,
  `description` longtext NOT NULL,
  `colors` longtext NOT NULL,
  `keywords` longtext NOT NULL,
  `old_category_id` int(11) DEFAULT NULL,
  `primary_category_id` int(11) DEFAULT NULL,
  `secondary_category_id` int(11) DEFAULT NULL,
  `created` date NOT NULL,
  `updated` date NOT NULL DEFAULT '2015-05-09',
  `last_updated_by_id` int(11) DEFAULT NULL,
  `recipients` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_tmp_tempproduct_af05e476` (`old_category_id`),
  KEY `product_tmp_tempproduct_8ede101f` (`primary_category_id`),
  KEY `product_tmp_tempproduct_9fbb9bdd` (`secondary_category_id`),
  KEY `product_tmp_tempproduct_65dff83` (`last_updated_by_id`),
  CONSTRAINT `last_updated_by_id_refs_id_414560df7e2d315e` FOREIGN KEY (`last_updated_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `old_category_id_refs_id_5708d4eda9a76f1b` FOREIGN KEY (`old_category_id`) REFERENCES `product_tmp_oldcategory` (`id`),
  CONSTRAINT `primary_category_id_refs_id_3b6781b49f43caa1` FOREIGN KEY (`primary_category_id`) REFERENCES `marketplace_category` (`id`),
  CONSTRAINT `secondary_category_id_refs_id_3b6781b49f43caa1` FOREIGN KEY (`secondary_category_id`) REFERENCES `marketplace_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_tmp_tempproduct`
--

LOCK TABLES `product_tmp_tempproduct` WRITE;
/*!40000 ALTER TABLE `product_tmp_tempproduct` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_tmp_tempproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_cart`
--

DROP TABLE IF EXISTS `purchase_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_cart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11),
  `created` date NOT NULL,
  `updated` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purchase_cart_user_id_19326ed7d2cd982c_uniq` (`user_id`),
  KEY `purchase_cart_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_3e3ee921a2b7ae15` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_cart`
--

LOCK TABLES `purchase_cart` WRITE;
/*!40000 ALTER TABLE `purchase_cart` DISABLE KEYS */;
INSERT INTO `purchase_cart` VALUES (1,1,'2015-05-09','2015-05-09'),(2,2,'2015-05-09','2015-05-09');
/*!40000 ALTER TABLE `purchase_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_cartproduct`
--

DROP TABLE IF EXISTS `purchase_cartproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_cartproduct` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cart_stall_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(10) unsigned NOT NULL,
  `unit_price` decimal(6,2) NOT NULL DEFAULT '0.00',
  `unit_price_currency` varchar(3) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_cartproduct_8f5e47f1` (`cart_stall_id`),
  KEY `purchase_cartproduct_bb420c12` (`product_id`),
  CONSTRAINT `product_id_refs_id_254ad1a8ff4de4fa` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`),
  CONSTRAINT `cart_stall_id_refs_id_666f17ddda146c4a` FOREIGN KEY (`cart_stall_id`) REFERENCES `purchase_cartstall` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_cartproduct`
--

LOCK TABLES `purchase_cartproduct` WRITE;
/*!40000 ALTER TABLE `purchase_cartproduct` DISABLE KEYS */;
INSERT INTO `purchase_cartproduct` VALUES (1,1,1,1,19.00,'GBP');
/*!40000 ALTER TABLE `purchase_cartproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_cartstall`
--

DROP TABLE IF EXISTS `purchase_cartstall`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_cartstall` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cart_id` int(11) NOT NULL,
  `stall_id` int(11) NOT NULL,
  `note` longtext NOT NULL,
  `checked_out` tinyint(1) NOT NULL DEFAULT '0',
  `checked_out_on` date DEFAULT NULL,
  `address_id` int(11),
  `speculative_country_id` int(11),
  `coupon_code` varchar(100),
  PRIMARY KEY (`id`),
  KEY `purchase_cartstall_129fc6a` (`cart_id`),
  KEY `purchase_cartstall_368109e5` (`stall_id`),
  KEY `purchase_cartstall_b213c1e9` (`address_id`),
  KEY `purchase_cartstall_6f25ac51` (`speculative_country_id`),
  CONSTRAINT `address_id_refs_id_43818af7c8fe3e9c` FOREIGN KEY (`address_id`) REFERENCES `accounts_shippingaddress` (`id`),
  CONSTRAINT `cart_id_refs_id_717ff9abc2acf630` FOREIGN KEY (`cart_id`) REFERENCES `purchase_cart` (`id`),
  CONSTRAINT `speculative_country_id_refs_id_314def579fe7a886` FOREIGN KEY (`speculative_country_id`) REFERENCES `marketplace_country` (`id`),
  CONSTRAINT `stall_id_refs_id_53a85810b5cd95d0` FOREIGN KEY (`stall_id`) REFERENCES `marketplace_stall` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_cartstall`
--

LOCK TABLES `purchase_cartstall` WRITE;
/*!40000 ALTER TABLE `purchase_cartstall` DISABLE KEYS */;
INSERT INTO `purchase_cartstall` VALUES (1,2,1,'',0,NULL,NULL,1,NULL);
/*!40000 ALTER TABLE `purchase_cartstall` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_lineitem`
--

DROP TABLE IF EXISTS `purchase_lineitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_lineitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `dispatched` tinyint(1) NOT NULL DEFAULT '0',
  `created` date NOT NULL,
  `updated` date NOT NULL,
  `quantity` int(10) unsigned NOT NULL,
  `price` decimal(6,2) NOT NULL DEFAULT '0.00',
  `price_currency` varchar(3) NOT NULL,
  `refund_id` int(11),
  PRIMARY KEY (`id`),
  KEY `purchase_lineitem_8337030b` (`order_id`),
  KEY `purchase_lineitem_bb420c12` (`product_id`),
  KEY `purchase_lineitem_af8d9d48` (`refund_id`),
  CONSTRAINT `refund_id_refs_id_50e955b0b929cd52` FOREIGN KEY (`refund_id`) REFERENCES `purchase_refund` (`id`),
  CONSTRAINT `order_id_refs_id_7d2f07a591a2e835` FOREIGN KEY (`order_id`) REFERENCES `purchase_order` (`id`),
  CONSTRAINT `product_id_refs_id_4bf5897f953b144b` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_lineitem`
--

LOCK TABLES `purchase_lineitem` WRITE;
/*!40000 ALTER TABLE `purchase_lineitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_lineitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_order`
--

DROP TABLE IF EXISTS `purchase_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `stall_id` int(11) NOT NULL,
  `created` date NOT NULL,
  `updated` date NOT NULL,
  `delivery_charge` decimal(6,2) NOT NULL DEFAULT '0.00',
  `delivery_charge_currency` varchar(3) NOT NULL,
  `address_id` int(11) NOT NULL DEFAULT '1',
  `is_joomla_order` tinyint(1) NOT NULL,
  `note` longtext NOT NULL,
  `discount_amount` decimal(6,2) NOT NULL,
  `discount_amount_currency` varchar(3) NOT NULL,
  `refund_reason` int(11),
  PRIMARY KEY (`id`),
  KEY `purchase_order_fbfc09f1` (`user_id`),
  KEY `purchase_order_368109e5` (`stall_id`),
  KEY `purchase_order_b213c1e9` (`address_id`),
  CONSTRAINT `address_id_refs_id_31bace2d22cbad00` FOREIGN KEY (`address_id`) REFERENCES `accounts_shippingaddress` (`id`),
  CONSTRAINT `stall_id_refs_id_6094321160fe0bac` FOREIGN KEY (`stall_id`) REFERENCES `marketplace_stall` (`id`),
  CONSTRAINT `user_id_refs_id_56d63fe215906de6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_order`
--

LOCK TABLES `purchase_order` WRITE;
/*!40000 ALTER TABLE `purchase_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_orderfeedback`
--

DROP TABLE IF EXISTS `purchase_orderfeedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_orderfeedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) DEFAULT NULL,
  `feedback_text` longtext NOT NULL,
  `created` date NOT NULL,
  `updated` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  CONSTRAINT `order_id_refs_id_4f7fed383e6a2fca` FOREIGN KEY (`order_id`) REFERENCES `purchase_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_orderfeedback`
--

LOCK TABLES `purchase_orderfeedback` WRITE;
/*!40000 ALTER TABLE `purchase_orderfeedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_orderfeedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_payment`
--

DROP TABLE IF EXISTS `purchase_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `secret_uuid` varchar(36) NOT NULL,
  `debug_request` longtext,
  `debug_response` longtext,
  `purchaser_id` int(11) NOT NULL,
  `pay_key` varchar(255) NOT NULL,
  `transaction_id` varchar(128) DEFAULT NULL,
  `status` varchar(200) NOT NULL,
  `status_detail` varchar(2048) NOT NULL,
  `order_id` int(11),
  `amount` decimal(6,2) NOT NULL DEFAULT '0.00',
  `amount_currency` varchar(3) NOT NULL,
  `logged_to_google` tinyint(1) NOT NULL,
  `discount_amount` decimal(6,2) NOT NULL,
  `discount_amount_currency` varchar(3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `purchase_payment_order_id_485e72d325f0f915_uniq` (`order_id`),
  KEY `purchase_payment_1e9fb4b8` (`purchaser_id`),
  CONSTRAINT `order_id_refs_id_3af0451e018536b3` FOREIGN KEY (`order_id`) REFERENCES `purchase_order` (`id`),
  CONSTRAINT `purchaser_id_refs_id_3924137335b5821e` FOREIGN KEY (`purchaser_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_payment`
--

LOCK TABLES `purchase_payment` WRITE;
/*!40000 ALTER TABLE `purchase_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_paymentattempt`
--

DROP TABLE IF EXISTS `purchase_paymentattempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_paymentattempt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cart_stall_id` int(11),
  `payment_id` int(11) NOT NULL,
  `created` date NOT NULL,
  `updated` date NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `payment_id` (`payment_id`),
  KEY `purchase_paymentattempt_8f5e47f1` (`cart_stall_id`),
  CONSTRAINT `cart_stall_id_refs_id_27d198801e87602b` FOREIGN KEY (`cart_stall_id`) REFERENCES `purchase_cartstall` (`id`),
  CONSTRAINT `payment_id_refs_id_616007024afcfd03` FOREIGN KEY (`payment_id`) REFERENCES `purchase_payment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_paymentattempt`
--

LOCK TABLES `purchase_paymentattempt` WRITE;
/*!40000 ALTER TABLE `purchase_paymentattempt` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_paymentattempt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_paymentreturnredirect`
--

DROP TABLE IF EXISTS `purchase_paymentreturnredirect`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_paymentreturnredirect` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `payment_already_processed` tinyint(1) NOT NULL DEFAULT '1',
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_paymentreturnredirect_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_105697948866470a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_paymentreturnredirect`
--

LOCK TABLES `purchase_paymentreturnredirect` WRITE;
/*!40000 ALTER TABLE `purchase_paymentreturnredirect` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_paymentreturnredirect` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase_refund`
--

DROP TABLE IF EXISTS `purchase_refund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `purchase_refund` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` date NOT NULL,
  `updated` date NOT NULL,
  `reason` varchar(200) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_refund_8337030b` (`order_id`),
  CONSTRAINT `order_id_refs_id_133f6585d64a738c` FOREIGN KEY (`order_id`) REFERENCES `purchase_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_refund`
--

LOCK TABLES `purchase_refund` WRITE;
/*!40000 ALTER TABLE `purchase_refund` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase_refund` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sem_activecampaignid`
--

DROP TABLE IF EXISTS `sem_activecampaignid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sem_activecampaignid` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sem_activecampaignid`
--

LOCK TABLES `sem_activecampaignid` WRITE;
/*!40000 ALTER TABLE `sem_activecampaignid` DISABLE KEYS */;
/*!40000 ALTER TABLE `sem_activecampaignid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sem_productadwords`
--

DROP TABLE IF EXISTS `sem_productadwords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sem_productadwords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `ad_group_id` varchar(30) NOT NULL,
  `status` varchar(40) NOT NULL DEFAULT 'ENABLED',
  `campaign_id` varchar(30) DEFAULT NULL,
  `cost` int(10) unsigned DEFAULT NULL,
  `average_cpc` int(10) unsigned DEFAULT NULL,
  `profit_banked` decimal(6,2) DEFAULT NULL,
  `profit_banked_currency` varchar(3) NOT NULL DEFAULT 'GBP',
  `clicks` smallint(5) unsigned DEFAULT NULL,
  `impressions` int(10) unsigned DEFAULT NULL,
  `conversions` smallint(5) unsigned DEFAULT NULL,
  `total_sales` smallint(5) unsigned DEFAULT NULL,
  `datetime_added` datetime NOT NULL,
  `datetime_updated` datetime NOT NULL,
  `velocity` decimal(4,2) NOT NULL,
  `max_cpc` decimal(4,2) NOT NULL,
  `max_cpc_currency` varchar(3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sem_productadwords_product_id_123b924cc05e97b0_uniq` (`product_id`,`ad_group_id`),
  KEY `sem_productadwords_bb420c12` (`product_id`),
  CONSTRAINT `product_id_refs_id_736216d28742f89e` FOREIGN KEY (`product_id`) REFERENCES `marketplace_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sem_productadwords`
--

LOCK TABLES `sem_productadwords` WRITE;
/*!40000 ALTER TABLE `sem_productadwords` DISABLE KEYS */;
/*!40000 ALTER TABLE `sem_productadwords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seo_metadatamodel`
--

DROP TABLE IF EXISTS `seo_metadatamodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seo_metadatamodel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `keywords` varchar(511) NOT NULL,
  `canonical_url` varchar(511) NOT NULL,
  `og_title` varchar(511) NOT NULL,
  `og_description` varchar(511) NOT NULL,
  `og_type` varchar(511) NOT NULL,
  `og_image` varchar(511) NOT NULL,
  `og_url` varchar(511) NOT NULL,
  `og_video` varchar(511) NOT NULL,
  `sailthru_tags` varchar(511) NOT NULL,
  `sailthru_image` varchar(511) NOT NULL,
  `sailthru_image_thumb` varchar(511) NOT NULL,
  `sailthru_title` varchar(511) NOT NULL,
  `sailthru_stall_title` varchar(511) NOT NULL,
  `sailthru_stall_url` varchar(511) NOT NULL,
  `sailthru_stall_owner_id` varchar(511) NOT NULL,
  `_content_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_content_type_id` (`_content_type_id`),
  CONSTRAINT `_content_type_id_refs_id_3be4e6eb` FOREIGN KEY (`_content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seo_metadatamodel`
--

LOCK TABLES `seo_metadatamodel` WRITE;
/*!40000 ALTER TABLE `seo_metadatamodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `seo_metadatamodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seo_metadatamodelinstance`
--

DROP TABLE IF EXISTS `seo_metadatamodelinstance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seo_metadatamodelinstance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `keywords` varchar(511) NOT NULL,
  `canonical_url` varchar(511) NOT NULL,
  `og_title` varchar(511) NOT NULL,
  `og_description` varchar(511) NOT NULL,
  `og_type` varchar(511) NOT NULL,
  `og_image` varchar(511) NOT NULL,
  `og_url` varchar(511) NOT NULL,
  `og_video` varchar(511) NOT NULL,
  `sailthru_tags` varchar(511) NOT NULL,
  `sailthru_image` varchar(511) NOT NULL,
  `sailthru_image_thumb` varchar(511) NOT NULL,
  `sailthru_title` varchar(511) NOT NULL,
  `sailthru_stall_title` varchar(511) NOT NULL,
  `sailthru_stall_url` varchar(511) NOT NULL,
  `sailthru_stall_owner_id` varchar(511) NOT NULL,
  `_path` varchar(255) NOT NULL,
  `_content_type_id` int(11) NOT NULL,
  `_object_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_path` (`_path`),
  UNIQUE KEY `_path_2` (`_path`),
  UNIQUE KEY `_content_type_id` (`_content_type_id`,`_object_id`),
  CONSTRAINT `_content_type_id_refs_id_19fb79c8` FOREIGN KEY (`_content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seo_metadatamodelinstance`
--

LOCK TABLES `seo_metadatamodelinstance` WRITE;
/*!40000 ALTER TABLE `seo_metadatamodelinstance` DISABLE KEYS */;
INSERT INTO `seo_metadatamodelinstance` VALUES (1,'','','','','','','','','','','','','','','','','','/blog/2015/ministerio-de-cultura-implementa-proyecto-de-trans/',72,1),(2,'','','','','','','','','','','','','','','','','','/blog/2015/ganador-concurso-elaboracion-joyas-julio-2011-toca/',72,2),(3,'','','','','','','','','','','','','','','','','','/blog/2015/aromaterapia-una-alternativa-saludable/',72,3),(4,'','','','','','','','','','','','','','','','','','/blog/2015/hidromiel-la-bebida-de-los-dioses/',72,4);
/*!40000 ALTER TABLE `seo_metadatamodelinstance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seo_metadatapath`
--

DROP TABLE IF EXISTS `seo_metadatapath`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seo_metadatapath` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `keywords` varchar(511) NOT NULL,
  `canonical_url` varchar(511) NOT NULL,
  `og_title` varchar(511) NOT NULL,
  `og_description` varchar(511) NOT NULL,
  `og_type` varchar(511) NOT NULL,
  `og_image` varchar(511) NOT NULL,
  `og_url` varchar(511) NOT NULL,
  `og_video` varchar(511) NOT NULL,
  `sailthru_tags` varchar(511) NOT NULL,
  `sailthru_image` varchar(511) NOT NULL,
  `sailthru_image_thumb` varchar(511) NOT NULL,
  `sailthru_title` varchar(511) NOT NULL,
  `sailthru_stall_title` varchar(511) NOT NULL,
  `sailthru_stall_url` varchar(511) NOT NULL,
  `sailthru_stall_owner_id` varchar(511) NOT NULL,
  `_path` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_path` (`_path`),
  UNIQUE KEY `_path_2` (`_path`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seo_metadatapath`
--

LOCK TABLES `seo_metadatapath` WRITE;
/*!40000 ALTER TABLE `seo_metadatapath` DISABLE KEYS */;
/*!40000 ALTER TABLE `seo_metadatapath` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seo_metadataview`
--

DROP TABLE IF EXISTS `seo_metadataview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seo_metadataview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `keywords` varchar(511) NOT NULL,
  `canonical_url` varchar(511) NOT NULL,
  `og_title` varchar(511) NOT NULL,
  `og_description` varchar(511) NOT NULL,
  `og_type` varchar(511) NOT NULL,
  `og_image` varchar(511) NOT NULL,
  `og_url` varchar(511) NOT NULL,
  `og_video` varchar(511) NOT NULL,
  `sailthru_tags` varchar(511) NOT NULL,
  `sailthru_image` varchar(511) NOT NULL,
  `sailthru_image_thumb` varchar(511) NOT NULL,
  `sailthru_title` varchar(511) NOT NULL,
  `sailthru_stall_title` varchar(511) NOT NULL,
  `sailthru_stall_url` varchar(511) NOT NULL,
  `sailthru_stall_owner_id` varchar(511) NOT NULL,
  `_view` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_view` (`_view`),
  UNIQUE KEY `_view_2` (`_view`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seo_metadataview`
--

LOCK TABLES `seo_metadataview` WRITE;
/*!40000 ALTER TABLE `seo_metadataview` DISABLE KEYS */;
/*!40000 ALTER TABLE `seo_metadataview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_association`
--

DROP TABLE IF EXISTS `social_auth_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` varchar(255) NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_association_handle_693a924207fa6ae_uniq` (`handle`,`server_url`),
  KEY `social_auth_association_5a32b972` (`issued`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_association`
--

LOCK TABLES `social_auth_association` WRITE;
/*!40000 ALTER TABLE `social_auth_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_nonce`
--

DROP TABLE IF EXISTS `social_auth_nonce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_nonce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_nonce_timestamp_3833ba21ef52524a_uniq` (`timestamp`,`salt`,`server_url`),
  KEY `social_auth_nonce_67f1b7ce` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_nonce`
--

LOCK TABLES `social_auth_nonce` WRITE;
/*!40000 ALTER TABLE `social_auth_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_nonce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_usersocialauth`
--

DROP TABLE IF EXISTS `social_auth_usersocialauth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_usersocialauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `provider` varchar(32) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `extra_data` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_usersocialauth_provider_2f763109e2c4a1fb_uniq` (`provider`,`uid`),
  KEY `social_auth_usersocialauth_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_529c317860fa311b` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_usersocialauth`
--

LOCK TABLES `social_auth_usersocialauth` WRITE;
/*!40000 ALTER TABLE `social_auth_usersocialauth` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_usersocialauth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_network_userfollow`
--

DROP TABLE IF EXISTS `social_network_userfollow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_network_userfollow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `target_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `social_network_userfollow_fbfc09f1` (`user_id`),
  KEY `social_network_userfollow_9358c897` (`target_id`),
  CONSTRAINT `target_id_refs_id_552f4ec8097c44a2` FOREIGN KEY (`target_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `user_id_refs_id_552f4ec8097c44a2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_network_userfollow`
--

LOCK TABLES `social_network_userfollow` WRITE;
/*!40000 ALTER TABLE `social_network_userfollow` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_network_userfollow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `south_migrationhistory`
--

DROP TABLE IF EXISTS `south_migrationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=220 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `south_migrationhistory`
--

LOCK TABLES `south_migrationhistory` WRITE;
/*!40000 ALTER TABLE `south_migrationhistory` DISABLE KEYS */;
INSERT INTO `south_migrationhistory` VALUES (1,'social_auth','0001_initial','2015-05-09 15:12:22'),(2,'social_auth','0002_auto__add_unique_nonce_timestamp_salt_server_url__add_unique_associati','2015-05-09 15:12:23'),(3,'easy_thumbnails','0001_initial','2015-05-09 15:12:25'),(4,'easy_thumbnails','0002_filename_indexes','2015-05-09 15:12:26'),(5,'easy_thumbnails','0003_auto__add_storagenew','2015-05-09 15:12:26'),(6,'easy_thumbnails','0004_auto__add_field_source_storage_new__add_field_thumbnail_storage_new','2015-05-09 15:12:28'),(7,'easy_thumbnails','0005_storage_fks_null','2015-05-09 15:12:30'),(8,'easy_thumbnails','0006_copy_storage','2015-05-09 15:12:30'),(9,'easy_thumbnails','0007_storagenew_fks_not_null','2015-05-09 15:12:32'),(10,'easy_thumbnails','0008_auto__del_field_source_storage__del_field_thumbnail_storage','2015-05-09 15:12:33'),(11,'easy_thumbnails','0009_auto__del_storage','2015-05-09 15:12:33'),(12,'easy_thumbnails','0010_rename_storage','2015-05-09 15:12:36'),(13,'easy_thumbnails','0011_auto__add_field_source_storage_hash__add_field_thumbnail_storage_hash','2015-05-09 15:12:37'),(14,'easy_thumbnails','0012_build_storage_hashes','2015-05-09 15:12:37'),(15,'easy_thumbnails','0013_auto__del_storage__del_field_source_storage__del_field_thumbnail_stora','2015-05-09 15:12:39'),(16,'easy_thumbnails','0014_auto__add_unique_source_name_storage_hash__add_unique_thumbnail_name_s','2015-05-09 15:12:40'),(17,'easy_thumbnails','0015_auto__del_unique_thumbnail_name_storage_hash__add_unique_thumbnail_sou','2015-05-09 15:12:41'),(18,'django_cron','0001_initial','2015-05-09 15:12:43'),(19,'django_cron','0002_auto__add_field_cronjoblog_ran_at_time','2015-05-09 15:12:45'),(20,'marketplace','0001_initial','2015-05-09 15:13:10'),(21,'marketplace','0002_add_thumbs_field','2015-05-09 15:13:11'),(22,'marketplace','0003_add_shipping_profiles','2015-05-09 15:13:13'),(23,'marketplace','0004_add_shipping_profiles','2015-05-09 15:13:15'),(24,'marketplace','0005_shipping_profiles','2015-05-09 15:13:25'),(25,'purchase','0001_initial','2015-05-09 15:13:35'),(26,'purchase','0002_auto__add_field_cartstall_address','2015-05-09 15:13:36'),(27,'purchase','0003_add_shipping_address_to_cartstall','2015-05-09 15:13:36'),(28,'purchase','0004_auto__del_field_shippingaddress_cart_stall','2015-05-09 15:13:37'),(29,'accounts','0001_initial','2015-05-09 15:13:38'),(30,'accounts','0002_add_shippingaddress','2015-05-09 15:13:38'),(31,'accounts','0003_auto__add_field_userprofile_is_publicly_viewable','2015-05-09 15:13:39'),(32,'accounts','0004_auto__del_field_userprofile_is_publicly_viewable','2015-05-09 15:13:40'),(33,'accounts','0005_auto__add_field_userprofile_country_new','2015-05-09 15:13:41'),(34,'accounts','0006_link_countries','2015-05-09 15:13:41'),(35,'accounts','0007_auto__del_field_userprofile_country','2015-05-09 15:13:41'),(36,'accounts','0008_rename_country_new_to_country','2015-05-09 15:13:42'),(37,'accounts','0009_auto__del_field_userprofile_country_new__chg_field_userprofile_country','2015-05-09 15:13:43'),(38,'accounts','0010_auto__add_field_shippingaddress_country_new','2015-05-09 15:13:44'),(39,'accounts','0011_populate_country_on_shippingaddress','2015-05-09 15:13:44'),(40,'accounts','0012_auto__del_field_shippingaddress_country','2015-05-09 15:13:44'),(41,'accounts','0013_rename_country_new_to_country','2015-05-09 15:13:45'),(42,'accounts','0014_auto__chg_field_shippingaddress_country','2015-05-09 15:13:46'),(43,'accounts','0015_add_data_field_to_profile','2015-05-09 15:13:47'),(44,'accounts','0016_social_auth','2015-05-09 15:13:48'),(45,'accounts','0017_facebookvideo','2015-05-09 15:13:48'),(46,'accounts','0018_auto__add_field_userprofile_activation_key_date','2015-05-09 15:13:49'),(47,'accounts','0019_auto__add_field_userprofile_last_activities_update','2015-05-09 15:13:51'),(48,'accounts','0020_auto__add_field_emailnotification_share_orders_in_activity_feed','2015-05-09 15:13:52'),(49,'accounts','0021_auto__add_field_userprofile_preferred_currency','2015-05-09 15:13:52'),(50,'accounts','0022_auto__add_field_userprofile_detected_country','2015-05-09 15:13:53'),(51,'accounts','0023_auto__add_field_shippingaddress_last_select_date_time','2015-05-09 15:13:54'),(52,'accounts','0024_add_blog_posts','2015-05-09 15:13:55'),(53,'accounts','0025_auto','2015-05-09 15:13:57'),(54,'accounts','0026_auto__add_field_emailnotification_product_discounts','2015-05-09 15:13:57'),(55,'accounts','0027_rename_notification_fields','2015-05-09 15:13:59'),(56,'accounts','0028_auto__add_field_userprofile_activities_last_checked_at','2015-05-09 15:13:59'),(57,'accounts','0029_auto__add_field_userprofile_phone_number','2015-05-09 15:14:00'),(58,'accounts','0030_auto__add_sellerstatuslog','2015-05-09 15:14:00'),(59,'accounts','0031_auto__del_sellerstatuslog','2015-05-09 15:14:01'),(60,'accounts','0032_auto__add_video__add_videotype','2015-05-09 15:14:03'),(61,'accounts','0033_auto__add_field_videotype_time_limit','2015-05-09 15:14:03'),(62,'lovelists','0001_initial','2015-05-09 15:14:10'),(63,'lovelists','0002_auto__add_field_lovelist_promoted','2015-05-09 15:14:11'),(64,'lovelists','0003_auto__add_promotionscheduler','2015-05-09 15:14:12'),(65,'main','0001_initial','2015-05-09 15:14:14'),(66,'main','0002_seo_rename_from_marketplace','2015-05-09 15:14:14'),(67,'main','0003_seo_auto__add_field_metadatas_sailthru_path','2015-05-09 15:14:14'),(68,'main','0004_seo_add_field_metadatas_sailthru','2015-05-09 15:14:14'),(69,'marketplace','0006_add_profile_rule_prices','2015-05-09 15:14:17'),(70,'marketplace','0007_add_suggested_certificates','2015-05-09 15:14:21'),(71,'marketplace','0008_adding_certificate_url','2015-05-09 15:14:22'),(72,'marketplace','0009_shifted_price_key_to_product','2015-05-09 15:14:23'),(73,'marketplace','0010_adding_is_chat_enabled','2015-05-09 15:14:24'),(74,'marketplace','0011_reverted_price_product_model_changed_price_amount','2015-05-09 15:14:27'),(75,'marketplace','0012_remove_superfluous_price_fields','2015-05-09 15:14:28'),(76,'marketplace','0013_make_shipping_rule_fields_required','2015-05-09 15:14:29'),(77,'marketplace','0014_adding_numeric_identifier','2015-05-09 15:14:30'),(78,'marketplace','0015_adding_gaglers_uri','2015-05-09 15:14:31'),(79,'marketplace','0016_adding_email_opt_in','2015-05-09 15:14:32'),(80,'marketplace','0017_add_cause_key_to_certificates_make_price_required','2015-05-09 15:14:34'),(81,'marketplace','0018_add_image_to_certificate','2015-05-09 15:14:36'),(82,'marketplace','0019_add_publication_date_convert_create_and_modify_to_datetime','2015-05-09 15:14:37'),(83,'marketplace','0020_increase_filepath_lengths','2015-05-09 15:14:38'),(84,'marketplace','0021_add_stall_video','2015-05-09 15:14:39'),(85,'marketplace','0022_adding_max_delivery_time','2015-05-09 15:14:39'),(86,'marketplace','0023_adding_worldwide_delivery_times','2015-05-09 15:14:40'),(87,'marketplace','0024_allow_null_for_worldwide_delivery','2015-05-09 15:14:41'),(88,'marketplace','0025_make_rule_price_extra_required','2015-05-09 15:14:41'),(89,'marketplace','0026_make_rule_price_extra_required_2','2015-05-09 15:14:42'),(90,'marketplace','0027_uniqueslug','2015-05-09 15:14:42'),(91,'marketplace','0028_replace_duplicates','2015-05-09 15:14:42'),(92,'marketplace','0029_auto__add_unique_titles','2015-05-09 15:14:44'),(93,'marketplace','0030_populate_missing_product_descriptions_with_titles','2015-05-09 15:14:44'),(94,'marketplace','0030_seo_auto_add_canonical_url','2015-05-09 15:14:44'),(95,'marketplace','0031_replace_commas_in_keywords_with_multiple_keywords','2015-05-09 15:14:45'),(96,'marketplace','0032_copy_ingredients_and_materials_to_keywords','2015-05-09 15:14:45'),(97,'marketplace','0033_auto__add_field_category_description','2015-05-09 15:14:45'),(98,'marketplace','0034_auto__add_field_category_image_src','2015-05-09 15:14:46'),(99,'marketplace','0035_auto__add_field_product_number_of_sales','2015-05-09 15:14:47'),(100,'marketplace','0036_auto__add_field_category_seo_title','2015-05-09 15:14:48'),(101,'marketplace','0037_auto__chg_field_category_seo_title__chg_field_category_description','2015-05-09 15:14:48'),(102,'marketplace','0038_seo_auto__chg_field_marketplacemetadata_description','2015-05-09 15:14:49'),(103,'marketplace','0039_auto__add_field_recipient_seo_title__add_field_material_seo_title__add','2015-05-09 15:14:52'),(104,'marketplace','0040_auto__add_field_product_number_of_recent_sales','2015-05-09 15:14:53'),(105,'marketplace','0041_auto__add_fields_stall_phone_landline_and_phone_mobile','2015-05-09 15:14:55'),(106,'marketplace','0042_migrate_old_phone_number','2015-05-09 15:14:56'),(107,'marketplace','0043_auto__del_field_stall_phone_number','2015-05-09 15:14:56'),(108,'marketplace','0044_auto__chg_field_productimage_slug','2015-05-09 15:14:57'),(109,'marketplace','0045_auto__add_currencyexchangerate','2015-05-09 15:14:57'),(110,'marketplace','0046_auto__add_field_category_navigation_name','2015-05-09 15:14:58'),(111,'marketplace','0047_auto__add_field_stall_renewal_tier__add_field_stall_is_suspended__add_','2015-05-09 15:15:00'),(112,'marketplace','0048_auto__add_stallstatuslog','2015-05-09 15:15:01'),(113,'marketplace','0049_auto__add_field_stall_total_gmv_till_yesterday__add_field_stall_total_','2015-05-09 15:15:03'),(114,'marketplace','0050_auto__add_field_stall_total_suspensions_till_yesterday','2015-05-09 15:15:04'),(115,'marketplace','0051_auto__del_field_stall_total_gmv_till_yesterday_currency__chg_field_sta','2015-05-09 15:15:05'),(116,'marketplace','0052_auto__add_field_stall_is_closed','2015-05-09 15:15:06'),(117,'marketplace','0053_auto__add_stallcallnotes__add_field_stall_total_products_till_yesterda','2015-05-09 15:15:11'),(118,'marketplace','0054_auto__chg_field_stallstatuslog_reason_for_suspension','2015-05-09 15:15:12'),(119,'marketplace','0055_auto__add_field_product_flag','2015-05-09 15:15:13'),(120,'marketplace','0056_auto__add_field_stall_days_to_next_stockcheck_till_yesterday','2015-05-09 15:15:14'),(121,'marketplace','0057_auto__add_field_stall_is_in_video_beta','2015-05-09 15:15:15'),(122,'messaging','0001_initial','2015-05-09 15:15:20'),(123,'messaging','0002_auto__add_bannedword','2015-05-09 15:15:20'),(124,'messaging','0003_auto__del_bannedword','2015-05-09 15:15:20'),(125,'purchase','0005__del_shippingaddress__chg_field_cartstall_address','2015-05-09 15:15:22'),(126,'purchase','0006_auto__add_lineitem__add_orderfeedback__add_order__add_refund','2015-05-09 15:15:27'),(127,'purchase','0007_auto__add_field_lineitem_quantity','2015-05-09 15:15:28'),(128,'purchase','0008_auto__add_field_order_delivery_charge__add_field_order_delivery_charge','2015-05-09 15:15:29'),(129,'purchase','0009_delete_payments','2015-05-09 15:15:29'),(130,'purchase','0010_auto__del_field_payment_cart_stall__add_field_payment_order','2015-05-09 15:15:30'),(131,'purchase','0011_auto__add_field_payment_amount__add_field_payment_amount_currency','2015-05-09 15:15:31'),(132,'purchase','0012_auto__chg_field_payment_order__del_unique_payment_order','2015-05-09 15:15:33'),(133,'purchase','0013_auto__add_field_cartstall_order','2015-05-09 15:15:34'),(134,'purchase','0014_auto__del_field_lineitem_price','2015-05-09 15:15:35'),(135,'purchase','0015_auto__add_field_lineitem_price__add_field_lineitem_price_currency','2015-05-09 15:15:36'),(136,'purchase','0016_auto__chg_field_cartstall_order__add_unique_cartstall_order','2015-05-09 15:15:37'),(137,'purchase','0017_auto__add_field_refund_reason','2015-05-09 15:15:37'),(138,'purchase','0018_auto__add_field_lineitem_refund__del_field_refund_line_item','2015-05-09 15:15:39'),(139,'purchase','0019_auto__add_field_refund_order','2015-05-09 15:15:41'),(140,'purchase','0020_auto__chg_field_payment_order__add_unique_payment_order','2015-05-09 15:15:44'),(141,'purchase','0021_delete_carts','2015-05-09 15:15:44'),(142,'purchase','0022_auto__chg_field_cart_user__add_unique_cart_user','2015-05-09 15:15:46'),(143,'purchase','0023_create_carts','2015-05-09 15:15:46'),(144,'purchase','0024_auto__add_field_order_address','2015-05-09 15:15:47'),(145,'purchase','0025_auto__chg_field_order_address','2015-05-09 15:15:48'),(146,'purchase','0026_auto__add_field_cartstall_speculative_country','2015-05-09 15:15:49'),(147,'purchase','0027_auto__chg_field_payment_status','2015-05-09 15:15:50'),(148,'purchase','0028_auto__add_paymentattempt','2015-05-09 15:15:51'),(149,'purchase','0029_auto__chg_field_payment_order__del_field_cartstall_order__chg_field_pa','2015-05-09 15:15:54'),(150,'purchase','0030_auto__chg_field_paymentattempt_cart_stall__add_field_order_is_joomla_o','2015-05-09 15:15:56'),(151,'purchase','0031_auto__chg_field_payment_amount__chg_field_lineitem_price__chg_field_or','2015-05-09 15:15:57'),(152,'purchase','0032_auto__add_field_order_note','2015-05-09 15:15:57'),(153,'purchase','0033_auto__add_field_payment_logged_to_google','2015-05-09 15:15:58'),(154,'purchase','0034_auto__chg_field_cart_user','2015-05-09 15:15:59'),(155,'purchase','0035_auto__add_field_cartstall_coupon_code','2015-05-09 15:15:59'),(156,'purchase','0036_auto__add_field_order_discount_amount__add_field_order_discount_amount','2015-05-09 15:16:00'),(157,'purchase','0037_auto__add_field_payment_discount_amount__add_field_payment_discount_am','2015-05-09 15:16:02'),(158,'purchase','0038_auto__add_paymentreturnredirect','2015-05-09 15:16:02'),(159,'purchase','0039_auto__add_field_order_refund_reason','2015-05-09 15:16:03'),(160,'articles','0001_initial','2015-05-09 15:16:17'),(161,'articles','0002_auto__add_field_article_created_at__add_field_article_updated_at','2015-05-09 15:16:19'),(162,'articles','0003_auto','2015-05-09 15:16:21'),(163,'articles','0004_auto__add_field_article_custom_unique_id','2015-05-09 15:16:22'),(164,'articles','0005_auto__add_field_article_seo_keyword__add_field_article_seo_meta_title','2015-05-09 15:16:24'),(165,'articles','0006_add_is_featured','2015-05-09 15:16:24'),(166,'articles','0007_auto__chg_field_attachment_attachment','2015-05-09 15:16:25'),(167,'image_crop','0001_initial','2015-05-09 15:16:27'),(168,'image_crop','0002_auto__del_field_tempimage_standardized__add_field_tempimage_standard','2015-05-09 15:16:30'),(169,'image_crop','0003_auto__add_field_tempimage_uuid','2015-05-09 15:16:31'),(170,'image_crop','0004_increasing_filepath_length','2015-05-09 15:16:32'),(171,'image_crop','0005_added_created_and_tag','2015-05-09 15:16:33'),(172,'spamish','0001_initial','2015-05-09 15:16:34'),(173,'threadedcomments','0001_initial','2015-05-09 15:16:40'),(174,'threadedcomments','0002_move_from_contrib_comments','2015-05-09 15:16:40'),(175,'threadedcomments','0003_auto__add_threadedcommentflag','2015-05-09 15:16:43'),(176,'threadedcomments','0004_migrate_comment_flags','2015-05-09 15:16:43'),(177,'threadedcomments','0005_set_tree_ids','2015-05-09 15:16:44'),(178,'mailing_lists','0001_initial','2015-05-09 15:16:46'),(179,'mailing_lists','0002_auto__add_field_mailinglistsignup_source__add_field_mailinglistsignup_','2015-05-09 15:16:47'),(180,'mailing_lists','0003_auto__add_field_mailinglistsignup_member_type','2015-05-09 15:16:48'),(181,'mailing_lists','0004_auto__chg_field_mailinglistsignup_category','2015-05-09 15:16:50'),(182,'mailing_lists','0005_auto__add_batchjob','2015-05-09 15:16:58'),(183,'mailing_lists','0006_auto__add_field_mailinglistsignup_is_seller_lead','2015-05-09 15:16:59'),(184,'mailing_lists','0007_populate_is_seller_lead','2015-05-09 15:16:59'),(185,'mailing_lists','0008_auto__add_field_mailinglistsignup_ip_address','2015-05-09 15:16:59'),(186,'mailing_lists','0009_register_page_source','2015-05-09 15:17:00'),(187,'mailing_lists','0010_auto__add_deletedemail','2015-05-09 15:17:01'),(188,'mailing_lists','0011_add_marketing_optin','2015-05-09 15:17:02'),(189,'social_network','0001_initial','2015-05-09 15:17:06'),(190,'analytics','0001_initial','2015-05-09 15:17:07'),(191,'analytics','0002_auto__chg_field_campaigntrack_source','2015-05-09 15:17:08'),(192,'analytics','0003_auto__chg_field_campaigntrack_term__chg_field_campaigntrack_medium__ch','2015-05-09 15:17:11'),(193,'analytics','0004_auto__add_field_campaigntrack_query_string__chg_field_campaigntrack_na','2015-05-09 15:17:13'),(194,'analytics','0005_auto__add_aggregatedata','2015-05-09 15:17:14'),(195,'analytics','0006_auto__del_field_aggregatedata_acquired_till_yesterday','2015-05-09 15:17:17'),(196,'analytics','0007_auto__add_field_campaigntrack_email_lead__chg_field_campaigntrack_user','2015-05-09 15:17:20'),(197,'analytics','0008_auto__add_lifetimetrack__add_field_campaigntrack_cookie','2015-05-09 15:17:24'),(198,'analytics','0009_auto__add_field_lifetimetrack_url_count','2015-05-09 15:17:24'),(199,'analytics','0010_auto__add_field_lifetimetrack_actual_activated_at__add_field_lifetimet','2015-05-09 15:17:26'),(200,'analytics','0011_auto__add_field_aggregatedata_order_count','2015-05-09 15:17:27'),(201,'analytics','0012_auto__add_productformerrors','2015-05-09 15:17:30'),(202,'analytics','0013_auto__del_field_productformerrors_rules_error__add_field_productformer','2015-05-09 15:17:31'),(203,'discounts','0001_initial','2015-05-09 15:17:34'),(204,'discounts','0002_auto__add_placampaign','2015-05-09 15:17:39'),(205,'discounts','0003_auto__add_freeshipping','2015-05-09 15:17:43'),(206,'sem','0001_initial','2015-05-09 15:17:47'),(207,'sem','0002_auto__add_activecampaignid__add_field_adwordslabel_label_id__add_uniqu','2015-05-09 15:17:53'),(208,'sem','0003_auto__del_adwordsoperations__del_adwordslabel__del_field_productadword','2015-05-09 15:17:54'),(209,'product_tmp','0001_initial','2015-05-09 15:18:00'),(210,'product_tmp','0002_auto__add_field_tempproduct_recipient','2015-05-09 15:18:01'),(211,'product_tmp','0003_auto__add_field_tempproduct_last_updated_by','2015-05-09 15:18:03'),(212,'product_tmp','0004_auto__del_field_tempproduct_recipient__add_field_tempproduct_recipient','2015-05-09 15:18:05'),(213,'actstream','0001_initial','2015-05-09 15:18:10'),(214,'actstream','0002_auto__chg_field_action_timestamp','2015-05-09 15:18:11'),(215,'actstream','0003_text_field_ids','2015-05-09 15:18:11'),(216,'actstream','0004_char_field_ids','2015-05-09 15:18:13'),(217,'actstream','0005_auto__add_field_follow_actor_only','2015-05-09 15:18:13'),(218,'actstream','0006_auto__add_field_action_data','2015-05-09 15:18:14'),(219,'actstream','0007_auto__add_field_follow_started','2015-05-09 15:18:15');
/*!40000 ALTER TABLE `south_migrationhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spamish_bannedword`
--

DROP TABLE IF EXISTS `spamish_bannedword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spamish_bannedword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(255) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spamish_bannedword`
--

LOCK TABLES `spamish_bannedword` WRITE;
/*!40000 ALTER TABLE `spamish_bannedword` DISABLE KEYS */;
/*!40000 ALTER TABLE `spamish_bannedword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `threadedcomments_threadedcomment`
--

DROP TABLE IF EXISTS `threadedcomments_threadedcomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `threadedcomments_threadedcomment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content_type_id` int(11) NOT NULL,
  `object_pk` longtext NOT NULL,
  `site_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `comment` longtext NOT NULL,
  `submit_date` datetime NOT NULL,
  `ip_address` char(15) DEFAULT NULL,
  `is_public` tinyint(1) NOT NULL DEFAULT '1',
  `is_removed` tinyint(1) NOT NULL DEFAULT '0',
  `post_to_facebook` tinyint(1) NOT NULL DEFAULT '0',
  `parent_id` int(11) DEFAULT NULL,
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `threadedcomments_threadedcomment_e4470c6e` (`content_type_id`),
  KEY `threadedcomments_threadedcomment_6223029` (`site_id`),
  KEY `threadedcomments_threadedcomment_fbfc09f1` (`user_id`),
  KEY `threadedcomments_threadedcomment_63f17a16` (`parent_id`),
  KEY `threadedcomments_threadedcomment_42b06ff6` (`lft`),
  KEY `threadedcomments_threadedcomment_91543e5a` (`rght`),
  KEY `threadedcomments_threadedcomment_efd07f28` (`tree_id`),
  KEY `threadedcomments_threadedcomment_2a8f42e8` (`level`),
  CONSTRAINT `parent_id_refs_id_791b9bc27ef2a789` FOREIGN KEY (`parent_id`) REFERENCES `threadedcomments_threadedcomment` (`id`),
  CONSTRAINT `content_type_id_refs_id_78a4a735af49ca3a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `site_id_refs_id_6f5af78dbc37c1f3` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`),
  CONSTRAINT `user_id_refs_id_1911788603c567b6` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `threadedcomments_threadedcomment`
--

LOCK TABLES `threadedcomments_threadedcomment` WRITE;
/*!40000 ALTER TABLE `threadedcomments_threadedcomment` DISABLE KEYS */;
INSERT INTO `threadedcomments_threadedcomment` VALUES (1,72,'1',1,2,' Excelente artículo','2015-05-09 20:24:49','127.0.0.1',1,0,0,NULL,1,2,1,0),(2,72,'2',1,2,' HeyThats great','2015-05-09 20:31:42','127.0.0.1',1,0,0,NULL,1,2,2,0);
/*!40000 ALTER TABLE `threadedcomments_threadedcomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `threadedcomments_threadedcommentflag`
--

DROP TABLE IF EXISTS `threadedcomments_threadedcommentflag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `threadedcomments_threadedcommentflag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `flag` varchar(30) NOT NULL,
  `flag_date` datetime NOT NULL,
  `comment_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `threadedcomments_threadedcommentf_user_id_48233752ff2ca988_uniq` (`user_id`,`comment_id`,`flag`),
  KEY `threadedcomments_threadedcommentflag_fbfc09f1` (`user_id`),
  KEY `threadedcomments_threadedcommentflag_111c90f9` (`flag`),
  KEY `threadedcomments_threadedcommentflag_9b3dc754` (`comment_id`),
  CONSTRAINT `comment_id_refs_id_1e6a9e31b6c897c1` FOREIGN KEY (`comment_id`) REFERENCES `threadedcomments_threadedcomment` (`id`),
  CONSTRAINT `user_id_refs_id_761ed4cf00250914` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `threadedcomments_threadedcommentflag`
--

LOCK TABLES `threadedcomments_threadedcommentflag` WRITE;
/*!40000 ALTER TABLE `threadedcomments_threadedcommentflag` DISABLE KEYS */;
/*!40000 ALTER TABLE `threadedcomments_threadedcommentflag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `todos_todo`
--

DROP TABLE IF EXISTS `todos_todo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `todos_todo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `creation_date` date NOT NULL,
  `view_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`view_name`),
  CONSTRAINT `user_id_refs_id_b790727c` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `todos_todo`
--

LOCK TABLES `todos_todo` WRITE;
/*!40000 ALTER TABLE `todos_todo` DISABLE KEYS */;
/*!40000 ALTER TABLE `todos_todo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-05-09 18:58:43
