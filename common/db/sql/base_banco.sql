CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE users ADD COLUMN email VARCHAR(255);
CREATE INDEX idx_users_user_id ON users(id);
CREATE INDEX idx_users_due_date ON todos(created_at);

CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_due_date ON todos(due_date);

SELECT public.update_user(:p_id, :p_username, :p_password_hash, :p_email);

CREATE OR REPLACE FUNCTION public.update_user(p_id integer, p_username character varying DEFAULT NULL::character varying, p_email character varying DEFAULT NULL::character varying)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
    UPDATE public.users
    SET
        username = COALESCE(p_username, username),
        email = COALESCE(p_email, email),
        updated_at = CURRENT_TIMESTAMP
    WHERE id = p_id;
END;
$function$
;
