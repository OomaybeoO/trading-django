// static/js/fetch_data.js

document.addEventListener("DOMContentLoaded", function() {
    fetch('https://api.bitget.com/api/spot/v1/market/history-candles?symbol=BTCUSDT_SPBL&period=4h&endTime=1659080270000&limit=4')  // 將 '/your-api-url/' 替換為您的API端點URL
    .then(response => response.json())
    .then(data => {
        // 在這裡處理從API獲取的數據
        console.log(data);  // 範例：將數據打印到控制台
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
});
