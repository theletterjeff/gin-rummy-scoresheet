import {
  formatDate,
  getJsonResponse,
  getJsonResponseArray,
  fillTitle,
  getCookie,
} from "./utils.js";

const matchesEndpoint = getMatchesEndpoint();
const loggedInPlayerEndpoint = getLoggedInPlayerEndpoint();

let currentMatchesTable = document.getElementById('current-matches-table');
let pastMatchesTable = document.getElementById('past-matches-table');

fillPlayerMatchesPage();

async function fillPlayerMatchesPage() {
  const loggedInPlayerData = await getLoggedInPlayerData();
  let matchesData = await getMatchesData();
  for (let match of matchesData) {
    if (match.complete == false) {
      addMatchToCurrentMatches(match, loggedInPlayerData);
    } else {
      addMatchToPastMatches(match);
    }
  }
}

function getMatchesEndpoint() {
  return window.location.origin + '/api/player-matches/';
}

function getLoggedInPlayerEndpoint() {
  return window.location.origin + '/api/logged-in-player/';
}

async function getMatchesData() {
  return getJsonResponse(matchesEndpoint);
}

async function getLoggedInPlayerData() {
  return await getJsonResponse(loggedInPlayerEndpoint);
}

async function addMatchToCurrentMatches(match, loggedInPlayerData) {
  let scoresObj = await getScoresObj(match.score_set);
  let scoresFormatted = formatScoresFromObj(scoresObj, loggedInPlayerData);
  let opponentUsername = await getOpponentUsername(match, loggedInPlayerData);
  let dateFormatted = formatDate(match.datetime_started)
  let matchHTML = `
    <tr>
      <td>${dateFormatted}</td>
      <td>${opponentUsername}</td>
      <td>${scoresFormatted}</td>
      <td class="button-cell"><button class="btn btn-small btn-outline-success edit">Edit</button></td>
      <td class="button-cell"><button class="btn btn-small btn-outline-secondary delete">Delete</button></td>
    </tr>
  `
  currentMatchesTable.innerHTML += matchHTML;
}

async function getScoresObj(scoreEndpointsArray) {
  let scoresObj = {};
  for (let scoreEndpoint of scoreEndpointsArray) {
    let scoreObj = await getJsonResponse(scoreEndpoint);
    scoresObj[scoreObj.player] = scoreObj.player_score;
  }
  return scoresObj;
}

function formatScoresFromObj(scoresObj, loggedInPlayerData) {
  let formattedScoresArray = []
  
  for (let playerEndpoint in scoresObj) {
    if (playerEndpoint == loggedInPlayerData.url) {
      formattedScoresArray[0] = scoresObj[playerEndpoint];
    } else {
      formattedScoresArray[1] = scoresObj[playerEndpoint];
    }
  };
  return `${formattedScoresArray[0]}-${formattedScoresArray[1]}`
}

async function getPlayerUsername(playerEndpoint) {
  let playerData = await getJsonResponse(playerEndpoint)
  return playerData.username;
}

async function getOpponentUsername(matchData, loggedInPlayerData) {
  for (let playerEndpoint of matchData.players) {
    let playerUsername = await getPlayerUsername(playerEndpoint)
    if (playerUsername == loggedInPlayerData.username) {
      continue;
    } else {
      return playerUsername;
    };
  }
}