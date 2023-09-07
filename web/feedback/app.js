let tg = window.Telegram.WebApp;
let main_button = tg.MainButton;

let files = [];
let reader = new FileReader();


const COLOR_GREEN = "text-green-500";
const COLOR_RED = "text-red-500";
const DEPENDENT_COUNTERS = [
    ['who', 128, true],
    ['description', 512, false],
    ['contacts', 128, false],
];


function toggle(cond, count) {
    if (cond) {
        count.classList.add(COLOR_GREEN);
        count.classList.remove(COLOR_RED); 
    } else {
        count.classList.add(COLOR_RED);
        count.classList.remove(COLOR_GREEN);
    }
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

    let tag = document.getElementById('image_count');
    let text = document.getElementById('image_count_text');

    let onchange = () => {
        let value = tag.value;
        text.innerText = `${value}/5`;

        if (value == 0) {
            main_button.text = "Опубликовать";
        } else {
            main_button.text = "Приложить фотографии и опубликовать";
        }
    };

    onchange();
    tag.onchange = onchange;


    main_button.onClick(() => {
        let reds = document.getElementsByClassName(COLOR_RED);
        if (reds.length > 0) {
            tg.showAlert('Заполните все поля правильно!', callback)
            return;
        }

        let data = {
            who: document.getElementById('who').value,
            description: document.getElementById('description').value,
            contacts: document.getElementById('contacts').value,
            telegram: document.getElementById('telegram').checked,
            callback: "feedback",
        };
 
        tg.sendData(JSON.stringify(data));
    });


    tg.expand();
    tg.enableClosingConfirmation();
    main_button.text = "Опубликовать";
    main_button.show();
};

