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
  let fillRowPromises = [];
  for (let matchData of matchesData) {
    let fillRowPromise = fillRow(matchData, loggedInPlayerData);
    fillRowPromises.push(fillRowPromise);
  };
  Promise.all(fillRowPromises)
    .then(addEditMatchButtons)
    .then(addDeleteMatchButtons);
}

function fillRow(match, loggedInPlayerData) {
  return new Promise((resolve, reject) => {
    if (!match.complete) {
      addMatchToCurrentMatches(match, loggedInPlayerData);
    } else {
      addMatchToPastMatches(match, loggedInPlayerData);
    };
    resolve();
  });
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

function addMatchToCurrentMatches(match, loggedInPlayerData) {
  match.loggedInPlayer = loggedInPlayerData;
  addPkToMatch(match)
    .then(addScoresObjToMatch)
    .then(formatScoresFromObj)
    .then(() => console.log(match))
    // .then(match => {console.log(match)})
}

//   let currentMatchObj = new Promise((resolve, reject) => {
//     let matchPk = getMatchPkFromURL(match.url);
//     let scoresObj = await getScoresObj(match.score_set);
//     let scoresFormatted = formatScoresFromObj(scoresObj, loggedInPlayerData);
//     let opponentUsername = await getOpponentUsername(match, loggedInPlayerData);
//     let dateFormatted = formatDate(match.datetime_started);
//     resolve({
//       matchPk: matchPk,
//       scoresObj: scoresObj,
//       scoresFormatted: scoresFormatted,
//       opponentUsername: opponentUsername,
//       dateFormatted: dateFormatted,
//     })
//   })
//   console.log(currentMatchObj);

//   currentMatchObj.then((data) => {
//     let matchHTML = `
//       <tr id="row-match-${data.matchPk}">
//         <td>${data.dateFormatted}</td>
//         <td>${data.opponentUsername}</td>
//         <td>${data.scoresFormatted}</td>
//         <td class="button-cell"><button class="btn btn-small btn-outline-success edit-match" id="edit-match-${data.matchPk}">Edit</button></td>
//         <td class="button-cell"><button class="btn btn-small btn-outline-secondary delete-match" id="delete-match-${data.matchPk}">Delete</button></td>
//       </tr>
//     `
//     currentMatchesTable.innerHTML += matchHTML;
//   })
// }

function addPkToMatch(match) {
  const re = new RegExp('\\d+(?=\/$)')
  return new Promise((resolve) => {
    match.pk = re.exec(match.url);
    resolve(match);
  })
}

function addScoresObjToMatch(match) {
  let promises = [];
  for (let scoreEndpoint of match.score_set) {
    promises.push(getJsonResponse(scoreEndpoint));
  };
  return Promise.all(promises)
    .then((scoreData) => {
      for (let i in scoreData) {
        match.score_set[i] = scoreData[i];
        }
      return match;
      });
}

function formatScoresFromObj(match) {
  let formattedScoresArray = [];
  for (let scoreObj of match.score_set) {
    if (scoreObj.player == match.loggedInPlayer.url) {
      formattedScoresArray[0] = scoreObj.player_score;
    } else {
      formattedScoresArray[1] = scoreObj.player_score;
    };
  match.formattedScores =  `${formattedScoresArray[0]}-${formattedScoresArray[1]}`
  }
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