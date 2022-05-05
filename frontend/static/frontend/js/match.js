class Match {

  constructor() {
    this.players = {}
    this.gameCards = ""
    this.matchEndpoint = getMatchEndpoint()
    this.gameWrapper = document.getElementById("game-wrapper")
  }

  fillPage() {
    getJSONResponsePromise(this.matchEndpoint)
    .then(matchData => this.fillPlayers(matchData))
    .then(matchData => this.fillGames(matchData))
  }
    
  async fillPlayers(matchData) {
    let players = await getPlayers(matchData);
    this.players = players;
    return matchData;
  }

  async fillGames(matchData) {
    let gamesHTML = await getGamesHTML(matchData);

    for (let i in gamesHTML) {
      this.gameWrapper.innerHTML += gamesHTML[i];
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

async function getPlayers(matchData) {
  players = {}
  for (playerEndpoint of matchData.players) {
    let playerJSON = await getJSONResponsePromise(playerEndpoint)
    let username = await playerJSON.username;
    players[playerEndpoint] = username;
  };
  return players;
}

async function getGamesHTML(matchData) {
  let gamesHTML = [];
  let gameEndpoints = matchData.games;

  for (let i in gameEndpoints) {
    let gameData = await getJSONResponsePromise(gameEndpoints[i]);
    let gameHTML = makeCard(gameData, idx=i);
    
    const endpointRe = new RegExp('(http.*?)(?=")')

    let playerEndpoint = endpointRe.exec(gameHTML)[0]

    gameHTML = gameHTML.replace("#", this.players[playerEndpoint])
    gamesHTML.push(gameHTML);
  }
  return gamesHTML;
}

function makeCard(gameData, idx) {
  let winnerEndpoint = gameData.winner

  let datePlayed = new Date(gameData.datetime_played).toDateString()
  let points = gameData.points
  let gin = gameData.gin
  let undercut = gameData.undercut

  let innerHTML = `
    <div class="card mt-4 mb-4">
      <div class="card-body p-1">
        <div class="row m-0 mt-1 pl-2">
          <div class="card-title">${datePlayed}</div>
        </div>
        <div class="row m-0">
          <div class="col">
            <h6>Winner</h6>
            <h5><a href="${winnerEndpoint}" class="winner-link" id="winner-${idx}">#</a></h5>
          </div>
          <div class="col">
            <h6>Points</h6>
            <h5>${points}</h5>
          </div>
        </div>
      </div>
    </div>
  `
  return innerHTML;
}

let match = new Match();
match.fillPage();