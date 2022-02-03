function linkCursor() {
     document.body.style.cursor = "pointer";
}

function normalCursor() {
    document.body.style.cursor = "default";
}

function getContent(sender, objetMail, message, id) {
    // console.log(sender, objetMail, message, id)
    let title = document.getElementById('Mtitle');
    let body = document.getElementById('Mbody');
    let from = document.getElementById('Mfooter');
    let idDelete = document.getElementById('Mfooter2');
    title.innerHTML = objetMail;
    body.innerHTML = message;
    from.innerHTML = 'from : ' + sender;
    idDelete.href = idDelete.getAttribute("href") + id;
}

function add_money(){
    argent = prompt("combien voulez-vous ajouter ?\n" +
        " 10 % seront débité en plus pour les frais de transaction");
    if (isNaN(argent))
        alert("erreur nombre");
    else
        document.location.href="/client/info/add_money/"+argent;
}