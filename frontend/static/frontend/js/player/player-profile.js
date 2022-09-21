import { fillTitle, getJsonResponse } from '../utils.js';
import { getPlayerFullName } from './utils.js';
import { getPlayerDetailEndpoint } from '../endpoints.js';

fillPlayerPage();

/**
 * Main function for filling the player detail page.
 */
async function fillPlayerPage() {
  const username = getUsername();
  const playerDetailEndpoint = getPlayerDetailEndpoint(username);
  let playerJson = await getJsonResponse(playerDetailEndpoint);

  fillPlayerDetailTitle(username);
  fillProfileCard(playerJson);
}
/**
 * Get the username from the player detail URL.
 * 
 * URLs for the `player-detail` page should be formatted as
 * '^players/(?P<username>[a-zA-Z]+\w*)/$'
 */
 function getUsername() {
  let urlPath = window.location.pathname;
  return urlPath.split('/')[2];
}
/**
 * Fill the page title for the player detail page.
 */
 function fillPlayerDetailTitle(username) {
  fillTitle(`Gin Rummy Scoresheet - ${username}`);
}
/**
 * Fills data within the player profile card--full name, date joined,
 * last login.
 */
function fillProfileCard(playerJson) {
  fillProfileElem('player-username', playerJson.username);
  fillProfileElem('player-name', getPlayerFullName(playerJson));
  fillProfileElem('player-date-joined', makeDateString(playerJson.date_joined));
  fillProfileElem('player-last-login', makeDateString(playerJson.last_login));
  addEditButtonRedirect();
}

function fillProfileElem(elemName, value) {
  let elem = document.getElementById(elemName)

  const re = new RegExp('\\w+');
  let fillValue = (re.exec(value) != null) ? value : "--";

  elem.innerHTML = fillValue;
}

function makeDateString(date) {
  return new Date(date).toDateString();
}
/**
 * Add link to the "Edit" button that redirects to the player-edit page.
 */
function addEditButtonRedirect() {
  const editPlayerEndpoint = window.location.href + 'edit-profile/'
  const editBtn = document.getElementById('edit-button');
  editBtn.addEventListener('click', function() {
    window.location = editPlayerEndpoint;
  })
}
