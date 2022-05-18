/** Export functions for player-profile.js and player-edit.js */

import { getApiDetailEndpoint } from '../endpoints.js';
import { getJsonResponse } from '../utils.js';

export async function getPlayerJson() {
  let playerApiEndpoint = null;

  if (window.location.href.includes('edit')) {
    let baseEndpoint = getApiDetailEndpoint();
    const re = new RegExp('.+\\/(?=\\w+\\/)');
    playerApiEndpoint = re.exec(baseEndpoint)[0];
  } else {
   playerApiEndpoint = getApiDetailEndpoint();
  }

  return getJsonResponse(playerApiEndpoint);
}

export function getPlayerFullName(playerJson) {
  return playerJson.first_name + " " + playerJson.last_name;
}
