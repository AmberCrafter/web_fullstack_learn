// get data
const DATABASE_URL_BASE = 'https://ideasky-fullstack-backend.herokuapp.com/forcast';

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

async function select_datetime(datetime) {
    url = String.format("{0}/select/{1}", DATABASE_URL_BASE,datetime);
    let data = await fetch(url)
        .then(data => data.json());
    return data;
}

async function get_header_list() {
    url = String.format("{0}/get_header", DATABASE_URL_BASE);
    let data = await fetch(url)
        .then(data => data.json());
    return data;
}

async function db_upload_data(body, datetime) {
    let url = String.format("{0}/put/{1}", DATABASE_URL_BASE, datetime);
    let headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        // "Authorization": `Bearer ${token}`,
    }
    let status = await fetch(url, {method: "POST", headers: headers, body: JSON.stringify(body)})
        .then(response => response.status)
    return status;
}

async function db_delete_data(datetime) {
    let url = String.format("{0}/delete/{1}", DATABASE_URL_BASE, datetime);
    let status = await fetch(url)
        .then(response => response.status)
    return status;
}

async function db_sync_data() {
    let url = String.format("{0}/sync", DATABASE_URL_BASE);
    let status = await fetch(url)
        .then(response => response.status)
    return status;
}