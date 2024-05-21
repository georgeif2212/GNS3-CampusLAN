CREATE TABLE cdp_neighbors (
    id_cdp_neighbor UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    id_device UNIQUEIDENTIFIER,
    neighbor_device_id UNIQUEIDENTIFIER,
    neighbor_device_name VARCHAR(50),
    local_interface VARCHAR(50),
    remote_interface VARCHAR(50),
    capacity VARCHAR(50),
    platform VARCHAR(50),
    software_version VARCHAR(50),
    duplex VARCHAR(20),
    advertisement_version VARCHAR(50),
    neighbor_ip_address VARCHAR(15),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_device) REFERENCES devices(id_device)
);