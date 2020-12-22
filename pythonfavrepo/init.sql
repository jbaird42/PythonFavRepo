use pythonfavrepo;

CREATE TABLE IF NOT EXISTS repos (
                                repo_id INTEGER PRIMARY KEY,
                                repo_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                                url VARCHAR(255),
                                created DATETIME,
                                last_push DATETIME,
                                description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
                                num_stars INTEGER
                            );