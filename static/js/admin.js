function details(id) {
    const url = "http://127.0.0.1:5000/admin/commande/" + id
    location.replace(url);
}

function linkCursor() {
     document.body.style.cursor = "pointer";
}

function normalCursor() {
    document.body.style.cursor = "default";
}