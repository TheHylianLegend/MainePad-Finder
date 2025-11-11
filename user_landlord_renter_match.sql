CREATE TABLE IF NOT EXISTS users (
	user_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL UNIQUE,
    user_name VARCHAR(50) NOT NULL UNIQUE,
    user_password VARCHAR(50) NOT NULL,
	email VARCHAR(100) NOT NULL,
    phone_number BIGINT NOT NULL,
    gender ENUM('male','female','other') DEFAULT 'other',
    user_desc NVARCHAR(1000),
    picture_url NVARCHAR(1000),
    birth_date DATE NULL,
    display_name VARCHAR(200) NOT NULL
);

CREATE TABLE renter (
	user_id_inside BIGINT UNSIGNED NOT NULL PRIMARY KEY,
	CONSTRAINT fk_renter_user FOREIGN KEY (user_id_inside) REFERENCES users(user_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE landlord (
	user_id_inside BIGINT UNSIGNED NOT NULL PRIMARY KEY,
	CONSTRAINT fk_landlord_user FOREIGN KEY (user_id_inside) REFERENCES users(user_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE user_match(
	match_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    renter_id_a BIGINT UNSIGNED NOT NULL,
    renter_id_b BIGINT UNSIGNED NOT NULL,
    
	CONSTRAINT fk_um_r1
    FOREIGN KEY (renter_id_a) REFERENCES renter(user_id_inside)
    ON DELETE CASCADE ON UPDATE CASCADE,
    
	CONSTRAINT fk_um_r2
    FOREIGN KEY (renter_id_b) REFERENCES renter(user_id_inside)
    ON DELETE CASCADE ON UPDATE CASCADE,
    
    CONSTRAINT ck_um_noself CHECK (renter1_id <> renter2_id),
    UNIQUE KEY ux_um_pair (pair_a, pair_b)
)