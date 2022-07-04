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
  return getJsonResponse(loggedInPlayerEndpoint);
}

function addMatchToCurrentMatches(match, loggedInPlayerData) {
  match.loggedInPlayer = loggedInPlayerData;
  addPkToMatch(match)
    .then(addScoresObjToMatch)
    .then(formatScoresFromObj)
    .then(addOpponentUsernameToMatch)
    .then(addFormattedDateToMatch)
    .then(addHTMLRowToCurrentMatchesTable)
    .then(addEditMatchButton)
    .then(addDeleteMatchButton)
}

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
  return match;
}

async function addOpponentUsernameToMatch(match) {
  match.opponent = {};
  for (let playerEndpoint of match.players) {
    if (playerEndpoint != match.loggedInPlayer.url) {
      match.opponent.url = playerEndpoint;
    }
  }
  return getJsonResponse(match.opponent.url)
    .then((playerData) => {
      match.opponent.username = playerData.username;
      return match;
    })
}

function addFormattedDateToMatch(match) {
  match.datetime_started_formatted = formatDate(match.datetime_started);
  return match;
}

function addHTMLRowToCurrentMatchesTable(match) {
  let currentMatchesTable = document.getElementById('current-matches-table');
  let matchHTML = `
      <tr id="row-match-${match.pk}">
        <td>${match.datetime_started_formatted}</td>
        <td>${match.opponent.username}</td>
        <td>${match.formattedScores}</td>
        <td class="button-cell"><button class="btn btn-small btn-outline-success edit-match" id="edit-match-${match.pk}">Edit</button></td>
        <td class="button-cell"><button class="btn btn-small btn-outline-secondary delete-match" id="delete-match-${match.pk}">Delete</button></td>
      </tr>
    `
    currentMatchesTable.innerHTML += matchHTML;
    return match;
}

function addEditMatchButton(match) {
  let editBtn = document.getElementById(`edit-match-${match.pk}`)
  editBtn.addEventListener('click', function() {
    window.location = window.location.href + match.pk;
  });
  return match;
} 

async function addDeleteMatchButton(match) {
  let deleteBtn = document.getElementById(`delete-match-${match.pk}`)

  deleteBtn.addEventListener('click', function() {
    let deleteMatchEndpoint = window.location.origin + '/api/match/' + match.pk;
    fetch(deleteMatchEndpoint, {
      method: 'DELETE',
      headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': csrfToken,
      }
      .then(() => deleteMatchFromTable(`row-match-${match.pk}`))
    })
  })
  return match;
}

function deleteMatchFromTable(matchElemID) {
  let matchElem = document.getElementById(matchElemID);
  matchElem.remove();
}