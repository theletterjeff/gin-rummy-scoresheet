import { fillTitle, getJsonResponse } from './utils.js';
import { getApiDetailEndpoint } from './endpoints.js';
import { fillWinnerDropdown, fillPoints, fillCheckbox } from './game-form.js';

fillGameEditPage();

async function fillGameEditPage() {
  fillTitle('Edit Game');
  fillGameEditForm();
}

async function fillGameEditForm() {
  const gameDetailEndpoint = getApiDetailEndpoint();
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
}