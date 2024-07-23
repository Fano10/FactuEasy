
function load_data(article, prix){
  /*
   Cette fonction afficher les articles et les prix dans leurs emplacements dédiées

  Arg:
      article(array(1,0)) : contients les articles
      prix(array(1,0)): contient les prix
  Return: none
  */
    let ulArticle = document.getElementsByClassName('sortable-list-article')[0];
    let ulPrix = document.getElementsByClassName('sortable-list-prix')[0];
    let tailleArticle = article.length;
    let taillePrix = prix.length;
    for (let i=0 ;i <tailleArticle ; i++){
        let li = document.createElement('li');
        li.className = 'item-article';
        li.draggable = true; // permet d'attribuer l'attribut draggable pour permettre le drag and drop
        li.innerHTML = article[i];
        li.addEventListener('dblclick',function(){ //
            // Lorsqu'on double click sur l'élément, il devient modifiable
            this.setAttribute('contenteditable','true');
            this.focus();
          });
          li.addEventListener('blur',function(){
            //Lorsqu'il perd le focus, l'élément devient normal
            this.removeAttribute('contenteditable');
        })
        ulArticle.appendChild(li);
        addDragAndDropEvents(li, 'article');
    }
    for (let i=0 ;i <taillePrix ; i++){
        let li = document.createElement('li');
        li.className = 'item-prix';
        li.draggable = true;
        li.innerHTML = prix[i];
        li.addEventListener('dblclick',function(){
            this.setAttribute('contenteditable','true');
            this.focus();
          });
          li.addEventListener('blur',function(){
            this.removeAttribute('contenteditable');
        })
        ulPrix.appendChild(li);
        addDragAndDropEvents(li, 'prix');
    }
}
function ajouter() {
  /*
  Cette fonction permet de définir les actions des deux boutons + pour ajouter un nouveau articles ou un nouveau prix

  Arg: none
  Return: none
  */
    let listeArticle = document.getElementsByClassName('sortable-list-article')[0];
    let listePrix = document.getElementsByClassName('sortable-list-prix')[0];
    let addArticle = document.getElementById('add-article');
    let addPrix = document.getElementById('add-prix');
  
    addArticle.addEventListener('click', function () {
      let li = document.createElement('li');
      li.className = 'item-article';
      li.draggable = true;
      li.innerHTML = 'Nouveau Produit';
      li.addEventListener('dblclick',function(){
        this.setAttribute('contenteditable','true');
        this.focus();
      });
      li.addEventListener('blur',function(){
        this.removeAttribute('contenteditable');
      })
      listeArticle.appendChild(li);
      addDragAndDropEvents(li, 'article');
    });
  
    addPrix.addEventListener('click', function () {
      let li = document.createElement('li');
      li.className = 'item-prix';
      li.draggable = true;
      li.innerHTML = 'Nouveau Prix';
      li.addEventListener('dblclick',function(){
        this.setAttribute('contenteditable','true');
        this.focus();
      });
      li.addEventListener('blur',function(){
        this.removeAttribute('contenteditable');
      })
      listePrix.appendChild(li);
      addDragAndDropEvents(li, 'prix');
    });
  }
  
  function addDragAndDropEvents(item, type) {
    /* 
    Cette fonction permet d'ajouter et d'enlever la classe dragging-(string) a un élément
    Cela permet de manipuler l'item lors du drag and drop

    Arg:
        item(objet) : plus précisement l'élément li
        type(string): pour le type d'élement: prix ou articles
    
    Return:none
    */
    const draggingClass = `dragging-${type}`;
    item.addEventListener("dragstart", () => {
      //Lorsqu'on commence à selectionner l'élément, ajouter la classe
      setTimeout(() => item.classList.add(draggingClass), 0);
    });
      //Lorsqu'on lache l'élément, supprimer la classe
    item.addEventListener("dragend", () => item.classList.remove(draggingClass));
  }
  
  function glisser_deposer() {
    /*
    Cette fonction gère toutes les actions de drag and drop. Que ce soit la permutations des éléments ou la suppréssion d'un élément lorsqu'il est drop à l'exterieur de son parent

    Arg: none
    Return: none
    */
    // Sélection les 2 parents(ul) qui contients toutes les listes
    const sortableListArticle = document.querySelector(".sortable-list-article");
    const sortableListPrix = document.querySelector(".sortable-list-prix");
  
    const itemsArticles = sortableListArticle.querySelectorAll(".item-article");
    const itemsPrix = sortableListPrix.querySelectorAll(".item-prix");
    // 
    const initSortableList = (e, sortableList, draggingClass) => {
    /* 
    Fonction pour réorganiser la liste des articles
     Arg:
        e(objetc): c'est l'événement par défaut
        sortableList(object) : ici c'est l'élément parent
        draggingClass(String): la classe de l'élément enfant qu'on veut drap and drop
    */
      
      e.preventDefault();
      //selectionner l'élément en drag and drop
      const draggingItem = document.querySelector(`.${draggingClass}`);
      //selectionner ces frères sauf lui
      let siblings = [...sortableList.querySelectorAll(`li:not(.${draggingClass})`)];
      //Chercher le voisin le plus proche de son emplacement
      let nextSibling = siblings.find(sibling => e.clientY <= sibling.offsetTop + sibling.offsetHeight / 2);
      //Inserer l'éléemnt en dessus des cet voisin
      sortableList.insertBefore(draggingItem, nextSibling || null);
    };
    //par défaut le dépot n'est pas autorisé par le navigateur

    //Lorsque l'élément se déplace dans la zone de drop
    sortableListArticle.addEventListener("dragover", e => initSortableList(e, sortableListArticle, 'dragging-article'));
    //Lorsque l'élément entre dans la zone de drop
    sortableListArticle.addEventListener("dragenter", e => e.preventDefault());
  
    sortableListPrix.addEventListener("dragover", e => initSortableList(e, sortableListPrix, 'dragging-prix'));
    sortableListPrix.addEventListener("dragenter", e => e.preventDefault());
  
    document.addEventListener("dragover", e => e.preventDefault());
  
    document.addEventListener("drop", e => {
      /*
      supprimer l'élément lorsqu'il est dehors de son contexte
      */
      const draggingItemArticle = document.querySelector(".dragging-article");
      const draggingItemPrix = document.querySelector(".dragging-prix");
  
      if (draggingItemArticle && !sortableListArticle.contains(e.target)) {
        draggingItemArticle.remove();
      }
  
      if (draggingItemPrix && !sortableListPrix.contains(e.target)) {
        draggingItemPrix.remove();
      }
    });
  }
function chargement_page(){
  /**
  Cette fonction afficher le div de loading et cache l'ancien page

  Args: none
  Return: none
  **/
    let divUpload = document.getElementsByClassName('upload')[0];
    let divLoading = document.getElementsByClassName('loading')[0];
    divUpload.style.display = 'none';
    divLoading.style.display = 'block';
}
function affichage_resultat(){
  /*
  Cette fonction fait 2 taches:
    a) cache le div de loading et prépare le div pour écrire le résultat
    b) définit l'événement de onclick du bouton valider

  Arg: none
  return: none
   */
    let divLoading = document.getElementsByClassName('loading')[0];
    let divResultat = document.getElementsByClassName('resultat')[0];
    let bouton_resultat = document.getElementById('bouton_valider');

    divLoading.style.display = 'none';
    divResultat.style.display = 'block';
    bouton_resultat.onclick = function (){
        let articles = [];
        let prixs  = [] ;
        url = '/apiAddBills'; //url
        urlRedict = '/allBills'; // url
        let itemsArticles = document.querySelectorAll('.item-article');
        let itemPrix =  document.querySelectorAll('.item-prix');
        itemsArticles.forEach(article => {
            articles.push(article.innerHTML);
        });
        itemPrix.forEach(prix =>{
            prixs.push(prix.innerHTML);
        });
        //si l'articles et le prix n'ont pas la meme taille
        if(articles.length !== prixs.length){
            let dialog = document.querySelector("dialog");
            let boutonDialog = document.getElementById("close_dialog")
            boutonDialog.addEventListener('click', ()=>{
              dialog.close();
            })
            dialog.showModal();
        }
        else{
            let data = {
              'articles' : articles,
              'prix' : prixs
            };
            data = JSON.stringify(data);
            //Envoye des informations à notre API pour qu'il enregistre les factures
            fetch(url, {
              method : 'POST',
              headers : {'Content-Type' : 'application/json'},
              credentials: 'include',
              body : data
            })
            .then(response => response.json())
            .then(data => {
              if(data.success) {
                //Si l'enregistrement c'est bien passer. Faire une redirection vers la page de facture
                window.location.href = urlRedict;
              }
              else {
                  alert('Nous rencontrons un probleme actuellement, veuillez reessayer plus tard');
              }
            })
            .catch(error => {
            console.error('Fetch error:',error);
          })
        }
    }
}
function main(){
    let inputFile = document.getElementById('input-file');
    //lorsqu'on a fini d'uploader une image:
    inputFile.onchange = function(){
        image = inputFile.files[0];
        let data = new FormData();
        data.append('image',image);
        url = '/upload'; //changer avec mon url
        chargement_page();
        fetch(url,{
            method: 'POST',
            body: data
        })
        .then(response => response.json())
        .then(data => {
            if(data.success){
                affichage_resultat();
                load_data(data.message.article, data.message.prix);
                ajouter();
                glisser_deposer();
            }
            else{
                alert('Erreur lors de l upload de l image');
            }
        })
        .catch(error =>{
            console.error('Erreur: ',error);
        })
    }
}



window.onload = main;