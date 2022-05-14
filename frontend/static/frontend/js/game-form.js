import { getPlayersEndpointUsername, getGameListCreateEndpoint } from "./endpoints.js";
import { getCookie } from "./utils.js";

export async function fillWinnerDropdown(matchDetailEndpoint, defaultWinner=null) {
  let players = await getPlayersEndpointUsername(matchDetailEndpoint);
  
  let dropdownOptions = ""

  Object.values(players).forEach(function(username) {
    let dropdownOption = `<option value=${username}>${username}</option>`;
    dropdownOptions += dropdownOption;
    
    if (defaultWinner == username) {
      dropdownOption.replace('option', 'option select');
    };
  })

  let winnerDropdown = document.getElementById('winner-dropdown');
  winnerDropdown.innerHTML = dropdownOptions;
}

export async function submitGameForm(e) {
  e.preventDefault();
  
  const csrfToken = getCookie("csrftoken");
  
  const gameEndpoint = getGameListCreateEndpoint();
  const matchDetailEndpoint = getApiDetailEndpoint();
  
  let playersUserEnd = await getPlayersUsernameEndpoint(matchDetailEndpoint);
  let playersEndUser = await getPlayersEndpointUsername(matchDetailEndpoint)

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

  fetch(gameEndpoint, {
    method: 'POST',
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
      'created_by': createdBy,
    }),
  }).then(() => listGames(playersEndUser));
  
  console.log('Form Submitted');
}
