import {
  getJsonResponse,
  fillTitle,
  getCookie,
  setFormElemsAsDisabled,
  setFormElemsAsEnabled,
  getValFromUrl,
} from "./utils.js";
import { getMatchDetailEndpoint, 
         getPlayerListMatchEndpoint,
         getGameListMatchEndpoint,
         getScoreListMatchEndpoint,
         getOutcomeListMatchEndpoint,
         getFrontendURL,
} from './endpoints.js';
import { fillWinnerDropdown, submitGameForm } from "./game-form.js";

const csrfToken = getCookie('csrftoken');
const matchPk = getValFromUrl(window.location.pathname, 'matches');
fillMatchDetailPage();

/**
 * Main function for filling the match detail page.
 */
async function fillMatchDetailPage() {
  // Page constants
  const endpoints = getEndpoints(matchPk);
  let data = await getDataObj(endpoints);
  
  fillMatchDetailPageTitle(data.playerList);
  fillWinnerDropdown(
    data.playerList.results[0].username,
    data.playerList.results[1].username,
  );
  listGames(data.gameList.results);
  fillScoreboard(
    data.playerList.results,
    data.matchDetail,
    data.gameList.results,
    data.scoreList.results,
  );

  // If match is complete, gray out the game submit form
  let matchIsComplete = checkMatchOutcome(data.outcomeList);
  if (matchIsComplete) {
    setMatchAsComplete(data.outcomeList.results, data.playerList.results);
  } else {
    enableNewGameFormFields();
    setScoreboardCardTitleWithoutWinner();
    addGameFormSubmitEvent(matchPk);
  }
}

async function addGameFormSubmitEvent(matchPk) {
  let newGameForm = document.getElementById("new-game-form");
  newGameForm.removeEventListener('submit', submitGameFormHandler);
  newGameForm.addEventListener("submit", submitGameFormHandler);
}
/**
 * Return an object containing the API endpoints for match-detail, 
 * game-list-match, player-list-match, and score-list-match.
 */
function getEndpoints(matchPk) {
  return [
    getMatchDetailEndpoint(matchPk),
    getGameListMatchEndpoint(matchPk),
    getPlayerListMatchEndpoint(matchPk),
    getScoreListMatchEndpoint(matchPk),
    getOutcomeListMatchEndpoint(matchPk),
  ];
}
/**
 * Function to use in addEventListener. Named here so that we can remove 
 * the event listener before adding a new one.
 */
async function submitGameFormHandler(e) {
  await submitGameForm(e, 'POST', matchPk);

  // Reset form, including removing the event listener
  let newGameForm = document.getElementById('new-game-form');
  newGameForm.reset();
  document.getElementById('new-game-form').reset();

  // Refill the page (adds event listener back)
  fillMatchDetailPage();
}
/**
 * Return Promise object for the match, match's games, match's players,
 * and match's scores. `endpoints` is an object of key-value pairs: key is 
 * name of endpoint, value is endpoint URL.
 */
async function getDataJsons(endpoints) {
  let promises = []
  for (let endpoint of endpoints) {
    promises.push(getJsonResponse(endpoint));
  };
  return Promise.all(promises);
}
/**
 * Loop through JSONs produced by getDataJsons, assigning them as values 
 * to an object whose keys are the JSON types (matchDetail, gameList, 
 * playerList, scoreList).
 */
async function getDataObj(endpoints) {
  let dataVals = await getDataJsons(endpoints);
  let dataKeys = [
    'matchDetail',
    'gameList',
    'playerList',
    'scoreList',
    'outcomeList',
  ];
  let dataObj = {};
  for (let i = 0; i < dataVals.length; i++) {
    dataObj[dataKeys[i]] = dataVals[i];
  };
  return dataObj;
}
/**
 * Fill the match-detail page title.
 */
function fillMatchDetailPageTitle(playerListData) {
  let usernames = [];
  for (let data of playerListData.results) {
    usernames.push(data.username);
  }
  fillTitle(`Match - ${usernames[0]} v. ${usernames[1]}`);
}
/** Fill the `game-wrapper` element with a list of game details */
async function listGames(gamesJson) {
  let gamesHTML = await getGamesHTML(gamesJson);
  
  let gameWrapper = document.getElementById("game-table-body");
  gameWrapper.innerHTML = "";
  gamesHTML.forEach(addGameRowToPage);
  addEditDeleteButtons(gamesJson);
}
/**
 * Return an array of game table row HTML elements
 */
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
  const gamePk = getValFromUrl(gameJson.url, 'games');
  const winnerUrl = getFrontendURL(gameJson.winner);

  let datePlayed = new Date(gameJson.datetime_played).toDateString()
  let points = gameJson.points

  const check_circle_html = '<span class="material-symbols-outlined pt-1">check_circle</span>'
  let gin = gameJson.gin
  let ginCheck = gin ? check_circle_html : ""

  let undercut = gameJson.undercut
  let undercutCheck = undercut ? check_circle_html : ""

  let innerHTML = `
    <tr class="game-row" id="game-row-${gamePk}">
      <td>${datePlayed}</td>
      <td><a href="${winnerUrl}">#</a></td>
      <td>${points}</td>
      <td class="checkbox-cell">${ginCheck}</td>
      <td class="checkbox-cell">${undercutCheck}</td>
      <td class="button-cell"><button id="edit-button-${gamePk}" class="btn btn-small btn-outline-success edit">Edit</button></td>
      <td class="button-cell"><button id="delete-button-${gamePk}" class="btn btn-small btn-outline-secondary delete">Delete</button></td>
    </tr>
  `
  return innerHTML;
}

function addGameRowToPage(gameHTML) {
  let gameWrapper = document.getElementById('game-table-body');
  gameWrapper.innerHTML += gameHTML;
}

async function addEditDeleteButtons(gamesJson) {
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
    window.location = getFrontendURL(gameEndpoint) + 'edit/';
  });
}

async function addDeleteButton(deleteButtonElem, gameEndpoint) {
  deleteButtonElem.addEventListener('click', async function() {
    await fetch(gameEndpoint, {
      method: 'DELETE',
      headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': csrfToken,
      }
    })
    fillMatchDetailPage();
  })
}

function fillScoreboard(playersJson, matchJson, gamesJson, scoresJson) {
  const targetScore = matchJson.target_score;
  let scoreboardUsernameElems = document.getElementsByClassName('scoreboard-username');
  let scoreboardPointsElems = document.getElementsByClassName('scoreboard-points');
  let scoreboardWinsLossesElems = document.getElementsByClassName('scoreboard-wins-losses')
  
  countWinsAndLosses(playersJson, gamesJson);

  for (let i in playersJson) {
    
    let scoreJson = getScoreJson(playersJson[i], scoresJson)
    
    // Stats
    let points = scoreJson.player_score;
    let wins = playersJson[i].wins;
    let losses = playersJson[i].losses;
    
    fillScoreboardUsernames(scoreboardUsernameElems[i], playersJson[i]);
    fillScoreboardPoints(scoreboardPointsElems[i], points, targetScore);
    fillScoreboardWinsLosses(scoreboardWinsLossesElems[i], wins, losses);
  }
}

function fillScoreboardUsernames(scoreboardUsernameElem, playerJson) {
  scoreboardUsernameElem.innerHTML = playerJson.username;
}

function getScoreJson(playerJson, scoresJson) {
  return scoresJson.filter(function(score) {
    return score.player == playerJson.url;
  })[0]
}

function fillScoreboardPoints(scoreboardPointsElem, points, targetScore) {
  scoreboardPointsElem.innerHTML = `${points}<span style="font-size:.6em">/${targetScore}</span>`;
}

function fillScoreboardWinsLosses(scoreboardWinsLossesElem, wins, losses) {
  let winWord = null;
  let lossWord = null;

  if (wins == 1) {
    winWord = 'Win';
  } else {
    winWord = 'Wins';
  };
  if (losses == 1) {
    lossWord = 'Loss';
  } else {
    lossWord = 'Losses';
  };

  scoreboardWinsLossesElem.innerHTML = `(${wins} ${winWord}, ${losses} ${lossWord})`
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

function checkMatchOutcome(outcomeList) {
  return outcomeList.count > 0;
}

function disableNewGameFormFields() {
  const formElemNames = [
    'winner-dropdown',
    'points-input',
    'gin-input',
    'undercut-input',
    'new-game-submit',
  ];
  setFormElemsAsDisabled(formElemNames);
}
/**
 * Enable all new game form fields.
 */
function enableNewGameFormFields() {
  const formElemNames = [
    'winner-dropdown',
    'points-input',
    'gin-input',
    'undercut-input',
    'new-game-submit',
  ];
  setFormElemsAsEnabled(formElemNames);
}

function setMatchAsComplete(outcomeList, playerList) {
  disableNewGameFormFields();
  addWinnerToScoreboardCardTitle(outcomeList, playerList);
}

function getMatchWinnerEndpoint(outcomeList) {
  let winnerEndpoint = null
  for (let outcome of outcomeList) {
    if (outcome.player_outcome == 1) {
      winnerEndpoint = outcome.player;
      break;
    }
  }
  return winnerEndpoint;
}

function getMatchWinnerUsername(outcomeList, playerList) {
  let winnerEndpoint = getMatchWinnerEndpoint(outcomeList);
  let winnerJson = playerList.filter(function(playerJson) {
    return playerJson.url == winnerEndpoint;
  })[0];
  return winnerJson.username;
}

function addWinnerToScoreboardCardTitle(outcomeList, playerList) {
  let winnerUsername = getMatchWinnerUsername(outcomeList, playerList);
  const scoreboardTitle = `Scoreboard :: <span><b>${winnerUsername} Wins!</b></span>`;
  document.getElementById('scoreboard-card-title').innerHTML = scoreboardTitle;
}

function setScoreboardCardTitleWithoutWinner() {
  const scoreboardTitle = 'Scoreboard';
  document.getElementById('scoreboard-card-title').innerHTML = scoreboardTitle;
}
