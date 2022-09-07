import { fillTitle, getJsonResponse } from '../utils.js';
import { getPlayerFullName } from './utils.js';

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
 * '^players/(?P<username>[a-zA-z]+.*)/$'
 */
 function getUsername() {
  let urlPath = window.location.pathname;
  return urlPath.split('/')[2];
}
/**
 * Given a player's username, return the API endpoint for that player's
 * player-detail view.
 */
 function getPlayerDetailEndpoint(username) {
  return window.location.origin + `/api/players/${username}/`
}
/**
 * Fill the page title for the player detail page.
 */
 function fillPlayerDetailTitle(username) {
  fillTitle(`Gin Rummy Scoresheet - ${username}`);
}
/**
 * Fills data within the player profile card--full name, email, date joined,
 * last login.
 */
function fillProfileCard(playerJson) {
  fillProfileElem('player-username', playerJson.username);
  fillProfileElem('player-name', getPlayerFullName(playerJson));
  fillProfileElem('player-email', playerJson.email);
  linkPlayerEmail('player-email', playerJson.email);
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

function linkPlayerEmail(emailElemName, emailValue) {
  let emailElem = document.getElementById(emailElemName);
  emailElem.href = "mailto:" + emailValue;
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
