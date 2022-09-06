import {
  getApiDetailEndpoint,
  getPlayersUsernameEndpoint,
  getPlayersEndpointUsername,
  getGameListCreateEndpoint
} from "./endpoints.js";
import { getCookie, getJsonResponse } from './utils.js';

export async function submitGameForm(e, method) {
  e.preventDefault();
  
  const csrfToken = getCookie("csrftoken");
  
  let gameEndpoint = null
  if (method == 'POST') {
    gameEndpoint = getGameListCreateEndpoint();
  } else {
    gameEndpoint = getApiDetailEndpoint();
  }

  let matchDetailEndpoint = null

  if (window.location.href.includes('match')) {
    matchDetailEndpoint = getApiDetailEndpoint();
  } else if (window.location.href.includes('game')) {
    const gameDetailEndpoint = window.location.origin + '/api' + window.location.pathname;
    let gameJson = await getJsonResponse(gameDetailEndpoint);
    matchDetailEndpoint = gameJson.match;
  };
  
  let playersUserEnd = await getPlayersUsernameEndpoint(matchDetailEndpoint);

  // Form fields
  let match = matchDetailEndpoint;
  
  let winnerUsername = document.getElementById('winner-dropdown').value;
  let winnerEndpoint = playersUserEnd[winnerUsername];
  
  // Delete winner from `players`, leaving only the loser
  delete playersUserEnd[winnerUsername]
  let loserEndpoint = Object.values(playersUserEnd)[0]
  
  let points = document.getElementById('points-input').value;
  let gin = document.getElementById('gin-input').checked;
  let undercut = document.getElementById('undercut-input').checked;
  
  // Logged in user placeholder, switch out later when I figure out login
  let createdBy = winnerEndpoint

  return fetch(gameEndpoint, {
    method: method,
    headers: {
      'Content-type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({
      'match': match,
      'winner': winnerEndpoint,
      'loser': loserEndpoint,
      'points': points,
      'gin': gin,
      'undercut': undercut,
    }),
  })
}

export function fillPoints(points) {
  let pointsInput = document.getElementById('points-input');
  pointsInput.value = points;
}

export function fillCheckbox(elementId, boolVal) {
  let checkboxElem = document.getElementById(elementId);
  checkboxElem.checked = boolVal;
}
