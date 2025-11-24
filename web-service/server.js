const express = require('express');
const axios = require('axios');
const app = express();
const port = 80;

// const API_URL = 'http://api-service:5000/api/data';

const API_URL = process.env.BACKEND_URL || 'http://api-service:5000/api/data';
console.log(`Using backend API URL: ${API_URL}`);

app.get('/', async (req, res) => {
  try {
    const response = await axios.get(API_URL);
    const apiData = response.data;

    res.send(`
            <html>
        <head><title>Demo Microservice</title></head>
        <body style="font-family: sans-serif; padding: 20px;">
          <h1>Selamat Datang di Web Service (Frontend)</h1>
          <p>Saya berhasil menghubungi Backend API dan mendapatkan data:</p>
          <div style="background-color: #f0f0f0; border-left: 5px solid #007bff; padding: 15px;">
            <p><strong>Pesan:</strong> ${apiData.message}</p>
            <p><strong>Data:</strong> ${apiData.data}</p>
            <p><strong>Dilayani oleh Pod Backend:</strong> ${apiData.server_pod}</p>
          </div>
        </body>
      </html>
    `);
  } catch (error) {
    res.status(500).send(`
      <h1>Gagal Menghubungi Backend API!</h1>
      <p>Error: ${error.message}</p>
      <p>Pastikan backend service 'api-service' sudah berjalan di port 5000.</p>
    `);
  }
});

app.listen(port, () => {
  console.log(`Web service listening on port ${port}`);
});