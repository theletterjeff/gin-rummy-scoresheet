import {
  formatDate,
  formatDateRange,
  getJsonResponse,
  getCookie,
  getRequestPlayerUsername,
  getValFromUrl,
  waitForElem,
} from "./utils.js";
import { getApiEndpointFromUrl, getPlayerDetailEndpoint } from "./endpoints.js";

fillPlayerMatchesPage();

async function fillPlayerMatchesPage() {
  
  const csrfToken = getCookie('csrftoken');
  const username = getValFromUrl(window.location.pathname, 'players');

  // Endpoints
  const matchListEndpoint = window.location.origin + `/api/matches/${username}/`;

  // JSON data
  let matchesData = await getJsonResponse(matchListEndpoint);
  matchesData = matchesData.results;
  
  addDataToMatches(matchesData)
  .then(function(matchesData) {
    fillMatchesTables(matchesData, csrfToken)
  });
}
/**
 * Loop through all matches, applying `addDataToMatch` function to each. Return 
 * matchesData array with added data included.
 */
async function addDataToMatches(matchesData) {
  for (let matchData of matchesData) {
    matchData = await addDataToMatch(matchData);
  };
  return matchesData;
}
/**
 * Add key datapoints to match object:
 * - match PK
 * - formatted scores
 * - opponent username
 * - formatted dates
 * - formatted outcomes (if complete)
 */
async function addDataToMatch(matchData) {
  matchData = await addViewPlayerToMatch(matchData)
  .then(addPkToMatch)
  .then(addScoresObjToMatch)
  .then(formatScoresFromObj)
  .then(addOpponentToMatch)
  .then(addFormattedDatesToMatch)
  .then(function(matchData) {
    if (matchData.complete) {
      return addFormattedOutcomeToMatch(matchData);
    };
  })
  return matchData;
}

/**
 * Add each match to either the current matches or the past matches table.
 */
async function fillMatchesTables(matchesData, csrfToken) {
  let currentMatchesTable = await waitForElem('current-matches-table');
  let pastMatchesTable = await waitForElem('past-matches-table');
  
  for (let matchData of matchesData) {
    if (matchData.complete) {
      addHTMLRowToPastMatchesTable(matchData, pastMatchesTable);
    } else {
      addHTMLRowToCurrentMatchesTable(matchData, currentMatchesTable);
    }

    // Add buttons if current match-list view is for request player (user)
    const requestPlayerUsername = await getRequestPlayerUsername();
    if (matchData.viewPlayer.username == requestPlayerUsername) {
      addEditMatchButton(matchData.pk);
      addDeleteMatchButton(matchData.pk, csrfToken);
    }
  }
}
/**
 * Add view player's username (player in URL) to match object.
 */
async function addViewPlayerToMatch(matchData) {
  const viewPlayerUsername = getValFromUrl(window.location.href, 'players');
  const viewPlayerEndpoint = getPlayerDetailEndpoint(viewPlayerUsername)
  matchData.viewPlayer = await getJsonResponse(viewPlayerEndpoint);
  return matchData;
}
/**
 * Add match's ID (PK) to the match object.
 */
function addPkToMatch(match) {
  const re = new RegExp('\\d+(?=\/$)')
  return new Promise((resolve) => {
    match.pk = re.exec(match.url);
    resolve(match);
  })
}
/**
 * Add data from GET requests to the match's `.scores` endpoints to the 
 * match object.
 */
async function addScoresObjToMatch(match) {
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
/**
 * Given two scores objects (nested within the match object), return a 
 * string that is formatted as 'score-score' (e.g., '25-10').
 */
function formatScoresFromObj(match) {
  let formattedScoresArray = [];
  for (let scoreObj of match.score_set) {
    if (scoreObj.player == match.viewPlayer.url) {
      formattedScoresArray[0] = scoreObj.player_score;
    } else {
      formattedScoresArray[1] = scoreObj.player_score;
    };
  match.formattedScores =  `${formattedScoresArray[0]}-${formattedScoresArray[1]}`
  }
  return match;
}
/**
 * Check if each player in the match's `.players` set is equal to the 
 * player whose username was passed in the URL (`match.viewPlayer`). If not, 
 * set that player as the opponent.
 */
async function addOpponentToMatch(match) {
  for (let playerEndpoint of match.players) {
    if (playerEndpoint != match.viewPlayer.url) {
      match.opponent = await getJsonResponse(playerEndpoint);
    };
  };
  return match;
}
/**
 * If the match has ended, add `.datetime_range_formatted` to the match object. 
 * If not, add a `.datetime_started_formatted` to the match object.
 * 
 * Format specified in formatDate function.
 */
function addFormattedDatesToMatch(match) {
  if (match.datetime_ended) {
    // Match is complete
    match.datetime_range_formatted = formatDateRange(
      match.datetime_started, match.datetime_ended);
  } else {
    // Match is not complete
    match.datetime_started_formatted = formatDate(match.datetime_started);
  };
  return match;
}
/**
 * Add `.formattedOutcome` to the match object. The value will either be 'W' 
 * or 'L'.
 */
async function addFormattedOutcomeToMatch(match) {
  const outcomeTable = {
    0: 'L',
    1: 'W',
  }
  if (match.complete) {
    for (let playerOutcomeEndpoint of match.outcome_set) {
      let playerUsername = getValFromUrl(playerOutcomeEndpoint, 'players');
      if (playerUsername == match.viewPlayer.username) {
        match.formattedOutcome = outcomeTable[playerOutcome.player_outcome];
      };
    };
  }
  return match;
}

function addHTMLRowToCurrentMatchesTable(matchData, currentMatchesTable) {
  let matchHTML = `
      <tr id="row-match-${matchData.pk}" class="row-current-match">
        <td>${matchData.datetime_started_formatted}</td>
        <td>${matchData.opponent.username}</td>
        <td>${matchData.formattedScores}</td>
      </tr>
    `
    currentMatchesTable.innerHTML += matchHTML;
}

function addHTMLRowToPastMatchesTable(matchData, pastMatchesTable) {
  let matchHTML = `
      <tr id="row-match-${matchData.pk}" class="row-past-match">
        <td id="past-match-datetime-${matchData.pk}">${matchData.datetime_range_formatted}</td>
        <td id="past-match-opponent-username-${matchData.pk}">${matchData.opponent.username}</td>
        <td id="past-match-outcome-${matchData.pk}">${matchData.formattedOutcome}</td>
        <td id="past-match-scores-${matchData.pk}">${matchData.formattedScores}</td>
    `
    pastMatchesTable.innerHTML += matchHTML;
}
/**
 * Add an 'Edit' button to a match row.
 */
async function addEditMatchButton(matchPk) {
  // Add HTML
  let matchRow = document.getElementById(`row-match-${matchPk}`)
  const editButtonHTML = `<td class="button-cell"><button class="btn btn-small btn-outline-success edit-match" id="edit-match-${matchPk}">Edit</button></td>`
  matchRow.innerHTML += editButtonHTML;

  // Add click event
  let editBtn = await waitForElem(`edit-match-${matchPk}`)
  editBtn.addEventListener('click', function() {
    window.location = window.location.origin + `/matches/${matchPk}/`
  });
} 
/**
 * Add a 'Delete' button to a match row.
 */
async function addDeleteMatchButton(matchPk, csrfToken) {
  // Add HTML
  let matchRow = document.getElementById(`row-match-${matchPk}`)
  const deleteButtonHTML = `<td class="button-cell"><button class="btn btn-small btn-outline-secondary delete-match" id="delete-match-${matchPk}">Delete</button></td>`
  matchRow.innerHTML += deleteButtonHTML;

  // Add click event
  let deleteBtn = await waitForElem(`delete-match-${matchPk}`)
  deleteBtn.addEventListener('click', function() {
    let deleteMatchEndpoint = window.location.origin + `/api/matches/${matchPk}/`;
    fetch(deleteMatchEndpoint, {
      method: 'DELETE',
      headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': csrfToken,
      }
    })
    .then(() => deleteElem(deleteBtn));
  })
}
/**
 * Delete an element from the page.
 */
function deleteElem(matchElem) {
  matchElem.remove();
}
