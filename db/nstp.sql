-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 07, 2024 at 10:25 AM
-- Server version: 8.0.31
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `thesis_2024_nstp`
--

-- --------------------------------------------------------

--
-- Table structure for table `batches`
--

DROP TABLE IF EXISTS `batches`;
CREATE TABLE IF NOT EXISTS `batches` (
  `batchID` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `userID` int UNSIGNED NOT NULL COMMENT 'head',
  `nstpComponentID` tinyint UNSIGNED NOT NULL,
  `schoolYear` varchar(9) COLLATE utf8mb4_general_ci NOT NULL,
  `term` tinyint NOT NULL,
  `code` varchar(6) COLLATE utf8mb4_general_ci NOT NULL,
  `studentCount` smallint UNSIGNED NOT NULL,
  `status` tinyint NOT NULL COMMENT '0=Open, 1=On Going, 2=Done',
  PRIMARY KEY (`batchID`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `batch_attendances`
--

DROP TABLE IF EXISTS `batch_attendances`;
CREATE TABLE IF NOT EXISTS `batch_attendances` (
  `batchAttendanceID` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `batchID` int UNSIGNED NOT NULL,
  `date` date DEFAULT NULL,
  `dateInserted` datetime DEFAULT NULL,
  PRIMARY KEY (`batchAttendanceID`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `batch_attendance_logs`
--

DROP TABLE IF EXISTS `batch_attendance_logs`;
CREATE TABLE IF NOT EXISTS `batch_attendance_logs` (
  `batchAttendanceLogID` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `batchAttendanceID` int UNSIGNED NOT NULL,
  `batchStudentID` int UNSIGNED NOT NULL,
  PRIMARY KEY (`batchAttendanceLogID`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `batch_students`
--

DROP TABLE IF EXISTS `batch_students`;
CREATE TABLE IF NOT EXISTS `batch_students` (
  `batchStudentID` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `batchID` int UNSIGNED NOT NULL,
  `userID` int UNSIGNED NOT NULL,
  `attendance` tinyint NOT NULL,
  `exam` tinyint NOT NULL,
  `performance` tinyint NOT NULL,
  `total` tinyint NOT NULL,
  `status` tinyint NOT NULL COMMENT '-1=Failed, 0=On Going, 1=Passed',
  PRIMARY KEY (`batchStudentID`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blood_types`
--

DROP TABLE IF EXISTS `blood_types`;
CREATE TABLE IF NOT EXISTS `blood_types` (
  `bloodTypeID` tinyint UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(5) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`bloodTypeID`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `blood_types`
--

INSERT INTO `blood_types` (`bloodTypeID`, `name`) VALUES
(1, 'A+'),
(2, 'A-'),
(3, 'B+'),
(4, 'B-'),
(5, 'AB+'),
(6, 'AB-'),
(7, 'O+'),
(8, 'O-');

-- --------------------------------------------------------

--
-- Table structure for table `configurations`
--

DROP TABLE IF EXISTS `configurations`;
CREATE TABLE IF NOT EXISTS `configurations` (
  `configurationID` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `remarks` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `isShown` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`configurationID`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `configurations`
--

INSERT INTO `configurations` (`configurationID`, `name`, `value`, `remarks`, `isShown`) VALUES
(1, 'Performance', '40', '', 0),
(2, 'Exam', '30', '', 0),
(3, 'Attendance', '30', '', 0),
(4, 'Passing', '75', '', 0);

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
CREATE TABLE IF NOT EXISTS `courses` (
  `courseID` tinyint UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `description` text COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`courseID`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`courseID`, `code`, `description`) VALUES
(1, 'BSIT', 'Bachelor of Science in Information Technology'),
(2, 'BSIS', 'Bachelor of Science in Information Systems'),
(3, 'BSA', 'Bachelor of Science in Accountancy');

-- --------------------------------------------------------

--
-- Table structure for table `nstp_components`
--

DROP TABLE IF EXISTS `nstp_components`;
CREATE TABLE IF NOT EXISTS `nstp_components` (
  `nstpComponentID` tinyint UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` varchar(4) COLLATE utf8mb4_general_ci NOT NULL,
  `description` text COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`nstpComponentID`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nstp_components`
--

INSERT INTO `nstp_components` (`nstpComponentID`, `code`, `description`) VALUES
(1, 'CWTS', 'Civic Welfare Training Service'),
(2, 'LTS', 'Literacy Training Service'),
(3, 'ROTC', 'Reserve Officers\' Training Corps');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `userID` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `userTypeID` tinyint UNSIGNED NOT NULL,
  `nstpComponentID` tinyint UNSIGNED NOT NULL,
  `courseID` tinyint UNSIGNED NOT NULL,
  `yearLevel` tinyint NOT NULL,
  `studentNo` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `lname` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `fname` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `mname` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ename` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `gender` tinyint NOT NULL COMMENT '0=Female, 1=Male',
  `birthDate` date DEFAULT NULL,
  `birthPlace` text COLLATE utf8mb4_general_ci NOT NULL,
  `religion` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `citizenship` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` text COLLATE utf8mb4_general_ci NOT NULL,
  `addressHomeStreet` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `addressHomeMunicipality` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `addressHomeProvince` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `addressHomePhone` varchar(11) COLLATE utf8mb4_general_ci NOT NULL,
  `addressTemporaryStreet` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `addressTemporaryMunicipality` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `addressTemporaryProvince` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `addressTemporaryPhone` varchar(11) COLLATE utf8mb4_general_ci NOT NULL,
  `fatherName` varchar(90) COLLATE utf8mb4_general_ci NOT NULL,
  `fatherOccupation` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `motherName` varchar(90) COLLATE utf8mb4_general_ci NOT NULL,
  `motherOccupation` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `emergencyContactName` varchar(90) COLLATE utf8mb4_general_ci NOT NULL,
  `emergencyContactPhone` varchar(11) COLLATE utf8mb4_general_ci NOT NULL,
  `emergencyContactRelationship` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `emergencyContactAddress` text COLLATE utf8mb4_general_ci NOT NULL,
  `height` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `weigh` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `complexion` text COLLATE utf8mb4_general_ci NOT NULL,
  `bloodTypeID` tinyint UNSIGNED NOT NULL,
  `takeAdvanceCourse` tinyint NOT NULL COMMENT '0=No, 1=Yes',
  `picExt` varchar(5) COLLATE utf8mb4_general_ci NOT NULL,
  `status` tinyint NOT NULL COMMENT '0=Deactivated, 1=Activated',
  PRIMARY KEY (`userID`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userID`, `userTypeID`, `nstpComponentID`, `courseID`, `yearLevel`, `studentNo`, `username`, `password`, `lname`, `fname`, `mname`, `ename`, `gender`, `birthDate`, `birthPlace`, `religion`, `citizenship`, `phone`, `email`, `addressHomeStreet`, `addressHomeMunicipality`, `addressHomeProvince`, `addressHomePhone`, `addressTemporaryStreet`, `addressTemporaryMunicipality`, `addressTemporaryProvince`, `addressTemporaryPhone`, `fatherName`, `fatherOccupation`, `motherName`, `motherOccupation`, `emergencyContactName`, `emergencyContactPhone`, `emergencyContactRelationship`, `emergencyContactAddress`, `height`, `weigh`, `complexion`, `bloodTypeID`, `takeAdvanceCourse`, `picExt`, `status`) VALUES
(1, 1, 0, 0, 0, '', 'admin', '$2b$12$bGK7Zjs/LMxDhejfDcJtg.2uyaIXU551CjWFujMFtap.enpJHccB.', 'admin', 'admin', '', '', 1, NULL, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 0, 0, '', 1);

-- --------------------------------------------------------

--
-- Table structure for table `user_military_sciences`
--

DROP TABLE IF EXISTS `user_military_sciences`;
CREATE TABLE IF NOT EXISTS `user_military_sciences` (
  `userMilitaryScienceID` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `userID` int UNSIGNED NOT NULL,
  `ms` text COLLATE utf8mb4_general_ci NOT NULL,
  `semester` tinyint NOT NULL,
  `schoolYear` text COLLATE utf8mb4_general_ci NOT NULL,
  `grade` tinyint NOT NULL,
  `remarks` text COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`userMilitaryScienceID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_types`
--

DROP TABLE IF EXISTS `user_types`;
CREATE TABLE IF NOT EXISTS `user_types` (
  `userTypeID` tinyint UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`userTypeID`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_types`
--

INSERT INTO `user_types` (`userTypeID`, `name`) VALUES
(1, 'Administrator'),
(2, 'Head'),
(3, 'Student');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
