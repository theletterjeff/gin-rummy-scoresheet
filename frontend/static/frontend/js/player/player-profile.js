import { getJsonResponse } from '../utils.js';
import { getPlayerFullName } from './utils.js';
import { getPlayerDetailEndpoint, getRequestPlayerEndpoint } from '../endpoints.js';

fillPlayerPage();

/**
 * Main function for filling the player detail page.
 */
async function fillPlayerPage() {
  const username = getUsername();
  const playerDetailEndpoint = getPlayerDetailEndpoint(username);
  let playerJson = await getJsonResponse(playerDetailEndpoint);
  
  const requestPlayerEndpoint = getRequestPlayerEndpoint();
  const requestPlayerJson = await getJsonResponse(requestPlayerEndpoint);

  fillPlayerDetailTitle(username);
  fillProfileCard(playerJson, requestPlayerJson);
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
 * Fills data within the player profile card--full name, date joined,
 * last login.
 */
function fillProfileCard(playerJson, requestPlayerJson) {
  fillProfileElem('player-username', playerJson.username);
  fillProfileElem('player-name', getPlayerFullName(playerJson));
  fillProfileElem('player-date-joined', makeDateString(playerJson.date_joined));
  fillProfileElem('player-last-login', makeDateString(playerJson.last_login));
  addEditButton(playerJson, requestPlayerJson);
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
function addEditButton(playerJson, requestPlayerJson) {
  if (playerJson.url == requestPlayerJson.url) {
    const editPlayerUrl = window.location.href + 'edit-profile/';
    let playerCardDiv = document.getElementById('player-card-body');
    playerCardDiv.innerHTML += `
      <div class="d-grid col-4 col-md-3 col-lg-2 mx-auto mt-4">
        <a href="${editPlayerUrl}" class="btn btn-outline-success"">Edit</a>
      </div>
    `;
  };
}