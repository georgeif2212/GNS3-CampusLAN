CREATE TABLE cdp_neighbors (
    ID_CDP_Neighbor INT PRIMARY KEY IDENTITY,
    ID_Device INT,
    Neighbor_Device_ID INT,
    Neighbor_Device_Name VARCHAR(50),
    Local_Interface VARCHAR(50),
    Remote_Interface VARCHAR(50),
    Capacity VARCHAR(50),
    Platform VARCHAR(50),
    Software_Version VARCHAR(50),
    Duplex VARCHAR(20),
    Advertisement_Version VARCHAR(50),
    Neighbor_IP_Address VARCHAR(15),
    FOREIGN KEY (ID_Device) REFERENCES devices(DispositivoID)
);