function linkCursor() {
     document.body.style.cursor = "pointer";
}

function normalCursor() {
    document.body.style.cursor = "default";
}

function getContent(sender, objetMail, message, id) {
    // console.log(sender, objetMail, message, id)
    let title = document.getElementById('exampleModalLongTitle');
    let body = document.getElementById('Mbody');
    let from = document.getElementById('Mfooter');
    let idDelete = document.getElementById('Mfooter2');

    title.innerHTML = objetMail;
    body.innerHTML = message;
    from.innerHTML = 'from : ' + sender;
    idDelete.href = "/mails/delete?id=" + id;
}