# GNS3-CampusLAN Network Analyzer

## Descripción breve / propósito del proyecto
Este proyecto es una aplicación web diseñada para analizar y monitorear redes empresariales simuladas en GNS3. Proporciona una interfaz para recopilar, analizar y visualizar información de dispositivos de red, incluyendo detalles de interfaces, tablas ARP, protocolos de enrutamiento (OSPF), información de hardware y software, y descubrimiento de vecinos CDP.

## Tabla de Contenidos
- [Tecnologías Usadas](#tecnologías-usadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Flujo de Datos](#flujo-de-datos)
- [Resultados Esperados](#resultados-esperados)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Pruebas](#pruebas)
- [To-Do / Mejoras Futuras](#to-do--mejoras-futuras)
- [Autor](#autor)

## Tecnologías Usadas
- **Backend:**
  - Python 3.x
  - Flask (Framework web)
  - SQLServer (Base de datos)
- **APIs y Protocolos:**
  - RESTCONF
  - YANG data models
  - CDP (Cisco Discovery Protocol)
  - OSPF
- **Herramientas de Red:**
  - GNS3
  - Cisco IOS XE
- **Otros:**
  - JSON para intercambio de datos
  - Algoritmo BFS para descubrimiento de topología

## Estructura del Proyecto
```
server/
├── src/
│   ├── app.py           # Aplicación principal Flask
│   ├── bfs.py           # Algoritmo de búsqueda BFS para topología
│   ├── controllers/     # Lógica de negocio
│   ├── model/          # Modelos de datos
│   ├── routers/        # Rutas de la API
│   ├── middlewares/    # Middleware de la aplicación
│   ├── utils/          # Funciones de utilidad
│   ├── db/            # Configuración de base de datos
│   ├── static/        # Archivos estáticos
│   └── templates/     # Plantillas HTML
├── docs/
│   ├── sql/           # Scripts SQL para la base de datos
│   ├── topology/      # Documentación de topología
│   └── jsons/        # Ejemplos y resultados JSON
```
```

## Configuración
1. Configurar la base de datos:
   - Los scripts SQL se encuentran en `server/docs/sql/`
   - Ejecutar los scripts en orden para crear las tablas necesarias

2. Configurar las variables de entorno:
   - Crear un archivo `.env` en la raíz del proyecto
   - Definir las variables necesarias (IPs, credenciales, etc.)


## Flujo de Datos
1. **Descubrimiento de Red:**
   - El algoritmo BFS comienza desde un dispositivo inicial
   - Recopila información ARP y de vecinos
   - Construye un mapa de topología

2. **Recopilación de Datos:**
   - Interfaces de red
   - Tablas ARP
   - Información CDP
   - Configuración OSPF
   - Detalles de hardware/software

3. **Almacenamiento:**
   - Los datos se almacenan en tablas SQL
   - Los resultados de topología se guardan en JSON

## Resultados Esperados
- Mapa de topología de red completo
- Información detallada de dispositivos
- Estado de interfaces y protocolos
- Relaciones entre dispositivos (vecinos)
- Métricas de red

## Capturas de Pantalla
[Sección pendiente para agregar capturas de pantalla del sistema en funcionamiento]

## Pruebas
- Pruebas de conectividad
- Validación de datos RESTCONF
- Verificación de descubrimiento de topología
- Pruebas de rendimiento de la API

## To-Do / Mejoras Futuras
- [ ] Implementar autenticación de usuarios
- [ ] Agregar soporte para LLDP
- [ ] Mejorar visualización de topología
- [ ] Implementar monitoreo en tiempo real
- [ ] Agregar exportación de datos
- [ ] Integrar con sistemas de monitoreo externos

## Autor
[Jorge Infante Fragoso]
[jinfante2212@gmail.com]
