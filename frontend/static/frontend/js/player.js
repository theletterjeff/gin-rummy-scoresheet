import { getApiDetailEndpoint } from './endpoints.js';
import { getJsonResponse, fillTitle } from './utils.js';

let playerJson = await getPlayerJson();
fillPlayerPage();

async function getPlayerJson() {
  const playerApiEndpoint = getApiDetailEndpoint();
  return getJsonResponse(playerApiEndpoint);
}

function fillPlayerPage() {
  fillPlayerPageTitle('');
  fillProfileCard();
}

function fillPlayerPageTitle() {
  const playerPageTitle = playerJson.username + "'s Profile"
  fillTitle(playerPageTitle);
}

function fillProfileCard() {
  fillProfileElem('player-username', playerJson.username);
  fillProfileElem('player-name', getPlayerFullName());
  fillProfileElem('player-email', playerJson.email);
  linkPlayerEmail();
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

function getPlayerFullName() {
  return playerJson.first_name + " " + playerJson.last_name;
}

function linkPlayerEmail() {
  let emailElem = document.getElementById('player-email');
  emailElem.href = `mailto:${playerJson.email}`;
}

function makeDateString(date) {
  return new Date(date).toDateString();
}

function addEditButtonRedirect() {
  const editPlayerEndpoint = window.location.href + 'edit/'
  const editBtn = document.getElementById('edit-button');
  editBtn.addEventListener('click', function() {
    window.location = editPlayerEndpoint;
  })
}