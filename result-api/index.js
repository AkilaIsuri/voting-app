// result/index.js
const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = process.env.PORT || 80;

const pool = new Pool({
  host: process.env.POSTGRES_HOST || 'db',
  user: process.env.POSTGRES_USER || 'postgres',
  password: process.env.POSTGRES_PASSWORD || 'postgres',
  database: process.env.POSTGRES_DB || 'votes',
  port: process.env.POSTGRES_PORT ? parseInt(process.env.POSTGRES_PORT) : 5432
});

app.get('/', async (req, res) => {
  try {
    const result = await pool.query('SELECT option, count FROM results ORDER BY option');
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('DB error');
  }
});

app.listen(port, () => {
  console.log(`Result service listening on port ${port}`);
});
