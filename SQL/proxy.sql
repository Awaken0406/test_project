/*
Navicat MySQL Data Transfer

Source Server         : 数据库
Source Server Version : 80100
Source Host           : 127.0.0.1:3306
Source Database       : senge

Target Server Type    : MYSQL
Target Server Version : 80100
File Encoding         : 65001

Date: 2023-07-28 18:34:45
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for proxy
-- ----------------------------
DROP TABLE IF EXISTS `proxy`;
CREATE TABLE `proxy` (
  `secret_id` varchar(255) DEFAULT NULL,
  `signature` varchar(255) DEFAULT NULL,
  `proxy_name` varchar(255) DEFAULT NULL,
  `proxy_password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of proxy
-- ----------------------------
INSERT INTO `proxy` VALUES ('o3jriybjgabkw9s4ttmo', 'cck1v6kn2to5ms1qaisjatzpf7lyt92b', 'd2704271743', '9an858x3');
