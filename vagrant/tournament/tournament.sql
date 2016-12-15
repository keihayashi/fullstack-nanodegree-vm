-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players ( player_id SERIAL primary key,
                       player_name TEXT);

CREATE TABLE matches ( match_id SERIAL primary key,
                       winner_id INTEGER references players (player_id),
                       loser_id INTEGER references players (player_id));

CREATE VIEW standings (id, name, wins, matches) AS
                       SELECT p.player_id, p.player_name,
                       COUNT(CASE WHEN m.winner_id = p.player_id THEN 1 END),
                       COUNT(m.match_id)
                       FROM players AS p LEFT JOIN matches AS m
                       ON p.player_id = m.winner_id OR p.player_id = m.loser_id
                       GROUP BY p.player_id;
