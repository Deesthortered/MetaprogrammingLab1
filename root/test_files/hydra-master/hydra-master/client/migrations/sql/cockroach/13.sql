-- +migrate Up
CREATE TABLE IF NOT EXISTS hydra_client (
	id varchar(255) NOT NULL,
	client_name text NOT NULL,
	client_secret text NOT NULL,
	redirect_uris text NOT NULL,
	grant_types text NOT NULL,
	response_types text NOT NULL,
	scope text NOT NULL,
	owner text NOT NULL,
	policy_uri text NOT NULL,
	tos_uri text NOT NULL,
	client_uri text NOT NULL,
	logo_uri text NOT NULL,
	contacts text NOT NULL,
	client_secret_expires_at INTEGER NOT NULL DEFAULT 0,
	sector_identifier_uri text NOT NULL,
	jwks text NOT NULL,
	jwks_uri text NOT NULL,
	request_uris text NOT NULL,
	token_endpoint_auth_method VARCHAR(25) NOT NULL DEFAULT '',
	request_object_signing_alg  VARCHAR(10) NOT NULL DEFAULT '',
	userinfo_signed_response_alg VARCHAR(10) NOT NULL DEFAULT '',
	subject_type VARCHAR(15) NOT NULL DEFAULT '',
	allowed_cors_origins text NOT NULL,
	pk SERIAL PRIMARY KEY,
	audience text NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	updated_at timestamp NOT NULL DEFAULT now(),
	frontchannel_logout_uri TEXT NOT NULL DEFAULT '',
	frontchannel_logout_session_required BOOL NOT NULL DEFAULT FALSE,
	post_logout_redirect_uris TEXT NOT NULL DEFAULT '',
	backchannel_logout_uri TEXT NOT NULL DEFAULT '',
	backchannel_logout_session_required BOOL NOT NULL DEFAULT FALSE,
	UNIQUE (id)
);

-- +migrate Down
DROP TABLE hydra_client;