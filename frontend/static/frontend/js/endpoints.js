import { getJsonResponse } from "./utils.js";

/** Return the endpoint for the API detail view corresponding to
 * the current frontend view */
 export function getApiEndpointFromUrl() {
  const pageURL = new URL(window.location.href);
  const pageOrigin = pageURL.origin;
  const pagePath = pageURL.pathname;
  return `${pageOrigin}/api${pagePath}`;
}

/**
 * Remove 'edit/' from the end of a URL. The resulting URL should
 * represent the `detail` endpoint for the related model (which accepts
 * PUT and PATCH requests).
 */
export function getDetailEndpointFromEditURL() {
  const apiDetailEndpoint = getApiEndpointFromUrl();
  const urlWithoutEditRegex = new RegExp('.+(?=edit\/)');
  return urlWithoutEditRegex.exec(apiDetailEndpoint);
}
/**
 * Given a player's username, return the API endpoint for that player's
 * player-detail view.
 */
export function getPlayerDetailEndpoint(username) {
 return window.location.origin + `/api/player/${username}/`
}

/**
 * Return the endoint for the GameCreate API view.
 */
export function getGameCreateEndpoint(matchPk) {
  const pageURL = new URL(window.location.href);
  const pageOrigin = pageURL.origin;
  return `${pageOrigin}/api/matches/${matchPk}/games/create/`
}

/* Return a players object {username: endpoint} */
export async function getPlayersEndpointUsername(matchDetailEndpoint) {
  let players = {}
  let matchData = await getJsonResponse(matchDetailEndpoint)

  for (let playerEndpoint of matchData.players) {
    let playerJSON = await getJsonResponse(playerEndpoint)
    let username = await playerJSON.username;
    players[playerEndpoint] = username;
  };
  return players;
}

/** Return a players object {endpoint: username} */
export async function getPlayersUsernameEndpoint(matchDetailEndpoint) {
  let players = await getPlayersEndpointUsername(matchDetailEndpoint);
  let playersFlipped = {};

  // Make the keys into values and the values into keys
  Object.entries(players).forEach(([key, value]) => {playersFlipped[value] = key});
  
  return playersFlipped;
}

/** Derive frontend URL for a match from the API endpoint */
export function getFrontendURL(apiEndpoint) {
  return apiEndpoint.replace('api/', '');
}
