import {
  getJsonResponse,
  getJsonResponseArray,
  fillTitle,
  getCookie,
  setFormElemAsDisabled,
  getValFromUrl,
} from "./utils.js";
import { getApiEndpointFromUrl, getFrontendURL } from './endpoints.js';
import { fillWinnerDropdown, submitGameForm } from "./game-form.js";

fillMatchDetailPage();

/**
 * Main function for filling the match detail page.
 */
async function fillMatchDetailPage() {
  // Page constants
  const matchDetailEndpoint = getApiEndpointFromUrl();
  const gameListDetailEndpoint = matchDetailEndpoint + 'games/'

  // Data
  let matchJson = await getJsonResponse(matchDetailEndpoint);
  let gamesJson = await getJsonResponse(gameListDetailEndpoint);
  let playersJson = await getJsonResponseArray(matchJson.players);
  let scoresJson = await getJsonResponseArray(matchJson.score_set);

  fillTitle(`Match - ${playersJson[0].username} v. ${playersJson[1].username}`);
  
  fillWinnerDropdown(playersJson[0].username, playersJson[1].username);
  listGames();
  fillScoreboard(playersJson, gamesJson);
  
  let matchOutcome = checkMatchOutcome();
  if (matchOutcome) {
    setMatchAsComplete();
  }

  let newGameForm = document.getElementById("new-game-form");
  newGameForm.addEventListener("submit", function(e) {
    submitGameForm(e, 'POST')
    .then(() => document.getElementById('new-game-form').reset())
    .then(() => updateMatchJsons())
    .then(() => listGames())
    .then(function() {
      let gamesJson = await getJsonResponse(gameListDetailEndpoint);
      let playersJson = await getJsonResponseArray(matchJson.players);
      fillScoreboard(playersJson, gamesJson))
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

async function updateMatchJsons() {
  matchJson = await getJsonResponse(matchDetailEndpoint);
  gamesJson = await getJsonResponseArray(matchJson.games);
  playersJson = await getJsonResponseArray(matchJson.players);
  scoresJson = await getJsonResponseArray(matchJson.score_set);
}

/* Return an array of game table row HTML elements */
async function getGamesHTML(gamesJson) {
  let gamesHTML = [];
  for (let gameJson of gamesJson) {
    let gameHTML = makeGameTableRow(gameJson);
    let winnerUsername = getValFromUrl(gameJson.winner, 'players');
    gameHTML = gameHTML.replace("#", winnerUsername);
    gamesHTML.push(gameHTML);
  }
  return gamesHTML;
}

function makeGameTableRow(gameJson) {
  let winnerEndpoint = gameJson.winner

  let datePlayed = new Date(gameJson.datetime_played).toDateString()
  let points = gameJson.points

  const check_circle_html = '<span class="material-symbols-outlined pt-1">check_circle</span>'
  let gin = gameJson.gin
  let ginCheck = gin ? check_circle_html : ""

  let undercut = gameJson.undercut
  let undercutCheck = undercut ? check_circle_html : ""

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

    addEditButton(editBtn, gameEndpoint);
    addDeleteButton(deleteBtn, gameEndpoint);
  }
}

function addEditButton(editButtonElem, gameEndpoint) {
  editButtonElem.addEventListener('click', function() {
    window.location = getFrontendURL(gameEndpoint)
  });
}

async function addDeleteButton(deleteButtonElem, gameEndpoint) {
  deleteButtonElem.addEventListener('click', function() {
    fetch(gameEndpoint, {
      method: 'DELETE',
      headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': csrfToken,
      }
    })
    .then(() => updateMatchJsons())
    .then(() => listGames())
    .then(() => fillScoreboard())
  })
}

function fillScoreboard(playersJson, gamesJson) {
  let scoreboardUsernameElems = document.getElementsByClassName('scoreboard-username');
  let scoreboardPointsElems = document.getElementsByClassName('scoreboard-points');
  let scoreboardWinsLossesElems = document.getElementsByClassName('scoreboard-wins-losses')
  
  countWinsAndLosses(playersJson, gamesJson);

  for (let i in playersJson) {
    
    let scoreJson = getScoreJson(playersJson[i])
    
    // Stats
    let points = scoreJson.player_score;
    let wins = playersJson[i].wins;
    let losses = playersJson[i].losses;
    
    fillScoreboardUsernames(scoreboardUsernameElems[i], playersJson[i]);
    fillScoreboardPoints(scoreboardPointsElems[i], points);
    fillScoreboardWinsLosses(scoreboardWinsLossesElems[i], wins, losses);
  }
}

function fillScoreboardUsernames(scoreboardUsernameElem, playerJson) {
  scoreboardUsernameElem.innerHTML = playerJson.username;
}

function getScoreJson(playerJson) {
  return scoresJson.filter(function(score) {
    return score.player == playerJson.url;
  })[0]
}

function fillScoreboardPoints(scoreboardPointsElem, points) {
  scoreboardPointsElem.innerHTML = points;
}

function fillScoreboardWinsLosses(scoreboardWinsLossesElem, wins, losses) {
  scoreboardWinsLossesElem.innerHTML = `(${wins} Wins, ${losses} losses)`
}

function countWinsAndLosses(playersJson, gamesJson) {
  for (let playerJson of playersJson) {
    playerJson.wins = 0;
    playerJson.losses = 0;
  };
  for (let gameJson of gamesJson) {
    let winner = playersJson.filter(function(playerJson) {
      return playerJson.url == gameJson.winner;
    })[0];
    let loser = playersJson.filter(function(playerJson) {
      return playerJson.url == gameJson.loser;
    })[0];
    winner.wins += 1;
    loser.losses += 1;
  }
}

function checkMatchOutcome() {
  return matchJson.outcome_set.length > 0;
}

function disableNewGameFormFields() {
  const formElemNames = [
    'winner-dropdown',
    'points-input',
    'gin-input',
    'undercut-input',
    'new-game-submit',
  ];
  for (let formElemName of formElemNames) {
    setFormElemAsDisabled(formElemName);
  }
}

function setMatchAsComplete() {
  disableNewGameFormFields();
  addWinnerToScoreboardCardTitle();
}

function getMatchWinnerEndpoint() {
  let outcomeArray = matchJson.outcome_set;
  let winnerEndpoint = null
  for (outcomeEndpoint of outcomeArray) {
    let outcomeJson = getJsonResponse(outcomeEndpoint);
    if (outcomeJson.player_outcome == 1) {
      winnerEndpoint = outcomeJson.player;
      break;
    }
  }
  return winnerEndpoint;
}

function getMatchWinnerUsername() {
  let winnerEndpoint = getMatchWinnerEndpoint();
  let winnerJson = playerJson.filter(function(playerJson) {
    return playerJson.url == winnerEndpoint;
  })[0];
  return winnerJson.username;
}

function addWinnerToScoreboardCardTitle() {
  let winnerUsername = getMatchWinnerUsername();
  document.getElementById('scoreboard-card-title').innerHTML = `Scoreboard :: <span><b>${winnerUsername} Wins!</b></span>`
}