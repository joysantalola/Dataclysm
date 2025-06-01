-- Crear roles
CREATE ROLE rol_admin;
CREATE ROLE rol_recepcio;
CREATE ROLE rol_cuina;
CREATE ROLE rol_facturacio;
CREATE ROLE rol_general;

-- Rol para admin
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO rol_admin;

-- Rol para recepcionista
GRANT SELECT, INSERT, UPDATE ON client TO rol_recepcio;
GRANT SELECT, INSERT, UPDATE ON reserva TO rol_recepcio;
GRANT SELECT, INSERT, UPDATE ON detall_reserva TO rol_recepcio;
GRANT SELECT, INSERT ON check_in TO rol_recepcio;
GRANT SELECT, INSERT ON check_out TO rol_recepcio;

-- Rol para cocineros
GRANT SELECT, INSERT, UPDATE ON solicitud_servei TO rol_cuina;

-- Rol para facturación
GRANT SELECT, INSERT, UPDATE ON factura TO rol_facturacio;
GRANT SELECT, INSERT, UPDATE ON detall_factura TO rol_facturacio;
GRANT SELECT, INSERT, UPDATE ON pagament TO rol_facturacio;
GRANT SELECT, INSERT, UPDATE ON metode TO rol_facturacio;

-- Rol para personas en general (solo puede hacer SELECT)
GRANT SELECT ON ALL TABLES IN SCHEMA public TO rol_general;
REVOKE SELECT ON public.pagament FROM rol_general;
REVOKE SELECT ON public.metode FROM rol_general;

--Una vez hecho esto se puede crear los roles con los nombres de los empleados y meterlos en los grupos para que tengan los privilegios

-- Ejemplo:
--CREATE USER pepito WITH PASSWORD 'pepito123';
--GRANT rol_recepcio TO pepito;

-- A pepito le estas metiendo en “rol_recepcio” y le estas dando los permisos que tiene

-- OPCIONAL, para que cuando se crea una tabla nueva se ponga directamente los privilegios de general (solo SELECT), si necesita más hay que ponerlo manualmente
--ALTER DEFAULT PRIVILEGES IN SCHEMA public
--GRANT SELECT ON TABLES TO rol_general;
