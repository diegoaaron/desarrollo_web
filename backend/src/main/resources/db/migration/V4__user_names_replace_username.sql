-- La cuenta se identifica solo por su correo; en lugar de un nombre de usuario se guardan
-- nombre y apellido (los mismos que se usan en los datos de entrega).
ALTER TABLE users ADD COLUMN first_name VARCHAR(80);
ALTER TABLE users ADD COLUMN last_name VARCHAR(80);

-- Cuentas existentes: el antiguo nombre de usuario pasa a ser el nombre.
UPDATE users SET first_name = username, last_name = '';

ALTER TABLE users ALTER COLUMN first_name SET NOT NULL;
ALTER TABLE users ALTER COLUMN last_name SET NOT NULL;
ALTER TABLE users ADD CONSTRAINT users_first_name_not_blank CHECK (length(btrim(first_name)) > 0);

ALTER TABLE users DROP COLUMN username;
