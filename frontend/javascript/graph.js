async function graph_temperature(data, timelist) {
    // let data = await get_forcast(7);
    // console.log(data);

    const temp_avg = data.results.map(v => v.temperature_avg);
    const temp_min = data.results.map(v => v.temperature_min);
    const temp_max = data.results.map(v => v.temperature_max);


    const ctx = document.getElementById('temperature');
    const temperatureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timelist,
            datasets: [{
                label: 'Temperature',
                data: temp_avg,
                borderColor: 'rgb(255, 166, 65)',
                fill: false,
                tension: 0.1,
                borderWidth: 3
            },
            {
                label: 'Min',
                data: temp_min,
                borderColor: 'rgb(78, 164, 255)',
                fill: false,
                tension: 0.1,
                borderWidth: 1
            },
            {
                label: 'Max',
                data: temp_max,
                borderColor: 'rgb(255, 0, 0)',
                fill: false,
                tension: 0.1,
                borderWidth: 1
            }]
        }
    });
}

async function graph_humidity(data, timelist) {
    // let data = await get_forcast(7);
    const rh_avg = data.results.map(v => v.humidity_avg);

    const ctx = document.getElementById('humidity');
    const humidityChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timelist,
            datasets: [{
                label: 'Humidity',
                data: rh_avg,
                borderColor: 'rgb(0, 0, 255)',
                fill: false,
                tension: 0.1,
                borderWidth: 3
            }]
        }
    });
}

async function graph_windspeed(data, timelist) {
    // let data = await get_forcast(7);
    const ws_avg = data.results.map(v => v.windspeed);

    const ctx = document.getElementById('windspeed');
    const windspeedChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timelist,
            datasets: [{
                label: 'Windspeed',
                data: ws_avg,
                borderColor: 'rgb(0, 0, 0)',
                fill: false,
                tension: 0.1,
                borderWidth: 3
            }]
        }
    });
}

async function graph_precipitation(data, timelist) {
    // let data = await get_forcast(7);
    const pop12h = data.results.map(v => v.pop12h);

    const backgroundcolor_list = Array(pop12h.length).fill('rgb(171, 210, 252)');
    const bordercolor_list = Array(pop12h.length).fill('rgb(255, 255, 255)');

    const ctx = document.getElementById('precipitation');
    const precipitationChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: timelist,
            datasets: [{
                label: 'My First Dataset',
                data: pop12h,
                backgroundColor: backgroundcolor_list,
                borderColor: bordercolor_list,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        },
    });
}


async function table_winddiection(data, fulldatetimelst) {
    let head_container = document.getElementById("weekly-winddir-header");
    let context = "";
    fulldatetimelst.map(v => {
        context = context+"<div>{0}/{1}<br>{2}:00</div>".format(v.slice(5,7), v.slice(8,10), v.slice(11,13));
    })
    head_container.innerHTML=context;


    let body_container = document.getElementById("weekly-winddir-body");
    context = "";
    data.results.map(v => {
        context = context+"<div>{0}</div>".format(v.winddirection);
    })
    body_container.innerHTML=context;
}

async function card_weather(data, current_page, total_page) {
    let datetime_container = document.getElementById("weather-card-datetime");
    datetime_container.innerHTML="<div>{0}</div>".format(data.datetimelst.replace('T', ' '));
    let body_container = document.getElementById("weather-card-info");
    body_container.innerHTML="<div>{0}</div>".format(data.description);
    let page_container = document.getElementById("weather-card-page");
    page_container.innerHTML="{0}/{1}".format(current_page+1, total_page);
}

async function graph() {
    let data = await get_forcast(7);
    console.log(data);
    const fulltimelist = data.results.map((v, i) => v.datetimelst.replace('T', ' '));
    const timelist = data.results.map((v, i) => { if (i % 2 == 0) { return v.datetimelst.replace('T', ' ') } else { return '' } });
    let temp = graph_temperature(data, timelist);
    let rh = graph_humidity(data, timelist);
    let ws = graph_windspeed(data, timelist);
    let rain = graph_precipitation(data, timelist);

    let wd = table_winddiection(data,fulltimelist);
    let weather = card_weather(data.results[0], 0, data.results.length);  // Future work: need to become class object
    await Promise.all([temp, rh, rain, ws, wd, weather]);
}