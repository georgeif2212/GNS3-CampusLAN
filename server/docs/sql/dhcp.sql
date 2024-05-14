CREATE TABLE dhcp (
    ID_DHCP INT PRIMARY KEY IDENTITY,
    ID_Device INT,
    Interface_Name VARCHAR(50),
    Client_IP_Address VARCHAR(15),
    State VARCHAR(50),
    Lease_Server_Address VARCHAR(15),
    Gateway_Address VARCHAR(15),
    Lease_Time INT,
    Lease_Expiry DATETIME,
    Lease_Remaining INT,
    Primary_DNS_Address VARCHAR(15),
    Secondary_DNS_Address VARCHAR(15),
    Subnet_Mask VARCHAR(15),
    Timestamp TIMESTAMP,
    FOREIGN KEY (ID_Device) REFERENCES devices(DispositivoID)
);