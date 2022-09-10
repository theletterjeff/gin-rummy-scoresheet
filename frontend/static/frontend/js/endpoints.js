import { getJsonResponse } from "./utils.js";

const baseUrl = window.location.origin;
const basePlayerUrl = baseUrl + '/players/'
const baseMatchUrl = baseUrl + '/matches/'

/**
 * Get API endpoint for player-detail.
 */
export function getPlayerDetailEndpoint(username) {
  return basePlayerUrl + username + '/';
}
/**
 * Get API endpoint for player-list-all.
 */
export function getPlayersListAllEndpoint() {
  return basePlayerUrl;
}
/**
 * Get API endpoint for player-create.
 */
export function getPlayerCreateEndpoint() {
  return basePlayerUrl + 'create/';
}
/**
 * Get API endpoint for request-player.
 */
export function getRequestPlayerEndpoint() {
  return baseUrl + '/request-player/';
}
/**
 * Get API endpoint for match-list-player.
 */
export function getMatchListPlayerEndpoint(username) {
  return basePlayerUrl + 'matches/';
}
/**
 * Get API endpoint for game-list-player.
 */
 export function getGameListPlayerEndpoint(username) {
  return basePlayerUrl + 'games/';
}
/**
 * Get API endpoint for score-list-player.
 */
 export function getScoreListPlayerEndpoint(username) {
  return basePlayerUrl + 'scores/';
}
/**
 * Get API endpoint for outcome-list-player.
 */
 export function getOutcomeListPlayerEndpoint(username) {
  return basePlayerUrl + 'outcomes/';
}
/**
 * Get API endpoint for match-detail.
 */
 export function getMatchDetailEndpoint(match_pk) {
  return baseMatchUrl + match_pk + '/';
}
/**
 * Get API endpoint for match-create.
 */
 export function getMatchCreateEndpoint() {
  return baseMatchUrl + 'create/';
}
/**
 * Get API endpoint for player-list-match.
 */
 export function getPlayerListMatchEndpoint(match_pk) {
  return baseMatchUrl + match_pk + 'players/';
}
/**
 * Get API endpoint for game-list-match.
 */
 export function getGameListMatchEndpoint(match_pk) {
  return baseMatchUrl + match_pk + 'games/';
}
/**
 * Get API endpoint for score-list-match.
 */
 export function getScoreListMatchEndpoint(match_pk) {
  return baseMatchUrl + match_pk + 'scores/';
}
/**
 * Get API endpoint for outcome-list-match.
 */
 export function getOutcomeListMatchEndpoint(match_pk) {
  return baseMatchUrl + match_pk + 'outcomes/';
}
/**
 * Get API endpoint for game-detail.
 */
 export function getGameDetailEndpoint(match_pk, game_pk) {
  return baseMatchUrl + match_pk + '/games/' + game_pk + '/';
}
/**
 * Get API endpoint for game-create.
 */
 export function getGameCreateView(match_pk) {
  return baseMatchUrl + match_pk + 'games/create/';
}
/**
 * Get API endpoint for score-detail.
 */
 export function getScoreDetailEndpoint(match_pk, username) {
  return baseMatchUrl + match_pk + '/players/' + username + '/scores/';
}
/**
 * Get API endpoint for outcome-detail.
 */
 export function getOutcomeDetailEndpoint(match_pk, username) {
  return baseMatchUrl + match_pk + '/players/' + username + '/outcomes/';
}



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
 return window.location.origin + `/api/players/${username}/`
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
