CREATE TABLE IF NOT EXISTS gdelt_datamart (
    GlobalEventID INT PRIMARY KEY,
    Day DATE,
    Actor1Geo_CountryCode INT,
);

CREATE TABLE IF NOT EXISTS gdelt_mentions (
    GlobalMentionID INT PRIMARY KEY,
    GlobalEventID INT,
    Actor1FullName INT,
);

CREATE TABLE IF NOT EXISTS gdelt_gkg (
    GlobalKnowledgeGraphID INT PRIMARY KEY,
    GlobalEventID INT,
    ActorsCount INT,
);

CREATE TABLE IF NOT EXISTS gdelt_datamart (
    GlobalEventID INT PRIMARY KEY,
    Day DATE,
    Actor1Geo_CountryCode INT,
    GlobalMentionID INT,
    Actor1FullName INT,
    GlobalKnowledgeGraphID INT,
    ActorsCount INT
);

INSERT INTO gdelt_datamart (
    GlobalEventID, 
    Day, 
    Actor1Geo_CountryCode, 
    GlobalMentionID, 
    Actor1FullName, 
    GlobalKnowledgeGraphID, 
    ActorsCount
)
SELECT DISTINCT
    e.GlobalEventID,
    e.Day,
    e.Actor1Geo_CountryCode,
    m.GlobalMentionID,
    m.Actor1FullName,
    g.GlobalKnowledgeGraphID,
    g.ActorsCount
FROM Events e
LEFT JOIN gdelt_mentions m ON e.GlobalEventID = m.GlobalEventID
LEFT JOIN gdelt_gkg g ON e.GlobalEventID = g.GlobalEventID
ON CONFLICT (GlobalEventID) DO UPDATE SET
    Day = EXCLUDED.Day,
    Actor1Geo_CountryCode = EXCLUDED.Actor1Geo_CountryCode,
    GlobalMentionID = EXCLUDED.GlobalMentionID,
    Actor1FullName = EXCLUDED.Actor1FullName,
    GlobalKnowledgeGraphID = EXCLUDED.GlobalKnowledgeGraphID,
    ActorsCount = EXCLUDED.ActorsCount;
