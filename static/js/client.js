function linkCursor() {
     document.body.style.cursor = "pointer";
}

function normalCursor() {
    document.body.style.cursor = "default";
}

function afficherMessage(message){
    alert(message);
}

function add_money(){
    argent = prompt("combien voulez-vous ajouter ?\n" +
        " 10 % seront débité en plus pour les frais de transaction");
    if (isNaN(argent))
        alert("erreur nombre");
    else
        document.location.href="/client/info/add_money/"+argent;
}