let tg = window.Telegram.WebApp;
let main_button = tg.MainButton;

let files = [];
let reader = new FileReader();


const COLOR_GREEN = "text-green-500";
const COLOR_RED = "text-red-500";
const DEPENDENT_COUNTERS = [
    ['type', 128, true],
    ['address', 128, false],
    ['description', 512, false],
    ['price', 64, false],
    ['contacts', 128, false],
];

function toggleBlock() {
    let reds = document.getElementsByClassName(COLOR_RED);
    if (reds.length > 0) {
        main_button.disable();
    } else {
        main_button.enable();
    }
}

function toggle(cond, count) {
    if (cond) {
        count.classList.add(COLOR_GREEN);
        count.classList.remove(COLOR_RED); 
    } else {
        count.classList.add(COLOR_RED);
        count.classList.remove(COLOR_GREEN);
    }

    toggleBlock();
}


window.onload = () => {
    toggleBlock();

    DEPENDENT_COUNTERS.forEach(item => {
        let [name, max_len, req] = item;

        let tag = document.getElementById(name);
        let count = document.getElementById(`${name}_count`);

        let oninput = () => {
            let len = tag.value.length;
            count.innerText = `${len}/${max_len}`;

            let cond = len <= max_len
            if (req) { cond = cond && len > 0; }

            toggle(cond, count);
        };

        oninput();
        tag.oninput = oninput;
    });


    main_button.onClick(() => {
        let data = {
            type: document.getElementById('type').value,
            description: document.getElementById('description').value,
            price: document.getElementById('price').value,
            address: document.getElementById('address').value,
            contacts: document.getElementById('contacts').value,
            telegram: document.getElementById('telegram').checked,
            callback: "rent",
        };
 
        tg.sendData(JSON.stringify(data));
    });


    tg.expand();
    tg.enableClosingConfirmation();
    main_button.text = "Опубликовать";
    main_button.show();
};
