import { fillTitle, getJsonResponse, getUsernameFromEndOfURL } from './utils.js';
import { getDetailEndpointFromEditURL,
         getFrontendURL } from './endpoints.js';
import { fillPoints, fillCheckbox,
         submitGameForm } from './game-form.js';

const gameDetailEndpoint = getDetailEndpointFromEditURL();

fillGameEditPage();

/**
 * Main function for filling the Game Edit page.
 */
async function fillGameEditPage() {
  fillTitle('Edit Game');
  fillGameEditForm();
}

/**
 * Populate form fields with current data, add PATCH event to submit button.
 */
async function fillGameEditForm() {
  const gameJson = await getJsonResponse(gameDetailEndpoint);
  
  const matchDetailEndpoint = gameJson.match;

  // Values to use in form
  const winnerUsername = getUsernameFromEndOfURL(gameJson.winner);
  const loserUsername = getUsernameFromEndOfURL(gameJson.loser);
  const points = gameJson.points;
  const gin = gameJson.gin;
  const undercut = gameJson.undercut;

  fillWinnerDropdown(winnerUsername, loserUsername);
  fillPoints(points);
  fillCheckbox("gin-input", gin);
  fillCheckbox("undercut-input", undercut);

  addGameEditSubmitEvent(matchDetailEndpoint);
}

async function addGameEditSubmitEvent(matchDetailEndpoint) {
  let gameEditForm = document.getElementById('edit-game-form');
  gameEditForm.addEventListener('submit', function(e) {
    submitGameForm(e, 'PATCH')
    .then((resp) => console.log(resp.status))
    .then(() => {window.location = getFrontendURL(matchDetailEndpoint)})
  })
}

/**
 * Fill the 'winner' dropdown with players' usernames.
 */
function fillWinnerDropdown(winnerUsername, loserUsername) {
  let dropdownOptions = ```
    <option select value=${winnerUsername}>${winnerUsername}</option>
    <option values=${loserUsername}>${loserUsername}</option>
  ```
  let winnerDropdown = document.getElementById('winner-dropdown');
  winnerDropdown.innerHTML = dropdownOptions;
}