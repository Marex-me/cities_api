SELECT
	p.value
FROM
	populations p
		JOIN
	(SELECT
		MAX(year) AS year
	FROM
		populations
	WHERE
		LOWER(city_name) = '{0}'
		AND year <= {1}
		{2}AND city_type = 'City proper'
	) my
		ON my.year = p.year
WHERE
	LOWER(p.city_name) = '{0}'
	AND p.year <= {1}
	{3}AND p.city_type = 'City proper';