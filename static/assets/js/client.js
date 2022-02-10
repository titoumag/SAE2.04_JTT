function updatePrice(clic,prixTot){
    let valAjout = document.getElementById("valAjoute").value;
    document.getElementById("resultPrixTotal").innerHTML = ((prixTot)*valAjout) + clic;
}