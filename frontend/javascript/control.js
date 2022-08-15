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

async function render_element(data) {
    let template = '                                                                                        \
    <div class="element-component">                                                                                 \
        <div class="element-key float-left">{0}: &nbsp;&nbsp;</div>                                                 \
        <div><input class="element-value float-left" type="text" name="{0}" id="{0}-inputbox" value="{1}"></div>    \
    </div>                                                                                                          \
    ';
    let element_container = document.getElementById("element-container");
    let context = "";

    if (data==null) {
        let header = await get_header_list();
        header = header.results.filter(v => v!="id" && v!="updatetime");
        header.forEach(v => context = context+template.format(v, ''));
    } else {
        let elements = data.results[0];
        let keys = Object.keys(elements);
        keys = keys.filter(v => v!='datetimelst');
        keys.forEach(v => context = context+template.format(v, elements[v]));
    }

    element_container.innerHTML = context
}


async function get_new_data() {
    // get select datetime
    let selector_container = document.getElementById("data-selector-time");

    if (selector_container.value=="") {
        render_element(null);
    } else {
        let data = await select_datetime(selector_container.value);
        render_element(data);
    }
}

async function upload_data() {
    let elements = document.getElementsByClassName("element-value");

    // generate upload body
    let context = {};
    for (let item of elements) {
        if (['datetimelst', 'description', 'weather', 'winddirection'].includes(item.name)) {
            context[item.name] = item.value;
        } else {
            if (item.value!='') {
                context[item.name] = parseInt(item.value);
            }
        }
    }
    
    console.log(context);
    if ('datetimelst' in context) {
        datetimelst = context['datetimelst'];
        delete context['datetimelst'];
    } else {
        // get select datetime
        let selector_container = document.getElementById("data-selector-time");
        datetimelst = selector_container.value;
    }

    console.log(context);
    console.log(datetimelst);

    let status = await db_upload_data(context, datetimelst);
    if (status==200) {
        alert("Successful");
    }else{
        alert("Failed");
    }
}

async function delete_data() {
    // get select datetime
    let selector_container = document.getElementById("data-selector-time");
    datetimelst = selector_container.value;

    let check_op = confirm("Delete the data: {0}".format(datetimelst));
    if (!check_op) {return}

    let status = await db_delete_data(datetimelst);
    if (status==200) {
        alert("Successful");
    }else{
        alert("Failed");
    }
}

async function sync_forcast() {
    let status = await db_sync_data();
    if (status==200) {
        alert("Successful");
    }else{
        alert("Failed");
    }
    
}