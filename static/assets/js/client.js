function updatePrice(clic,prixTot){
    let idType = document.getElementById("type_id").value;

    if(idType==0){
        return;
    }

    let valAjout = document.getElementById("va"+idType).innerHTML;
    document.getElementById("resultPrixTotal").innerHTML = ((prixTot)*valAjout) + clic;
}