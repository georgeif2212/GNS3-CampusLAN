CREATE TABLE lldp_neighbors (
    id_lldp_neighbor UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    id_device UNIQUEIDENTIFIER,
    neighbor_device_id VARCHAR(50),
    local_interface VARCHAR(10),
    remote_interface VARCHAR(10),
    capabilities VARCHAR(50),
    ttl INT,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_device) REFERENCES devices(id_device)
);