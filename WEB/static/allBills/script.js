
var GLOBAL_DATA = []
var signeTrieIdentifiant = 0
function Ajax(method,url,urlRedirct){
    //Creation de l'objet Ajax
    let xhr = new XMLHttpRequest();
    //Definir la requete que l'on veut faire
    xhr.open(method,url);
    // Ajouter le cookie sur l'en-tete
    xhr.withCredentials = true;
    //Ajouter les en-tetes CORS necessaires
    xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhr.setRequestHeader('Access-Control-Allow-Credentials', 'true');
    xhr.onload = function(){
        if(xhr.status ===200){
            let data = JSON.parse(xhr.responseText);
            data = data["bills"];
            GLOBAL_DATA = data["bills"];
            createTableBills(data);
            //alert('OK')
        }
        else if (xhr.status === 401) {
            window.location.href = urlRedirct
        }
        else{
            alert('Problem')
        }
    };
    //Envoyer la requete
    xhr.send();

}


function sortArray(type_colonne){
    let taille  = GLOBAL_DATA.length
    let intermediaire;
    for (let i=0 ; i<taille ; i++){
        for(let a = i+1; a < taille ; a++){
            if(type_colonne ==="Date"){
                if (GLOBAL_DATA[i]["date"] < GLOBAL_DATA[a]["date"] && signeTrieIdentifiant % 2 ===0){
                    intermediaire = GLOBAL_DATA[a];
                    GLOBAL_DATA[a] = GLOBAL_DATA[i];
                    GLOBAL_DATA[i] = intermediaire;
                }
                if (GLOBAL_DATA[i]["date"] > GLOBAL_DATA[a]["date"] && signeTrieIdentifiant % 2 ===1){
                    intermediaire = GLOBAL_DATA[a];
                    GLOBAL_DATA[a] = GLOBAL_DATA[i];
                    GLOBAL_DATA[i] = intermediaire;
                }
            }
            else{
                if (GLOBAL_DATA[i]["total"] < GLOBAL_DATA[a]["total"] && signeTrieIdentifiant % 2 ===0){
                    intermediaire = GLOBAL_DATA[a];
                    GLOBAL_DATA[a] = GLOBAL_DATA[i];
                    GLOBAL_DATA[i] = intermediaire;
                }
                if (GLOBAL_DATA[i]["total"] > GLOBAL_DATA[a]["total"] && signeTrieIdentifiant % 2 ===1){
                    intermediaire = GLOBAL_DATA[a];
                    GLOBAL_DATA[a] = GLOBAL_DATA[i];
                    GLOBAL_DATA[i] = intermediaire;
                }
            }
        }
    }
    signeTrieIdentifiant ++;
    removeArrayTr();
    createTableBills(GLOBAL_DATA);
}

function removeArrayTr(){
    let tr = document.querySelectorAll("tbody tr");
    tr.forEach(item => item.remove());
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
    let link = '/item/'
    let tbody = document.querySelector("tbody");
    let size = data.length;
    for(let i=0; i<size;i++){
        addBill(tbody,data[i]["id"],data[i]["name"],data[i]["date"],data[i]["total"],link);
    }
}

function main(){
    let method = 'GET';
    let URL = '/apiAllBills'; //a changer
    let urlRedirct = '/login'
    
    Ajax(method,URL,urlRedirct);
}

window.onload = main;