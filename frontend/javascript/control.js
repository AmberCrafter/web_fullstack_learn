async function load_time() {
    let selector_container = document.getElementById("data-selector-time");
    let timelist = await get_datetime_list();
    timelist = timelist.results.map((v) => v.replace('T', ' '))
    timelist = timelist.reverse()

    let context = selector_container.innerHTML;

    timelist.map(v => {
        context = context+'<option value="{0}">{0}</option>'.format(v)
    })

    selector_container.innerHTML = context;
}