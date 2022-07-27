SELECT t.name, p.name
FROM track AS t
INNER JOIN track_playlist AS tp
ON t.id = tp.track_id
INNER JOIN playlist AS p
ON tp.playlist_id = p.id;


SELECT * FROM track_playlist
ORDER BY track_id ASC, playlist_id ASC;

SELECT * FROM track
ORDER BY id ASC;