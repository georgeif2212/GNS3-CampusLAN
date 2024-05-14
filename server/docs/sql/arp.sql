CREATE TABLE arp (
    ID_ARP INT PRIMARY KEY IDENTITY,
    ID_Device INT,
    IP_Address VARCHAR(15),
    Encryption_Type VARCHAR(50),
    Interface_Name VARCHAR(50),
    Link_Type VARCHAR(50),
    ARP_Mode VARCHAR(50),
    Hardware_Type VARCHAR(50),
    MAC_Address VARCHAR(17),
    Time TIMESTAMP,
    FOREIGN KEY (ID_Device) REFERENCES devices(DispositivoID)
);