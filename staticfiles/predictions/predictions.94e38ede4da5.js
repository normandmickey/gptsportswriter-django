window.onload = function(){
        

    let selector = document.querySelector("#sport");
    selector.addEventListener('change',function(){

        let sport_id = selector.value;
        console.log(sport_id)
        if(sport_id == "no_sport"){
            hideSpinner()
            removeChilds(document.getElementById('game'));
        }
        else{
            ajax_request(sport_id);
        }
        
    });


function ajax_request(id){
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
  xhttp.open("GET", `/ajax_handler/${id}`, true);
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

// Function to hide the Spinner 
function hideSpinner() { 
    document.getElementById('spinner') 
            .style.display = 'none'; 
}  