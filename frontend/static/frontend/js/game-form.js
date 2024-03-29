import { getDetailEndpointFromEditURL,
         getPlayersUsernameEndpoint,
         getGameCreateEndpoint,
         getMatchDetailEndpoint,
         getPlayerDetailEndpoint,
       } from "./endpoints.js";
import { getCookie } from './utils.js';

/**
 * Fill the 'winner' dropdown with players' usernames. winnerUsername
 */
export function fillWinnerDropdown(player0Username, player1Username) {
  let dropdownOptions = `
    <option select id="player0-username-option" value=${player0Username}>${player0Username}</option>
    <option id="player1-username-option" value=${player1Username}>${player1Username}</option>
  `
  let winnerDropdown = document.getElementById('winner-dropdown');
  winnerDropdown.innerHTML = dropdownOptions;
}

/**
 * Fill the points field with game's current points.
 */
export function fillPoints(elementId, points) {
  let pointsInput = document.getElementById(elementId);
  pointsInput.value = points;
}

/**
 * Fill the checkboxes with a bool value. Used for gin-input and undercut-input.
 */
export function fillCheckbox(elementId, boolVal) {
  let checkboxElem = document.getElementById(elementId);
  checkboxElem.checked = boolVal;
}

/**
 * Submit the Game form (either as a new Game or as an edit on an existing Game).
 */
export async function submitGameForm(e, method, matchPk) {
  e.preventDefault();
  
  const csrfToken = getCookie("csrftoken");
  
  let gameEndpoint = null
  if (method == 'POST') {
    gameEndpoint = getGameCreateEndpoint(matchPk);
  } else {
    gameEndpoint = getDetailEndpointFromEditURL();
  }
  // Form fields
  let matchDetailEndpoint = getMatchDetailEndpoint(matchPk);
  
  let playersUserEnd = await getPlayersUsernameEndpoint(matchDetailEndpoint);

  let winnerUsername = document.getElementById('winner-dropdown').value;
  let winnerEndpoint = getPlayerDetailEndpoint(winnerUsername);
  
  // Delete winner from `players`, leaving only the loser
  delete playersUserEnd[winnerUsername]
  let loserEndpoint = Object.values(playersUserEnd)[0]
  
  let points = document.getElementById('points-input').value;
  let gin = document.getElementById('gin-input').checked;
  let undercut = document.getElementById('undercut-input').checked;

  return fetch(gameEndpoint, {
    method: method,
    headers: {
      'Content-type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({
      'match': matchDetailEndpoint,
      'winner': winnerEndpoint,
      'loser': loserEndpoint,
      'points': points,
      'gin': gin,
      'undercut': undercut,
    }),
  })
}
