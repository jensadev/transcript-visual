import express from 'express'
import fs from 'node:fs';
import { parse } from 'csv-parse';

const port = process.env.PORT || 3000

const app = express()

const __dirname = new URL('.', import.meta.url).pathname;

const processFile = async () => {
  const records = [];
  const parser = fs
    .createReadStream(`${__dirname}/csv/test.csv`)
    .pipe(parse({
    // CSV options if any
    }));
  for await (const record of parser) {
    // Work with each record
    records.push(record);
  }
  return records;
};

app.get('/', async (req, res) => {
  const records = await processFile();
  res.json(records);
})


app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`)
})