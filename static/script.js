function noData() {
    document.getElementById('response-image').src = '';
    [...document.getElementsByClassName('data-row')].forEach(element => {
        element.children[1].innerText = '-';
    });
}


function loadingData() {
    noData();
}


function formatNumber(x) {
    if (isNaN(x))
        return x;

    if (x === 0)
        return 0;

    const sign = x > 0 ? 1 : -1;
    x *= sign;
    let e = 0;
    while (x >= 10) {
        x /= 10;
        ++e;
    }
    while (x < 1) {
        x *= 10;
        --e;
    }
    return (x * sign).toFixed(4) + '&middot;10<sup>' + e + '</sup>'
}


function loadedData({img, data}) {
    noData();
    document.getElementById('response-image').src = img;
    Object.keys(data).forEach(key => {
        const element = document.getElementById(key);
        if (element)
            element.innerHTML = formatNumber(data[key].value) + '&nbsp;' + (data[key].unit || '');
    });
}


function loadFigure() {
    loadingData();
    fetch('/backend', {
        method: 'POST',
        body: new FormData(document.getElementById('form')),
        cache: 'no-cache'
    }).then(res => {
        return res.json();
    }).then(res => {
        if (res.error)
            throw Error(res.error);

        loadedData(res);
    }).catch(err => {
        alert(err.message);
    });
}


function fillValues(values) {
    if (!values instanceof Array)
        throw Error("Podaj listę");
    if (values.length !== 12)
        throw Error("Zły rozmiar");

    let it = values[Symbol.iterator]();
    [...document.getElementById('form').getElementsByTagName('input')].
    forEach(element => {
        element.value = it.next().value;
    });
}


function loadExample() {
    fillValues([
        1.98855, 30,
        5.97219, 24,
        0, 0,
        1.49598261, 11,
        3, 4,
        0, 0
    ]);
    loadFigure();
}


function scrollToElement(e, element) {
    e.preventDefault();
    document.getElementById('panel-container').style.left = -(
        [...document.getElementsByClassName('panel')].indexOf(element) * 100
    ) + 'vw';
    document.getElementsByClassName('active')[0].classList.remove('active');
    e.target.classList.add('active');
}