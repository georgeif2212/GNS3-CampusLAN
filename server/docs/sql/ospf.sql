-- Tabla OSPF
CREATE TABLE ospf_table (
    ospf_id INT PRIMARY KEY,
    device_id INT,
    ospf_process_id INT,
    Timestamp TIMESTAMP,
);

-- Tabla OSPF Redes
CREATE TABLE ospf_networks (
    ospf_network_id INT PRIMARY KEY,
    ospf_process_id INT,
    network_ip_address VARCHAR(15),
    mask VARCHAR(15),
    area INT,
    Timestamp TIMESTAMP,
    FOREIGN KEY (ospf_process_id) REFERENCES ospf_table(ospf_process_id)
);