function add_money(){
    let argent = prompt("combien voulez-vous ajouter ?\n" +
        " 10 % seront débité en plus pour les frais de transaction");
    if (isNaN(argent))
        alert("erreur nombre");
    else
        document.location.href="/client/info/add_money/"+argent;
}