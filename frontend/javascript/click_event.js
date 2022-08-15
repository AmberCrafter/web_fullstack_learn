async function card_page_next() {
    let data = await get_forcast(7);
    // get current page
    let page_container = document.getElementById("weather-card-page");
    let current = parseInt(page_container.innerHTML.split('/')[0]);
    
    if (current>=data.results.length) return;
    
    // update
    await card_weather(data.results[current], current, data.results.length);
}

async function card_page_prev() {
    let data = await get_forcast(7);
    // get current page
    let page_container = document.getElementById("weather-card-page");
    let current = parseInt(page_container.innerHTML.split('/')[0]);

    if (current<=1) return;

    // update
    await card_weather(data.results[current-2], current-2, data.results.length);
}