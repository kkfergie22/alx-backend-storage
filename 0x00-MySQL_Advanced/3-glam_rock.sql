-- List all bands with Glam rock as their main style, ranked by their longevity
SELECT name AS band_name, YEAR(MAX(year_formed)) - YEAR(MIN(year_formed)) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
GROUP BY name
ORDER BY lifespan DESC;
