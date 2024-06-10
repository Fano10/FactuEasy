//-----------------------------definition des classes--------------------------------------------
class Bill {
    constructor(id,name,date,total){
        this.id = id;
        this.name = name;
        this.date = date;
        this.total = total;
    }
}



var identifiant = ["1","2"]
var centre = ["Maxi","Maxi"];
var date = ["2024-05-10","2024-02-11"]
var total = ["15,15","40,23"]

function Ajax(method,url){
    //Creation de l'objet Ajax
    let xhr = new XMLHttpRequest();
    //Definir la requete que l'on veut faire
    xhr.open(method,url);
    xhr.onload = function(){
        if(xhr.status ===200){
            let data = JSON.parse(xhr.responseText);
            data = data["bills"];
            createTableBills(data);
            //alert('OK')
        }
        else{
            alert('Problem')
        }
    };
    //Envoyer la requete
    xhr.send();

}


function addBill(tbody, id, name, date, total, link){
    //creation des lignes
    let tr = document.createElement("tr");
    //Colonne nom
    let tdName = document.createElement("td");
    tdName.innerHTML = name;
    //Colonne date
    let tdDate = document.createElement("td");
    tdDate.innerHTML=date;
    //Colonne total
    let tdTotal = document.createElement("td");
    tdTotal.innerHTML = total;
    //Colonne consulter
    let tdLink = document.createElement("td");
    let aLink = document.createElement("a");
    aLink.href = link + id ;
    aLink.innerHTML = "Consulter";
    tdLink.appendChild(aLink);
    //Attacher les td sur le tr
    tr.appendChild(tdName);
    tr.appendChild(tdDate);
    tr.appendChild(tdTotal);
    tr.appendChild(tdLink);
    //Attacher le tr sur le tbody
    tbody.appendChild(tr);
}

function createTableBills(data){
    let tbody = document.querySelector("tbody");
    let size = data.length;
    for(let i=0; i<size;i++){
        addBill(tbody,"",data[i]["name"],data[i]["date"],data[i]["total"],"allBills.html");
    }
}

function main(){
    let method = 'GET';
    let URL = 'http://127.0.0.1:5000/allBill';
    Ajax(method,URL);
}

window.onload = main;