-- Funció per crear el trigger i esborrar les dades del client
CREATE OR REPLACE FUNCTION eliminar_dades_targeta()
RETURNS TRIGGER AS $$
BEGIN
    -- Quan es crea una factura després del check-out, esborrem dades de la targeta
    UPDATE metode
    SET 
        numero = NULL,
        cvv = NULL,
        data_caducitat = NULL,
        nom = NULL
    WHERE id_pagament IN (
        SELECT id_pagament FROM pagament WHERE id_factura = NEW.id_factura
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Creació del trigger
CREATE TRIGGER trigger_esborra_targeta
AFTER INSERT ON factura
FOR EACH ROW
EXECUTE FUNCTION eliminar_dades_targeta();
