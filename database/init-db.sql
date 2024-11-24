CREATE DATABASE CryptomessengerDB;
GO
ALTER AUTHORIZATION ON DATABASE::CryptomessengerDB TO sa;
GO
-- setup_database.sql
USE master;
CREATE DATABASE CryptomessengerDB;
GO
USE CryptomessengerDB;

-- Create Users Table
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL UNIQUE,
    PublicKey NVARCHAR(MAX) NOT NULL,
    IsOnline BIT DEFAULT 0
);

-- Create Contacts Table
CREATE TABLE Contacts (
    ContactID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    ContactUserID INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ContactUserID) REFERENCES Users(UserID),
    CONSTRAINT UQ_Contacts UNIQUE (UserID, ContactUserID)
);

-- Create Messages Table
CREATE TABLE Messages (
    MessageID INT PRIMARY KEY IDENTITY(1,1),
    SenderID INT NOT NULL,
    RecipientID INT NOT NULL,
    MessageContent NVARCHAR(MAX) NOT NULL,
    Timestamp DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (SenderID) REFERENCES Users(UserID),
    FOREIGN KEY (RecipientID) REFERENCES Users(UserID)
);

-- Create Status Table
CREATE TABLE Status (
    StatusID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    StatusChange BIT NOT NULL,
    Timestamp DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Create Devices Table
CREATE TABLE Devices (
    DeviceID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    DeviceName NVARCHAR(100),
    MACAddress NVARCHAR(17) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Create Device_Connections Table
CREATE TABLE Device_Connections (
    ConnectionID INT PRIMARY KEY IDENTITY(1,1),
    DeviceID INT NOT NULL,
    IPAddress NVARCHAR(45) NOT NULL,  -- Supports IPv6 addresses
    LoginTimestamp DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (DeviceID) REFERENCES Devices(DeviceID)
);
