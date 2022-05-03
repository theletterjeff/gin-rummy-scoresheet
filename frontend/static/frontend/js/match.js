class Match {

  constructor() {
    this.players = {}
    this.matchEndpoint = getMatchEndpoint()
    this.gameWrapper = document.getElementById("game-wrapper")
  }

  fillPage() {
    getJSONResponsePromise(this.MatchEndpoint)
    .then(function(matchData) {
      let players = getPlayers(matchData);
      this.players.push(players);
      return matchData;
    })
    .then(function(matchData) {
      let gameEndpoints = matchData.games;
      for (let i in gameEndpoints) {
        getJSONResponsePromise(gameEndpoints[i])
        .then(function(gameData) {
          this.gameWrapper += makeCard(gameData, this.players, i)
        });
      };
    });
  }
}


function getJSONResponsePromise(endpoint) {
  let json = fetch(endpoint)
             .then((response) => response.json);
  return json;
}

function getPlayers(matchData) {
  players = {}
  for (playerEndpoint of matchData.players) {
    getJSONResponsePromise(playerEndpoint)
    .then(function(playerData) {
      players[playerEndoint] = playerData.username;
    });
  };
}

function makeCard(gameData, playersObj, idx) {
  let winnerEndpoint = gameData.winner
  let winnerUsername = playersObj[winnerEndpoint]

  let datePlayed = new Date(gameData.datetime_played).toDateString()
  let points = gameData.points
  let gin = gameData.gin
  let undercut = gameData.undercut

  let innerHTML = `
    <div class="card mt-4 mb-4" id="game-card-${idx}">
      <div class="card-body row">
        <div class="col">
          <h6>Winner</h6>
          <h5>${winnerUsername}</h5>
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