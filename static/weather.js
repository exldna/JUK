
function get_weather() {
    get(
        "https://api.weather.yandex.ru/v1/informers?lat=55.75396&lon=37.620393",
        {
        'X-Yandex-API-Key': '9894f93c-6bb8-45a2-95e2-6eee7ea9ab53',
        },
        function(now) {
            console.log(now)
        }
    );
}