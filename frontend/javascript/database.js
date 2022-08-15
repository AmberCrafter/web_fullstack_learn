// get data
const DATABASE_URL_BASE = 'http://127.0.0.1:8000/forcast';

async function get_forcast(days) {
    url = String.format("{0}/get/{1}", DATABASE_URL_BASE, 7);
    let data = await fetch(url)
        .then(data => data.json());
    return data;
}

async function get_datetime_list() {
    url = String.format("{0}/get_all/datetime", DATABASE_URL_BASE);
    let data = await fetch(url)
        .then(data => data.json());
    return data;
}