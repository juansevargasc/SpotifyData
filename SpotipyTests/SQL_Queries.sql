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


SELECT t.name, a.name
FROM track AS t
INNER JOIN artist AS a
ON t.artist_id = a.id
WHERE a.name = 'Coldplay'
ORDER BY t.name;


SELECT t.name, p.name AS Playlist_Name, a.name AS artist
FROM track AS t
LEFT JOIN track_playlist AS tp
ON t.id = tp.track_id
LEFT JOIN playlist AS p
ON tp.playlist_id = p.id
LEFT JOIN artist AS a
ON t.artist_id = a.id;

SELECT * 
FROM artist
ORDER BY artist.name ASC;

SELECT *
FROM track; 