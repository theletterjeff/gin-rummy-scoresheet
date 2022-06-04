import {
  formatDate,
  getJsonResponse,
  getJsonResponseArray,
  fillTitle,
  getCookie,
} from "./utils.js";

const csrfToken = getCookie('csrftoken');

const matchesEndpoint = getMatchesEndpoint();
const loggedInPlayerEndpoint = getLoggedInPlayerEndpoint();

let currentMatchesTable = document.getElementById('current-matches-table');
let pastMatchesTable = document.getElementById('past-matches-table');

fillPlayerMatchesPage();

async function fillPlayerMatchesPage() {
  const loggedInPlayerData = await getLoggedInPlayerData();
  let matchesData = await getMatchesData();
  fillCurrentAndPastMatchesTables(matchesData, loggedInPlayerData);
}

function fillCurrentAndPastMatchesTables(matchesData, loggedInPlayerData) {
  let fillRowPromise = new Promise((resolve) => {
    matchesData.map((match) => {
      if (match.complete == false) {
        addMatchToCurrentMatches(match, loggedInPlayerData);
      } else {
        addMatchToPastMatches(match);
      };
    });
    resolve();
  })
  fillRowPromise
  .then(addEditMatchButtons)
  .then(addDeleteMatchButtons);
  // let x = Promise.all(
  //   matchesData.map((match) => {
  //     return new Promise((resolve) => {
  //       if (match.complete == false) {
  //         addMatchToCurrentMatches(match, loggedInPlayerData);
  //       } else {
  //         addMatchToPastMatches(match);
  //       };
  //       resolve();
  //     })
  //   })
  // )

  // x
  // .then(() => console.log(document.getElementsByClassName('edit-match')))
  // .then(() => addEditMatchButtons())
  // .then(() => addDeleteMatchButtons());
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
  let matchPk = getMatchPkFromURL(match.url)
  let scoresObj = await getScoresObj(match.score_set);
  let scoresFormatted = formatScoresFromObj(scoresObj, loggedInPlayerData);
  let opponentUsername = await getOpponentUsername(match, loggedInPlayerData);
  let dateFormatted = formatDate(match.datetime_started)

  let matchHTML = `
    <tr id="row-match-${matchPk}">
      <td>${dateFormatted}</td>
      <td>${opponentUsername}</td>
      <td>${scoresFormatted}</td>
      <td class="button-cell"><button class="btn btn-small btn-outline-success edit-match" id="edit-match-${matchPk}">Edit</button></td>
      <td class="button-cell"><button class="btn btn-small btn-outline-secondary delete-match" id="delete-match-${matchPk}">Delete</button></td>
    </tr>
  `
  currentMatchesTable.innerHTML += matchHTML;
}

function getMatchPkFromURL(matchURL) {
  const re = new RegExp('\\d+(?=\/$)')
  return re.exec(matchURL);
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

function addEditMatchButtons() {
  let editBtns = document.getElementsByClassName('edit-match')
  console.log(editBtns);
  const re = new RegExp('\\d+');

  for (let btn of editBtns) {
    let matchPk = re.exec(btn.id);
    btn.addEventListener('click', function() {
      window.location = window.location.href + matchPk;
    })
  }
}

async function addDeleteMatchButtons() {
  let deleteBtns = document.getElementsByClassName('delete-match')
  const re = new RegExp('\\d+');

  for (let btn of deleteBtns) {
    let matchPk = re.exec(btn.id);
    btn.addEventListener('click', function() {
      let deleteMatchEndpoint = window.location.origin + '/api/match/' + matchPk;
      fetch(deleteMatchEndpoint, {
        method: 'DELETE',
        headers: {
          'Content-type': 'application/json',
          'X-CSRFToken': csrfToken,
        }
      })
      .then(() => deleteMatchFromTable(`row-match-${matchPk}`));
    })
  }
}

function deleteMatchFromTable(matchElemID) {
  let matchElem = document.getElementById(matchElemID);
  matchElem.remove();
}