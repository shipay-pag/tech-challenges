--===>>> Roles:
CREATE TABLE roles (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	description varchar NOT NULL,
	CONSTRAINT roles_pk PRIMARY KEY (id)
);


--===>>> Claims:
CREATE TABLE claims (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	decription varchar NOT NULL,
	active bool NOT NULL DEFAULT true,
	CONSTRAINT claims_pk PRIMARY KEY (id)
);


--===>>> Users:
CREATE TABLE users (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" varchar NOT NULL,
	email varchar NOT NULL,
	"password" varchar NOT NULL,
	role_id int4 NOT NULL,
	created_at date NOT NULL,
	updated_at date NULL,
	CONSTRAINT users_pk PRIMARY KEY (id)
);

-- users foreign keys
ALTER TABLE users ADD CONSTRAINT users_fk FOREIGN KEY (role_id) REFERENCES roles(id);

--===>>> UserClaims:
CREATE TABLE user_claims (
	user_id int8 NOT NULL,
	claim_id int8 NOT NULL,
	CONSTRAINT user_claims_un UNIQUE (user_id, claim_id)
);

-- user_claims foreign keys
ALTER TABLE user_claims ADD CONSTRAINT user_claims_fk FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE user_claims ADD CONSTRAINT user_claims_fk_1 FOREIGN KEY (claim_id) REFERENCES claims(id);
