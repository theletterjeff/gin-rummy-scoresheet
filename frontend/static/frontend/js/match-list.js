import {
  formatDate,
  formatDateRange,
  getJsonResponse,
  getCookie,
  getRequestPlayerUsername,
  getValFromUrl,
  setElemAsHidden,
  setFormElemsAsDisabled,
  waitForElem,
} from "./utils.js";
import {
  getFrontendURL,
  getMatchCreateEndpoint,
  getMatchDetailEndpoint,
  getMatchListPlayerEndpoint, 
  getPlayerDetailEndpoint,
  getPlayersListAllEndpoint,
  getRequestPlayerEndpoint,
} from "./endpoints.js";

const defaultTargetScore = 500
fillPlayerMatchesPage();

async function fillPlayerMatchesPage() {
  
  const csrfToken = getCookie('csrftoken');
  const username = getValFromUrl(window.location.pathname, 'players');
  const requestPlayer = await getJsonResponse(getRequestPlayerEndpoint());

  // Endpoints
  const matchListEndpoint = getMatchListPlayerEndpoint(username);

  // JSON data
  let matchesData = await getJsonResponse(matchListEndpoint);
  matchesData = matchesData.results;
  
  addDataToMatches(matchesData)
  .then(function(matchesData) {
    fillMatchesTables(matchesData, csrfToken)
  })
  
  if (requestPlayer.username != username) {
    disableNewMatchFormFields();
    setElemAsHidden('new-match-card');
  } else {
    fillNewMatchForm();
  };
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
  }
  const matchesPromise = matchesData.map(async function(matchData) {
    const requestPlayerUsername = await getRequestPlayerUsername();
    if (matchData.viewPlayer.username == requestPlayerUsername) {
      await addDeleteMatchButton(matchData.pk, csrfToken);
    };
  });
  Promise.all(matchesPromise);
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
      const playerOutcome = await getJsonResponse(playerOutcomeEndpoint);
      // See if it's the request user
      let playerUsername = getValFromUrl(playerOutcomeEndpoint, 'players');
      if (playerUsername == match.viewPlayer.username) {
        match.formattedOutcome = outcomeTable[playerOutcome.player_outcome];
      };
    };
  }
  return match;
}

function addHTMLRowToCurrentMatchesTable(matchData, currentMatchesTable) {
  const matchDetailUrl = getFrontendURL(matchData.url);
  const opponentDetailUrl = getFrontendURL(matchData.opponent.url);
  let matchHTML = `
      <tr id="row-match-${matchData.pk}" class="row-current-match">
        <td><a href="${matchDetailUrl}">${matchData.datetime_started_formatted}</a></td>
        <td><a href="${opponentDetailUrl}">${matchData.opponent.username}</a></td>
        <td>${matchData.formattedScores}</td>
        <td>${matchData.target_score}</td>
      </tr>
    `
    currentMatchesTable.innerHTML += matchHTML;
}

function addHTMLRowToPastMatchesTable(matchData, pastMatchesTable) {
  const matchDetailUrl = getFrontendURL(matchData.url);
  const opponentDetailUrl = getFrontendURL(matchData.opponent.url);
  let matchHTML = `
      <tr id="row-match-${matchData.pk}" class="row-past-match">
        <td id="past-match-datetime-${matchData.pk}"><a href="${matchDetailUrl}">${matchData.datetime_range_formatted}</a></td>
        <td id="past-match-opponent-username"><a href="${opponentDetailUrl}">${matchData.opponent.username}</a></td>
        <td id="past-match-outcome-${matchData.pk}">${matchData.formattedOutcome}</td>
        <td id="past-match-scores-${matchData.pk}">${matchData.formattedScores}</td>
    `
    pastMatchesTable.innerHTML += matchHTML;
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
  deleteBtn.addEventListener('click', function(e) {
    e.preventDefault();
    let deleteMatchEndpoint = window.location.origin + `/api/matches/${matchPk}/`;
    fetch(deleteMatchEndpoint, {
      method: 'DELETE',
      headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': csrfToken,
      }
    })
    .then(() => deleteElem(matchRow));
  })
}
/**
 * Delete an element from the page.
 */
function deleteElem(matchRow) {
  matchRow.remove();
}
/**
 * Fill the New Match form's opponent box and add a submit event to the button.
 */
async function fillNewMatchForm() {
  const requestPlayer = await getJsonResponse(getRequestPlayerEndpoint());
  fillOpponentDropdown(requestPlayer);
  fillDefaultTargetScore();
  addSubmitEventListener(requestPlayer);
}
/**
 * Fill the opponent dropdown in the new match card with the names of all 
 * the players except for the request user.
 */
async function fillOpponentDropdown(requestPlayer) {
  const playersEndpoint = getPlayersListAllEndpoint();
  const playersData = await getJsonResponse(playersEndpoint);

  let playersDropdown = document.getElementById('opponent-dropdown');
  for (let player of playersData.results) {
    if (player.username != requestPlayer.username) {
      let dropdownOption = `<option class="opponent-option" value=${player.url}>${player.username}</option>`;
      playersDropdown.innerHTML += dropdownOption;
    };
  };
}
/**
 * Fill the target-score-input element with the default score for matches (500).
 * TODO: move away from hard-coded default, ping server for what default is set to.
 */
function fillDefaultTargetScore() {
  let targetScoreInput = document.getElementById('target-score-input');
  targetScoreInput.value = defaultTargetScore
}
/**
 * Add a click event on the `submit` button that posts a new Match.
 */
function addSubmitEventListener(requestPlayer) {
  let newMatchForm = document.getElementById('new-match-form');
  newMatchForm.addEventListener('submit', function(e) {
    e.preventDefault();
    submitNewMatch(requestPlayer)
    .then((resp) => resp.json())
    .then((data) => window.location.replace(getFrontendURL(data.url)));
  });
}

function submitNewMatch(requestPlayer) {
  const matchCreateEndpoint = getMatchCreateEndpoint()
  const csrfToken = getCookie('csrftoken');

  const requestPlayerEndpoint = requestPlayer.url;
  const opponentEndpoint = document.getElementById('opponent-dropdown').value;
  const targetScore = document.getElementById('target-score-input').value;

  const body = {
    'players': [requestPlayerEndpoint, opponentEndpoint],
    'target_score': targetScore,
  };

  return fetch(matchCreateEndpoint, {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify(body),
  });
}

function disableNewMatchFormFields() {
  const formElems = [
    'opponent-dropdown',
    'target-score-input',
    'new-match-submit',
  ];
  setFormElemsAsDisabled(formElems);
}