CREATE TABLE Interfaces (
    ID_Interface INT PRIMARY KEY IDENTITY,
    ID_Device INT,
    Interface_Name VARCHAR(50),
    IP_Address VARCHAR(15),
    Subnet_Mask VARCHAR(15),
    CDP_State VARCHAR(20),
    FOREIGN KEY (ID_Device) REFERENCES devices(DispositivoID)
);