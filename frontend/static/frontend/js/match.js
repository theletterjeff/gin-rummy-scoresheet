import { getJsonResponse, getJsonResponseArray, fillTitle, getCookie } from "./utils.js";
import { getApiDetailEndpoint, getPlayersEndpointUsername, getFrontendURL } from './endpoints.js';


import { fillWinnerDropdown, submitGameForm } from "./game-form.js";

// Page constants
const matchDetailEndpoint = getApiDetailEndpoint();
const playersEndUser = await getPlayersEndpointUsername(matchDetailEndpoint);
const csrfToken = getCookie('csrftoken');

// Data
const matchJson = await getJsonResponse(matchDetailEndpoint);
const gamesJson = await getJsonResponseArray(matchJson.games);
const playersJson = await getJsonResponseArray(matchJson.players);

fillMatchDetailPage();

/** Main execution function */
async function fillMatchDetailPage() {
  fillTitle('Match');
  
  fillWinnerDropdown(matchDetailEndpoint);
  listGames(playersEndUser);
  fillScores();

  let newGameForm = document.getElementById("new-game-form");
  newGameForm.addEventListener("submit", function(e) {
    submitGameForm(e, 'POST')
    .then(() => document.getElementById('new-game-form').reset())
    .then(() => listGames(playersEndUser))
  });
}

/** Fill the `game-wrapper` element with a list of game details */
async function listGames() {
  let gamesHTML = await getGamesHTML();

  let gameWrapper = document.getElementById("game-table-body");
  gameWrapper.innerHTML = "";
  gamesHTML.forEach(addGameRowToPage);
  addEditDeleteButtons(matchJson);
}

/* Return an array of game table row HTML elements */
async function getGamesHTML() {
  let gamesHTML = [];
  for (let gameJson of gamesJson) {
    // Get winner
    let winnerJson = playersJson.filter(function(playerJson) {
      return playerJson.url == gameJson.winner;
    });
    let winnerUsername = winnerJson[0].username
    
    // Make HTML
    let gameHTML = makeGameTableRow(gameJson);
    gameHTML = gameHTML.replace("#", winnerUsername)
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

async function addEditDeleteButtons() {
  let editBtns = document.getElementsByClassName('edit')
  let deleteBtns = document.getElementsByClassName('delete')

  for (let i in gamesJson) {
    let gameEndpoint = gamesJson[i].url;
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
      }).then(() => listGames())
    })
  }
}
