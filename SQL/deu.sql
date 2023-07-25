/*
Navicat MySQL Data Transfer

Source Server         : 数据库
Source Server Version : 80100
Source Host           : 127.0.0.1:3306
Source Database       : senge

Target Server Type    : MYSQL
Target Server Version : 80100
File Encoding         : 65001

Date: 2023-07-25 17:28:57
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for deu
-- ----------------------------
DROP TABLE IF EXISTS `deu`;
CREATE TABLE `deu` (
  `sexual` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `sex` int NOT NULL,
  `phone` varchar(255) NOT NULL,
  `mail` varchar(255) NOT NULL,
  `passport` varchar(255) NOT NULL,
  `start` date NOT NULL,
  `end` date NOT NULL,
  `brith` date NOT NULL,
  `effective` date NOT NULL,
  `state` int DEFAULT '0',
  PRIMARY KEY (`sexual`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
