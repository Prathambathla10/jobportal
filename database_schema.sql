-- --------------------------------------------------------
-- Database Creation
-- --------------------------------------------------------
CREATE DATABASE IF NOT EXISTS `jobportal`;

USE `jobportal`;

-- --------------------------------------------------------
-- Table Structure for `users`
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `status` VARCHAR(50) DEFAULT 'active',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------
-- Table Structure for `employers`
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `employers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------
-- Table Structure for `profiles` (User Profiles)
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `profiles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255),
    `image` VARCHAR(255),
    FOREIGN KEY (`username`) REFERENCES `users` (`username`) ON DELETE CASCADE
);

-- --------------------------------------------------------
-- Table Structure for `employeers_profiles` (Employer Profiles)
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `employeers_profiles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(255) NOT NULL,
    `name` VARCHAR(255),
    `image` VARCHAR(255),
    FOREIGN KEY (`username`) REFERENCES `employers` (`username`) ON DELETE CASCADE
);

-- --------------------------------------------------------
-- Table Structure for `jobs`
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `jobs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `emp_name` VARCHAR(255) NOT NULL,
    `job_title` VARCHAR(255) NOT NULL,
    `job_description` TEXT,
    `job_status` VARCHAR(50) DEFAULT 'vacant',
    `stipend` VARCHAR(255),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------
-- Optional: Insert some dummy data to get started
-- --------------------------------------------------------
-- INSERT INTO `users` (`username`, `password`) VALUES ('testuser', 'password123');
-- INSERT INTO `employers` (`username`, `password`) VALUES ('testemployer', 'password123');