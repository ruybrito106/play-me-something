CREATE TABLE survey_result (
    id BIGSERIAL PRIMARY KEY,
    text_id TEXT,
    spotify_id TEXT,
    anger DOUBLE PRECISION,
    fear DOUBLE PRECISION,
    sadness DOUBLE PRECISION,
    joy DOUBLE PRECISION,
    analytical DOUBLE PRECISION,
    confident DOUBLE PRECISION,
    tentative DOUBLE PRECISION,
    daceability DOUBLE PRECISION, -- [0.0; 1.0]
    acousticness DOUBLE PRECISION, -- [0.0; 1.0] 
    valence DOUBLE PRECISION, -- [0.0; 1.0]
    tempo DOUBLE PRECISION, -- > 0
    energy DOUBLE PRECISION, -- [0.0; 1.0]
    time_signature DOUBLE PRECISION, -- > 0
    mode DOUBLE PRECISION, -- {0, 1},
    loudness DOUBLE PRECISION, -- [-60, 0]
    "key" DOUBLE PRECISION -- [0, 11] 
);