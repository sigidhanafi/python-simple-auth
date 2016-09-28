# python-simple-auth

This is my first application that using flask framework. This application is an case that I use to learn flask. This application can create user, login user, logout and display all user. I am referring from this tutorial : https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972

# database structure

# Create Database

CREATE DATABASE BucketList;

#Create Table User

CREATE TABLE `BucketList`.`user` (
  `id` BIGINT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(45) NULL,
  `bio` VARCHAR(255) NULL,
PRIMARY KEY (`user_id`));