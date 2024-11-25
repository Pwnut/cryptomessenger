CREATE DATABASE CryptomessengerDB;
GO

USE CryptomessengerDB;

-- Create Users Table
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL UNIQUE,
    PublicKey NVARCHAR(MAX) NOT NULL,
    IP NVARCHAR(15) NULL, --added ip field 
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
    MessageID NVARCHAR(36) PRIMARY KEY, --changed to string
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


