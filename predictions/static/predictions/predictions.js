window.onload = function(){    

   let selector = document.querySelector("#sport");
    var pageTitle = document.title;
    selector.addEventListener('change',function(){

        let sport_id = selector.value;
        console.log(sport_id)
        if(sport_id == "no_sport"){
            removeChilds(document.getElementById('game'));
        }
        else{
            if(pageTitle == "GPTSportsWriter - Predictions" || pageTitle == "GPTSportsWriter - Parlays"){
                ajax_request(sport_id);
            }
            else {
                ajax_requestb(sport_id);
            }
        }
    });

function ajax_request(id){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     console.log(this.responseText);
     res = JSON.parse(this.responseText)
     games = res.games;
     odds = res.odds;
     removeChilds(document.getElementById('game'));
     for(const prop in games){
        add_option(games[prop],games[prop]);
     }
    }
  };
  xhttp.open("GET", `/ajax_handler/${id}`, true);
  xhttp.send();
}

function ajax_requestb(id){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     console.log(this.responseText);
     res = JSON.parse(this.responseText)
     games = res.games;
     removeChilds(document.getElementById('game'));
     for(const prop in games){
        add_option(games[prop],games[prop]);
     }
    }
  };
  xhttp.open("GET", `/ajax_handlerb/${id}`, true);
  xhttp.send();
}

function add_option(val,text){
    var sel = document.getElementById('game');
    
// create new option element
var opt = document.createElement('option');

// create text node to add to option element (opt)
opt.appendChild( document.createTextNode(text) );

// set value property of opt
opt.value = val; 

// add opt to end of select box (sel)
sel.appendChild(opt); 
}

}

var removeChilds = function (node) {
    var last;
    while (last = node.lastChild) node.removeChild(last);
};

