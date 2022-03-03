
let pos = "10";
function updatePosOfPierre(){
    document.getElementById(pos.toString()).style.fill = "#FFFFFF";
    pos = (Math.floor(Math.random() * 94 + 1)).toString();
    while(pos.length < 2){
        pos = "0"+pos;
    }
    if(pos==="20"){
        pos = "2A";
    }
    console.log(pos);
    document.getElementById(pos.toString()).style.fill = "blue";
    setTimeout(function(){updatePosOfPierre(); }, 500);

}