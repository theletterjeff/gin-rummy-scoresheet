import { getCookie, getJsonResponse } from '../utils.js';
import { getApiDetailEndpoint, getFrontendURL } from '../endpoints.js';

let playerJson = await getJsonResponse(
  window.location.origin + '/api/logged-in-player/')
fillPlayerEditPlaceholders();
addPlayerEditButtonEvent();

function fillPlayerEditPlaceholders() {

  fillDefaultInputText('player-username-input', playerJson.username);
  fillDefaultInputText('player-first-name-input', playerJson.first_name);
  fillDefaultInputText('player-last-name-input', playerJson.last_name);
  fillDefaultInputText('player-email-input', playerJson.email);
}

function fillDefaultInputText(elemName, defaultInputText) {
  let elem = document.getElementById(elemName);
  elem.value = defaultInputText;
}

async function addPlayerEditButtonEvent() {
  const playerEditApiEndpoint = getApiDetailEndpoint();
  const submitBtn = document.getElementById('player-edit-submit');
  submitBtn.addEventListener('click', function(e) {
    e.preventDefault();
    const csrfToken = getCookie('csrftoken');

    // Form values
    let username = document.getElementById('player-username-input').value;
    let firstName = document.getElementById('player-first-name-input').value;
    let lastName = document.getElementById('player-last-name-input').value;
    let email = document.getElementById('player-email-input').value;

    return fetch(playerEditApiEndpoint, {
      method: 'PATCH',
      headers: {
        'Content-type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        'username': username,
        'first_name': firstName,
        'last_name': lastName,
        'email': email,
      }),
    }).then(() => {window.location = getFrontendURL(playerJson.url)})
  })
}