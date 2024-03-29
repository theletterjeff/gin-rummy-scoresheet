import { getJsonResponse, getValFromUrl } from './utils.js';
import { getDetailEndpointFromEditURL, getFrontendURL } from './endpoints.js';
import { fillPoints, fillCheckbox, 
         fillWinnerDropdown, submitGameForm } from './game-form.js';

const matchPk = getValFromUrl(window.location.href, 'matches');
fillGameEditPage();

/**
 * Main function for filling the Game Edit page.
 */
async function fillGameEditPage() {
  fillGameEditForm();
}

/**
 * Populate form fields with current Game data, add PATCH event to submit button.
 */
async function fillGameEditForm() {
  const gameDetailEndpoint = getDetailEndpointFromEditURL();
  const gameJson = await getJsonResponse(gameDetailEndpoint);
  const matchDetailEndpoint = gameJson.match;

  // Values to use in form
  const winnerUsername = getValFromUrl(gameJson.winner, 'players');
  const loserUsername = getValFromUrl(gameJson.loser, 'players');
  const points = gameJson.points;
  const gin = gameJson.gin;
  const undercut = gameJson.undercut;

  fillWinnerDropdown(winnerUsername, loserUsername);
  fillPoints("points-input", points);
  fillCheckbox("gin-input", gin);
  fillCheckbox("undercut-input", undercut);

  addGameEditSubmitEvent(matchDetailEndpoint);
}

/**
 * Add submit event to the game form on the game-edit page.
 */
async function addGameEditSubmitEvent(matchDetailEndpoint) {
  let gameEditForm = document.getElementById('edit-game-form');
  gameEditForm.addEventListener('submit', function(e) {
    submitGameForm(e, 'PATCH', matchPk)
    .then((resp) => console.log(resp.status))
    .then(() => {window.location = getFrontendURL(matchDetailEndpoint)})
  })
}

