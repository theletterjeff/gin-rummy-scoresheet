class Match {

  constructor() {
    this.players = {}
    this.gameCards = ""
    this.matchEndpoint = getMatchDetailEndpoint()
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

function getMatchDetailEndpoint() {
  const pageURL = new URL(window.location.href);
  const pageOrigin = pageURL.origin;
  const pagePath = pageURL.pathname;
  return `${pageOrigin}/api${pagePath}`;
}

function getGameListCreateEndpoint() {
  const pageURL = new URL(window.location.href);
  const pageOrigin = pageURL.origin;
  return `${pageOrigin}/api/game`
}

// Return a players object {username: endpoint}
async function getPlayers(matchData) {
  players = {}
  for (playerEndpoint of matchData.players) {
    let playerJSON = await getJSONResponsePromise(playerEndpoint)
    let username = await playerJSON.username;
    players[playerEndpoint] = username;
  };
  return players;
}

// Return a players object {endpoint: username}
async function getPlayersUsernameEndpoint(matchData) {
  players = {}
  for (playerEndpoint of matchData.players) {
    let playerJSON = await getJSONResponsePromise(playerEndpoint)
    let username = await playerJSON.username;
    players[username] = playerEndpoint;
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
          <div>
            <button class="btn btn-small btn-outline-info edit mx-1">Edit</button>
          </div>
          <div>
            <button class="btn btn-small btn-outline-dark delete mx-1">Delete</button>
          </div>
        </div>
      </div>
    </div>
  `
  return innerHTML;
}

class winnerDropdown {

  constructor() {
    this.winnerDropdown = document.getElementById('winner-dropdown')
  }

  async fillWinnerDropdown() {
    let matchEndpoint = getMatchDetailEndpoint();
    let players = await getJSONResponsePromise(matchEndpoint)
                  .then((matchData) => getPlayers(matchData));
    
    let dropdownOptions = ""

    Object.values(players).forEach(function(username) {
      let dropdownOption = `<option value=${username}>${username}</option>`;
      dropdownOptions += dropdownOption;
    })

    this.winnerDropdown.innerHTML = dropdownOptions;
  }
}

async function submitNewGameForm(e) {
  e.preventDefault();
  console.log('Form Submitted');
  
  const gameEndpoint = getGameListCreateEndpoint();
  const matchEndpoint = getMatchDetailEndpoint();

  let players = await getJSONResponsePromise(matchEndpoint)
                  .then((matchData) => getPlayersUsernameEndpoint(matchData));

  // Form fields
  let match = matchEndpoint;
  
  let winnerUsername = document.getElementById('winner-dropdown').value;
  let winnerEndpoint = players[winnerUsername];

  // Delete winner from `players`, leaving only the loser
  delete players[winnerUsername]
  let loserEndpoint = Object.values(players)[0]
  
  let points = document.getElementById('points-input').value;
  let gin = document.getElementById('gin-input');
  let undercut = document.getElementById('undercut-input');

  // Logged in user placeholder, switch out later when I figure out login
  let createdBy = winnerEndpoint

  fetch(gameEndpoint, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      'match': match,
      'winner': winnerEndpoint,
      'loser': loserEndpoint,
      'points': points,
      'gin': gin,
      'undercut': undercut,
      'created_by': createdBy,
    }),
  }).then((matchData) => match.fillPage());
}

let match = new Match();
match.fillPage();

let dropdown = new winnerDropdown();
dropdown.fillWinnerDropdown();

let form = document.getElementById('new-game-form');
form.addEventListener("submit", (e) => submitNewGameForm(e));