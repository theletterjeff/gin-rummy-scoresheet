import { getJsonResponse, fillTitle, getCookie } from "./utils.js";
import { getApiDetailEndpoint, getPlayersEndpointUsername, getFrontendURL } from './endpoints.js';


import { fillWinnerDropdown, submitGameForm } from "./game-form.js";

fillMatchDetailPage();

/** Main execution function */
async function fillMatchDetailPage() {
  fillTitle('Match');

  const matchDetailEndpoint = getApiDetailEndpoint();
  let playersEndUser = await getPlayersEndpointUsername(matchDetailEndpoint);
  
  fillWinnerDropdown(matchDetailEndpoint);
  listGames(playersEndUser);

  let newGameForm = document.getElementById("new-game-form");
  newGameForm.addEventListener("submit", function(e) {
    submitGameForm(e, 'POST')
    .then(() => document.getElementById('new-game-form').reset())
    .then(() => listGames(playersEndUser))
  });
}

/** Fill the `game-wrapper` element with a list of game details */
async function listGames(playersEndpointUsername) {
  let matchEndpoint = getApiDetailEndpoint()
  let matchDetailJson = await getJsonResponse(matchEndpoint);
  let gamesHTML = await getGamesHTML(matchDetailJson, playersEndpointUsername);

  let gameWrapper = document.getElementById("game-table-body");
  gameWrapper.innerHTML = "";
  gamesHTML.forEach(addGameRowToPage);
  addEditDeleteButtons(matchDetailJson);
}

/* Return an array of game table row HTML elements */
async function getGamesHTML(matchData, playersEndpointUsername) {
  let gamesHTML = [];
  let gameEndpoints = matchData.games;

  for (let gameEndpoint of gameEndpoints) {
    let gameData = await getJsonResponse(gameEndpoint);
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
      <td class="button-cell"><button class="btn btn-small btn-outline-success edit">Edit</button></td>
      <td class="button-cell"><button class="btn btn-small btn-outline-secondary delete">Delete</button></td>
    </tr>
  `
  return innerHTML;
}

function addGameRowToPage(gameHTML) {
  let gameWrapper = document.getElementById('game-table-body');
  gameWrapper.innerHTML += gameHTML;
}

async function addEditDeleteButtons(matchDetailJson) {
  let gameEndpoints = matchDetailJson.games;
  let editBtns = document.getElementsByClassName('edit')
  let deleteBtns = document.getElementsByClassName('delete')
  const csrfToken = getCookie('csrftoken')

  const matchDetailEndpoint = getApiDetailEndpoint();
  let playersEndUser = await getPlayersEndpointUsername(matchDetailEndpoint);

  for (let i in gameEndpoints) {
    let gameEndpoint = gameEndpoints[i];
    let editBtn = editBtns[i];
    let deleteBtn = deleteBtns[i];

    editBtn.addEventListener('click', function() {
      window.location = getFrontendURL(gameEndpoint)
    });
    deleteBtn.addEventListener('click', function() {
      fetch(gameEndpoint, {
        method: 'DELETE',
        headers: {
          'Content-type': 'application/json',
          'X-CSRFToken': csrfToken,
        }
      }).then(() => listGames(playersEndUser))
    })
  }
}