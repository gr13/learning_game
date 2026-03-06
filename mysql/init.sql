CREATE DATABASE IF NOT EXISTS learning_db;
CREATE DATABASE IF NOT EXISTS test_db;
use learning_db;

-- ##################################################
-- Core Vocabulary
-- ##################################################

CREATE TABLE IF NOT EXISTS core_vocabulary (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(255) NOT NULL UNIQUE,
    introduced BOOLEAN NOT NULL DEFAULT FALSE,
    dt_introduced DATETIME NULL,
    learned BOOLEAN NOT NULL DEFAULT FALSE,
    dt_learned DATETIME NULL,
    INDEX idx_introduced (introduced),
    INDEX idx_learned (learned)
);

LOAD DATA INFILE "/docker-entrypoint-initdb.d/core_vocabulary.csv"
IGNORE
INTO TABLE core_vocabulary
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
(word);

-- ##################################################
-- Domain Vocabulary
-- ##################################################

CREATE TABLE IF NOT EXISTS domain_vocabulary (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(255) NOT NULL UNIQUE,
    domain VARCHAR(100) NOT NULL,
    introduced BOOLEAN NOT NULL DEFAULT FALSE,
    dt_introduced DATETIME NULL,
    learned BOOLEAN NOT NULL DEFAULT FALSE,
    dt_learned DATETIME NULL,
    INDEX idx_domain (domain),
    INDEX idx_introduced (introduced),
    INDEX idx_learned (learned)
);

LOAD DATA INFILE "/docker-entrypoint-initdb.d/domain_vocabulary.csv"
IGNORE
INTO TABLE domain_vocabulary
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS
(word, domain);

-- ##################################################
-- reading exam
-- ##################################################

CREATE TABLE IF NOT EXISTS reading_exam (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    task_level ENUM("A1","A2","B1","B2","C1") NOT NULL DEFAULT "A2",
    main_task TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    dt_done DATETIME NULL,
    INDEX idx_done (done)
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/reading_exam.csv'
IGNORE
INTO TABLE reading_exam
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(task_level, main_task);

-- ##################################################
-- writing exam
-- ##################################################

CREATE TABLE IF NOT EXISTS writing_exam (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    task_level ENUM("A1","A2","B1","B2","C1") NOT NULL DEFAULT "A2",
    main_task VARCHAR(255) NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    dt_done DATETIME NULL,
    INDEX idx_done (done)
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/writing_exam.csv'
IGNORE
INTO TABLE writing_exam
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(task_level, main_task);

-- ##################################################
-- speaking exam
-- ##################################################

CREATE TABLE IF NOT EXISTS speaking_exam (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    task_level ENUM("A1","A2","B1","B2","C1") NOT NULL DEFAULT "A2",
    main_task VARCHAR(255) NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE,
    dt_done DATETIME NULL,
    INDEX idx_done (done)
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/speaking_exam.csv'
IGNORE
INTO TABLE speaking_exam
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(task_level, main_task);


-- ##################################################
-- profile # one user for now
-- ##################################################
CREATE TABLE IF NOT EXISTS profile (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_level ENUM("A1","A2","B1","B2","C1") NOT NULL DEFAULT "A2", -- user_level (A1–C1)
    preferences  VARCHAR(255) NOT NULL DEFAULT "" -- not sure yet, placeholder
);

INSERT IGNORE INTO profile (user_level) VALUES ("A2");


-- ##################################################
-- training_lesson
-- one to several records per day per day 
-- in theory can be several records per day
-- paceholder, if I do all exercises and deside that
-- is not anough
-- not done could be only one
-- ##################################################
CREATE TABLE IF NOT EXISTS training_lesson (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_level ENUM("A1","A2","B1","B2","C1") NOT NULL DEFAULT "A2",
    ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

-- ##################################################
-- modules
-- several modules per training lesson
-- several modules at max 5 per training day
-- ##################################################
CREATE TABLE IF NOT EXISTS modules (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    training_lesson_id INT UNSIGNED, -- training_day.id
    module_type ENUM(
        "CORE",
        "DOMAIN",
        "READING",
        "WRITING",
        "SPEAKING"
    ) NOT NULL DEFAULT "CORE",
    done BOOLEAN NOT NULL DEFAULT FALSE,
    INDEX idx_training_lesson (training_lesson_id),
    INDEX idx_done (done)
);


-- ##################################################
-- sessions
-- one session per exercise / 5 exercises per module
-- or 1 big exercise for writing, reading, speaking
-- ##################################################
CREATE TABLE IF NOT EXISTS sessions (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    module_id INT UNSIGNED NOT NULL, -- modules.id
    session_id CHAR(36) NOT NULL UNIQUE, -- str(uuid.uuid4())
    INDEX idx_module_id (module_id)
);

-- ##################################################
-- session_messages
-- several messages per session
-- ##################################################
CREATE TABLE IF NOT EXISTS session_messages (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    session_db_id INT UNSIGNED, -- sessions.id
    current_exercise TINYINT UNSIGNED DEFAULT 1, -- 1-5
    status ENUM("assistant", "error", "system", "user", "correction", "summary") DEFAULT "system", -- (system / user)
    content TEXT NOT NULL,
    INDEX idx_session_db_id (session_db_id)
);

