-- OSPF TABLE
CREATE TABLE ospf_table (
    ospf_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    device_id UNIQUEIDENTIFIER,
    ospf_process_id INT,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT UQ_ospf_process_id UNIQUE (ospf_process_id)
);

-- OSPF NETWORKS
CREATE TABLE ospf_networks (
    ospf_network_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ospf_process_id INT,
    network_ip_address VARCHAR(15),
    mask VARCHAR(15),
    area INT,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ospf_process_id) REFERENCES ospf_table(ospf_process_id)
);