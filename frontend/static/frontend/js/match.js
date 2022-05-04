class Match {

  constructor() {
    this.players = {}
    this.matchEndpoint = getMatchEndpoint()
  }

  fillPage() {
    getJSONResponsePromise(this.matchEndpoint)
    .then(matchData => this.fillPlayers(matchData))
    .then(matchData => this.fillGames(matchData))
  }
    
  fillPlayers(matchData) {
    let players = getPlayers(matchData);
    this.players = players;
    return matchData;
  }

  async fillGames(matchData) {
    let gamesHTML = await getGamesHTML(matchData);

    for (let card of gamesHTML) {
      document.getElementById("game-wrapper") += card;
    };
  }

}



function getJSONResponsePromise(endpoint) {
  let json = fetch(endpoint)
             .then((response) => response.json());
  return json;
}

function getMatchEndpoint() {
  const pageURL = new URL(window.location.href);
  const pageOrigin = pageURL.origin;
  const pagePath = pageURL.pathname;
  return `${pageOrigin}/api${pagePath}`;
}

function getPlayers(matchData) {
  players = {}
  for (playerEndpoint of matchData.players) {
    let username = getJSONResponsePromise(playerEndpoint)
                   .then(function(playerData) {
                     return playerData.username;
                    });
    players[playerEndpoint] = username;
  };
  return players;
}

async function getGamesHTML(matchData) {
  let gamesHTML = [];
  let gameEndpoints = matchData.games;

  for (gameEndpoint of gameEndpoints) {
    let gameData = await getJSONResponsePromise(gameEndpoint);
    let gameHTML = makeCard(gameData);

    gamesHTML.push(gameHTML);
  }
  return gamesHTML;
}

function makeCard(gameData) {
  let winnerEndpoint = gameData.winner

  let datePlayed = new Date(gameData.datetime_played).toDateString()
  let points = gameData.points
  let gin = gameData.gin
  let undercut = gameData.undercut

  let innerHTML = `
    <div class="card mt-4 mb-4">
      <div class="card-body row">
        <div class="col">
          <h6>Winner</h6>
          <h5>${winnerEndpoint}</h5>
        </div>
        <div class="col">
          <h6>Played</h6>
          <h5>${datePlayed}</h5>
        </div>
        <div class="col">
          <h6>Points</h6>
          <h5>${points}</h5>
        </div>
      </div>
    </div>
  `
  return innerHTML;
}

let match = new Match();
match.fillPage();