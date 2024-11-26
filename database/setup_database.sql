-- Ensure CryptomessengerDB exists
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'CryptomessengerDB')
BEGIN
    CREATE DATABASE CryptomessengerDB;
END;
GO

USE CryptomessengerDB;
GO

-- Drop tables if they exist
IF OBJECT_ID('dbo.Status', 'U') IS NOT NULL DROP TABLE Status;
IF OBJECT_ID('dbo.Messages', 'U') IS NOT NULL DROP TABLE Messages;
IF OBJECT_ID('dbo.Contacts', 'U') IS NOT NULL DROP TABLE Contacts;
IF OBJECT_ID('dbo.Users', 'U') IS NOT NULL DROP TABLE Users;

-- Create Users table
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) UNIQUE NOT NULL,
    PublicKey NVARCHAR(MAX) NOT NULL,
    IP NVARCHAR(15) NULL,--added IP field
    IsOnline BIT NOT NULL
);

-- Create Contacts table
CREATE TABLE Contacts (
    ContactID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL,
    ContactUserID INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ContactUserID) REFERENCES Users(UserID)
);

-- Create Messages table
CREATE TABLE Messages (
    MessageID NVARCHAR(36) PRIMARY KEY, -- Changed to string
    SenderID INT NOT NULL,
    ReceiverID INT NOT NULL,
    MessageText NVARCHAR(MAX) NOT NULL,
    Timestamp DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (SenderID) REFERENCES Users(UserID),
    FOREIGN KEY (ReceiverID) REFERENCES Users(UserID)
);

-- Create Status table
CREATE TABLE Status (
    StatusID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NOT NULL,
    LastSeen DATETIME DEFAULT GETDATE(),
    CurrentStatus NVARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
>>>>>>> 0f63b106176df086ce85b1171980a64526a4be21
