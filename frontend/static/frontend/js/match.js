import {fillTitle} from "./base.js";

fillMatchDetailPage();

// Functions

/** Main execution function */
async function fillMatchDetailPage() {
  fillTitle('Match');

  const matchDetailEndpoint = getMatchDetailEndpoint();
  let playersEndpointUsername = await getPlayersEndpointUsername(matchDetailEndpoint);
  
  fillWinnerDropdown();
  listGames(playersEndpointUsername);

  let newGameForm = document.getElementById("new-game-form");
  newGameForm.addEventListener("submit", (e) => submitNewGameForm(e));
}

/** Get cookie value (used to pass CSRF token to POST requests) */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

/** Fill the `game-wrapper` element with a list of game details */
async function listGames(playersEndpointUsername) {
  let matchDetailJSON = await getMatchDetailJSON();
  let gamesHTML = await getGamesHTML(matchDetailJSON, playersEndpointUsername);

  let gameWrapper = document.getElementById("game-table-body");
  gameWrapper.innerHTML = ""

  for (let gameHTML of gamesHTML) {
    gameWrapper.innerHTML += gameHTML;
  }
}

/** Return the endpoint for the MatchDetail API view */
function getMatchDetailEndpoint() {
  const pageURL = new URL(window.location.href);
  const pageOrigin = pageURL.origin;
  const pagePath = pageURL.pathname;
  return `${pageOrigin}/api${pagePath}`;
}

/** Return the endoint for the GameListCreate API view */
function getGameListCreateEndpoint() {
  const pageURL = new URL(window.location.href);
  const pageOrigin = pageURL.origin;
  return `${pageOrigin}/api/game`
}

function getJSONResponsePromise(endpoint) {
  let json = fetch(endpoint)
             .then((response) => response.json());
  return json;
}

async function getMatchDetailJSON() {
  const matchDetailEndpoint = getMatchDetailEndpoint()
  return await getJSONResponsePromise(matchDetailEndpoint);
}

/* Return a players object {username: endpoint} */
async function getPlayersEndpointUsername(matchDetailEndpoint) {
  let players = {}
  let matchData = await getJSONResponsePromise(matchDetailEndpoint)

  for (let playerEndpoint of matchData.players) {
    let playerJSON = await getJSONResponsePromise(playerEndpoint)
    let username = await playerJSON.username;
    players[playerEndpoint] = username;
  };

  return players;
}

/** Return a players object {endpoint: username} */
async function getPlayersUsernameEndpoint(matchDetailEndpoint) {
  let players = await getPlayersEndpointUsername(matchDetailEndpoint);
  let playersFlipped = {};

  // Make the keys into values and the values into keys
  Object.entries(players).forEach(([key, value]) => {playersFlipped[value] = key});
  
  return playersFlipped;
}

/* Return an array of game table row HTML elements */
async function getGamesHTML(matchData, playersEndpointUsername) {
  let gamesHTML = [];
  let gameEndpoints = matchData.games;

  for (let gameEndpoint of gameEndpoints) {
    let gameData = await getJSONResponsePromise(gameEndpoint);
    let gameHTML = makeGameTableRow(gameData);
    
    const endpointRe = new RegExp('(http.*?)(?=")')

    let playerEndpoint = endpointRe.exec(gameHTML)[0]

    gameHTML = gameHTML.replace("#", playersEndpointUsername[playerEndpoint])
    gamesHTML.push(gameHTML);
  }
  return gamesHTML;
}

function makeGameTableRow(gameData) {
  let winnerEndpoint = gameData.winner

  let datePlayed = new Date(gameData.datetime_played).toDateString()
  let points = gameData.points

  let gin = gameData.gin
  let ginCheck = gin ? "X" : ""

  let undercut = gameData.undercut
  let undercutCheck = undercut ? "X" : ""

  let innerHTML = `
    <tr>
      <td>${datePlayed}</td>
      <td><a href="${winnerEndpoint}">#</a></td>
      <td>${points}</td>
      <td class="checkbox-cell">${ginCheck}</td>
      <td class="checkbox-cell">${undercutCheck}</td>
      <td class="button-cell"><button class="btn btn-small btn-outline-info edit">Edit</button></td>
      <td class="button-cell"><button class="btn btn-small btn-outline-dark delete">Delete</button></td>
    </tr>
  `
  return innerHTML;
}

async function fillWinnerDropdown() {
  let matchEndpoint = getMatchDetailEndpoint();
  let players = await getPlayersEndpointUsername(matchEndpoint);
  
  let dropdownOptions = ""

  Object.values(players).forEach(function(username) {
    let dropdownOption = `<option value=${username}>${username}</option>`;
    dropdownOptions += dropdownOption;
  })

  let winnerDropdown = document.getElementById('winner-dropdown');
  winnerDropdown.innerHTML = dropdownOptions;
}

async function submitNewGameForm(e) {
  e.preventDefault();
  
  const csrfToken = getCookie("csrftoken");
  
  const gameEndpoint = getGameListCreateEndpoint();
  const matchDetailEndpoint = getMatchDetailEndpoint();
  
  let playersUserEnd = await getPlayersUsernameEndpoint(matchDetailEndpoint);
  let playersEndUser = await getPlayersEndpointUsername(matchDetailEndpoint)

  // Form fields
  let match = matchDetailEndpoint;
  
  let winnerUsername = document.getElementById('winner-dropdown').value;
  let winnerEndpoint = playersUserEnd[winnerUsername];
  
  // Delete winner from `players`, leaving only the loser
  delete playersUserEnd[winnerUsername]
  let loserEndpoint = Object.values(playersUserEnd)[0]
  
  let points = document.getElementById('points-input').value;
  let gin = document.getElementById('gin-input').value;
  let undercut = document.getElementById('undercut-input').value;
  
  // Logged in user placeholder, switch out later when I figure out login
  let createdBy = winnerEndpoint

  fetch(gameEndpoint, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
      'X-CSRFToken': csrfToken,
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
  }).then(() => listGames(playersEndUser));
  
  console.log('Form Submitted');
}
