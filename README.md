##  Documentación de la API de consulta para las salidas numéricas del pronóstico de SisPI

### 1. Introducción
> "In a few moments he was barefoot, his stockings folded in his pockets and his
  canvas shoes dangling by their knotted laces over his shoulders and, picking a
  pointed salt-eaten stick out of the jetsam among the rocks, he clambered down
  the slope of the breakwater. Por aca jorge"

### 2. Instalación
* Requisitos
* Configurando la base de datos
  
  Ejecutar los siguientes comandos para cambiar la configuracion del usuario en el servidor de postgres:
  - sudo -u postgres psql
  - \password postgres
  - now enter New Password and Confirm 
  - then \q to exit
  - Now create a database. You can use pgAdmin or connect to psql and do it from cli. In the second case
  do:
   * Connect to psql: <code>psql -U "username" -h "servername"<code>
   * Create de database: <code>CREATE DATABASE "db_name"<code>
  - Now add the postgis extension:
     * Connect to the database: Run command 1 and then <code>\connect "db_name"<code>
     * Create the extension support: <code>CREATE EXTENSION POSTGIS;<CODE>
     * Check if the extension was created successfully: <code>\dt<code>. if you see the table spatial_ref_sys. All was done!
                                                                                                                                                                                                                                                                                    >
  
### 2. Introducción
