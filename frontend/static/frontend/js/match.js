fillMatchesNavLink();
let players = getPlayers(); 
listGames(players);
fillWinners();

// Derive the match's endpoint from the current page's URL
function getMatchEndoint() {
    const pageURL = new URL(window.location.href);
    const pageOrigin = pageURL.origin;
    const pagePath = pageURL.pathname;
    return `${pageOrigin}/api${pagePath}`;
};

function getPlayers() {
    let matchEndpoint = getMatchEndoint();
    let players = [];

    fetch(matchEndpoint)
    .then((resp) => resp.json())
    .then(function(data) {
        console.log(data.players);
        for (playerEndpoint of data.players) {
            fetch(playerEndpoint)
            .then((resp) => resp.json())
            .then(function(playerData) {
                players.push(playerData);
            });
        };
    });
    return players;
};

/**
 * Take in an array of Player objects, return an object mapping 
 * endpoint to username. Used to cross-reference the player endpoints 
 * we get back from listGames.
 * @param {Object} players  Player data loaded from API.
 */
function getPlayerUsernames(players) {
    let endpointUsername = {};
    for (let player of players) {
        endpointUsername[player.url] = player.username;
    };
    return endpointUsername;
}

/**
 * Build a list of games and fill div with data from those games.
 * @param {Object} players   Player data loaded from API.
 */
function listGames(players) {
    
    let wrapper = document.getElementById('game-wrapper');
    let matchEndpoint = getMatchEndoint();
    let playerUsernames = getPlayerUsernames(players);

    fetch(matchEndpoint)
    .then((resp) => resp.json())
    .then(function(data) {
        let gameEndpoints = data.games;

        for (let i in gameEndpoints) {

            fetch(gameEndpoints[i])
            .then((response) => response.json())
            .then(function(data) {
                let item = makeCard(data, idx=i);
                wrapper.innerHTML += item;
                return data;
            })
            .then(() => fillWinners());
            
            
        };
    
    });
    
    
};

function makeCard(gameResponseJson, idx) {
    
    let winnerEndpoint = gameResponseJson.winner
    let datePlayed = new Date(gameResponseJson.datetime_played).toDateString()
    let points = gameResponseJson.points
    let gin = gameResponseJson.gin
    let undercut = gameResponseJson.undercut

    let innerHTML = `
        <div class="card mt-4 mb-4" id="game-card-${idx}">
            <div class="card-body row">
                <div class="col">
                    <h6>Winner</h6>
                    <h5 class="winner">${winnerEndpoint}<h5>
                </div>
                <div class="col">
                    <h6>Played</h6>
                    <h5>${datePlayed}</h5>
                </div>
                <div class="col">
                    <h6>Points</h6>
                    <h5>+${points}</h5>
                </div>
            </div>
        </div>
    `;

    return innerHTML;
};

function fillWinners() {
    let winnerElems = document.getElementsByClassName("winner");

    for (let winnerElem of winnerElems) {
        fetch(winnerElem.innerHTML)
        .then((response) => response.json())
        .then(function(data) {
            winnerElem.innerHTML = data.username;
        });
    };

};

function getUsername(playerEndpoint) {
    let username = fetch(playerEndpoint)
    .then((resp) => resp.json())
    .then(function(data) {
        return data.username;
    });
    return username;
};

function getMatchesURL() {
    const pageURL = new URL(window.location.href);
    const pageOrigin = pageURL.origin;
    return pageOrigin + "/api/matches";
};
function fillMatchesNavLink() {
    const matchesURL = getMatchesURL();
    matchesNavElem = document.getElementById("matches-nav-link");
    matchesNavElem.href = matchesNavElem.href.replace(
        "#", matchesURL);
};