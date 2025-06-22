window.onload = function () {
    let selector = document.querySelector("#sport");
    var pageTitle = document.title;

    // Reference the game dropdown and submit button
    var gameSelect = document.getElementById('game');
    var submitBtn = document.getElementById('submitBtn');

    // Initial check: disable submit button if game dropdown is empty
    if (gameSelect && gameSelect.options.length === 0) {
        if (submitBtn) {
            submitBtn.disabled = true;
        }
    }

    selector.addEventListener('change', function () {
        let sport_id = selector.value;
        console.log(sport_id);

        if (sport_id == "no_sport") {
            removeChilds(gameSelect);

            // Disable submit button if no game is selected
            if (submitBtn) {
                submitBtn.disabled = true;
            }
        } else {
            if (pageTitle == "GPTSportsWriter - Predictions" || pageTitle == "GPTSportsWriter - Parlays" || pageTitle == "GPTSportsWriter - Props") {
                ajax_request(sport_id);
            } else {
                ajax_requestb(sport_id);
            }
        }
    });

    function ajax_request(id) {
        if (submitBtn) {
            submitBtn.disabled = true;
            openLoader();
        }

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4) {
                document.getElementById("loadingModal").style.display = "none";

                if (this.status == 200) {
                    try {
                        var res = JSON.parse(this.responseText);
                        var games = res.games || [];

                        removeChilds(gameSelect);

                        if (Array.isArray(games) && games.length > 0) {
                            // Add each game as an option
                            games.forEach(game => {
                                add_option(game.id, game.text);
                            });
                        } else {
                            // No games returned
                            add_option("", "No games available");
                        }

                    } catch (e) {
                        console.error("Error parsing JSON:", e);
                        add_option("", "Error loading games");
                    }
                } else {
                    console.error("AJAX request failed with status:", this.status);
                    add_option("", "Failed to load games");
                }

                // Enable/disable submit button based on game options
                if (gameSelect && gameSelect.options.length > 0) {
                    submitBtn.disabled = false;
                } else {
                    submitBtn.disabled = true;
                }
            }
        };
        xhttp.open("GET", `/ajax_handler/${id}`, true);
        xhttp.send();
    }

    function ajax_requestb(id) {
        if (submitBtn) {
            submitBtn.disabled = true;
            openLoader();
        }

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4) {
                document.getElementById("loadingModal").style.display = "none";

                if (this.status == 200) {
                    try {
                        var res = JSON.parse(this.responseText);
                        var games = res.games || [];

                        removeChilds(gameSelect);

                        if (Array.isArray(games) && games.length > 0) {
                            // Add each game as an option
                            games.forEach(game => {
                                add_option(game.id, game.text);
                            });
                        } else {
                            // No games returned
                            add_option("", "No games available");
                        }

                    } catch (e) {
                        console.error("Error parsing JSON:", e);
                        add_option("", "Error loading games");
                    }
                } else {
                    console.error("AJAX request failed with status:", this.status);
                    add_option("", "Failed to load games");
                }

                // Enable/disable submit button based on game options
                if (gameSelect && gameSelect.options.length > 0) {
                    submitBtn.disabled = false;
                } else {
                    submitBtn.disabled = true;
                }
            }
        };
        xhttp.open("GET", `/ajax_handlerb/${id}`, true);
        xhttp.send();
    }

    function add_option(val, text) {
        var sel = document.getElementById('game');
        var opt = document.createElement('option');
        opt.appendChild(document.createTextNode(text));
        opt.value = val;
        sel.appendChild(opt);
    }

    var removeChilds = function (node) {
        var last;
        while (last = node.lastChild) {
            node.removeChild(last);
        }
    };

    function openLoader() {
        document.getElementById("loadingModal").style.display = "block";
    }
};