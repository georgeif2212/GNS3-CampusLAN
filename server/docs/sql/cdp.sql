CREATE TABLE cdp_neighbors (
    id_cdp UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    id_device UNIQUEIDENTIFIER,
    neighbor_id_device UNIQUEIDENTIFIER,
    neighbor_device_name VARCHAR(25),
    local_interface_name VARCHAR(20),
    neighbor_interface_name VARCHAR(20),
    capability VARCHAR(25),
    platform VARCHAR(20),
    software_version VARCHAR(130),
    duplex VARCHAR(20),
    advertisement_version VARCHAR(20),
    neighbor_ip_address VARCHAR(15),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_device) REFERENCES devices(id_device)
);

