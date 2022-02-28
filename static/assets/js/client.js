function updatePrice(clic,prixTot){
    let idType = document.getElementById("type_id").value;

    let idCoupon = "IGNORE";
    if(document.getElementById("couT") != null){
        idCoupon = document.getElementById("coupon_id").value;
    }


    if(idType==0){
        return;
    }

    let valAjout = document.getElementById("va"+idType).innerHTML;

    let valCoupon = 0;
    if (idCoupon != "IGNORE"){
        valCoupon = document.getElementById("cou"+idCoupon).innerHTML;
    }

    document.getElementById("resultPrixTotal").innerHTML = (( prixTot*valAjout + clic)
    *(100-valCoupon)/100).toFixed(2);
}