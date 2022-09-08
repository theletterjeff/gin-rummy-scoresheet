import { getCookie, getJsonResponse, getValFromUrl } from '../utils.js';
import { getFrontendURL } from '../endpoints.js';

fillPlayerEditPage();

/**
 * Main function for filling the player-edit page.
 */
async function fillPlayerEditPage() {
  const username = getValFromUrl(window.location.href, 'players');
  const playerDetailEndpoint = window.location.origin + `/api/players/${username}/`
  let playerJson = await getJsonResponse(playerDetailEndpoint);
  fillPlayerEditPlaceholders(playerJson);
  addPlayerEditButtonEvent(playerJson);
}
/**
 * Populate form fields with current player information.
 */
function fillPlayerEditPlaceholders(playerJson) {

  fillDefaultInputText('player-username-input', playerJson.username);
  fillDefaultInputText('player-first-name-input', playerJson.first_name);
  fillDefaultInputText('player-last-name-input', playerJson.last_name);
  fillDefaultInputText('player-email-input', playerJson.email);
}
/**
 * Helper function for filling in form fields with curren player information.
 */
function fillDefaultInputText(elemName, defaultInputText) {
  let elem = document.getElementById(elemName);
  elem.value = defaultInputText;
}
/**
 * Add a PATCH event to the submit button.
 */
async function addPlayerEditButtonEvent(playerJson) {
  const submitBtn = document.getElementById('player-edit-submit');
  submitBtn.addEventListener('click', function(e) {
    e.preventDefault();
    const csrfToken = getCookie('csrftoken');

    // Form values
    let username = document.getElementById('player-username-input').value;
    let firstName = document.getElementById('player-first-name-input').value;
    let lastName = document.getElementById('player-last-name-input').value;
    let email = document.getElementById('player-email-input').value;

    return fetch(playerJson.url, {
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
    })
    .then(() => {window.location = getFrontendURL(playerJson.url)})
  })
}
