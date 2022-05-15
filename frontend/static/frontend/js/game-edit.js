import { fillTitle, getJsonResponse } from './utils.js';
import { getApiDetailEndpoint, getFrontendURL } from './endpoints.js';
import { fillWinnerDropdown, fillPoints, fillCheckbox, submitGameForm } from './game-form.js';

const gameDetailEndpoint = getApiDetailEndpoint();

fillGameEditPage();

async function fillGameEditPage() {
  fillTitle('Edit Game');
  fillGameEditForm();
}

async function fillGameEditForm() {
  const gameJson = await getJsonResponse(gameDetailEndpoint);
  
  const winnerEndpoint = gameJson.winner;
  const winnerJson = getJsonResponse(winnerEndpoint);
  
  const matchDetailEndpoint = gameJson.match;

  // Values to use in form
  const winnerUsername = winnerJson.username;
  const points = gameJson.points;
  const gin = gameJson.gin;
  const undercut = gameJson.undercut;

  fillWinnerDropdown(matchDetailEndpoint, winnerUsername);
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