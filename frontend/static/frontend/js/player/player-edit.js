import { getPlayerJson } from './utils.js';

let playerJson = await getPlayerJson();
fillPlayerEditPlaceholders();

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