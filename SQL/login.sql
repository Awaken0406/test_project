/*
Navicat MySQL Data Transfer

Source Server         : 数据库
Source Server Version : 80100
Source Host           : 127.0.0.1:3306
Source Database       : senge

Target Server Type    : MYSQL
Target Server Version : 80100
File Encoding         : 65001

Date: 2023-07-20 18:26:37
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for login
-- ----------------------------
DROP TABLE IF EXISTS `login`;
CREATE TABLE `login` (
  `account` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `date` date DEFAULT NULL,
  `count` int DEFAULT NULL,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
