CREATE TABLE lldp_neighbors (
    ID_LLDP_Neighbor INT PRIMARY KEY IDENTITY,
    ID_Device INT,
    Neighbor_Device_ID INT,
    Local_Interface VARCHAR(50),
    Remote_Interface VARCHAR(50),
    Capabilities VARCHAR(50),
    TTL INT,
    FOREIGN KEY (ID_Device) REFERENCES devices(DispositivoID)
);