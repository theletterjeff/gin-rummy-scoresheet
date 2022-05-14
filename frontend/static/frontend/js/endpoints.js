import { getJsonResponse } from "./utils.js";

/** Return the endpoint for the API detail view corresponding to
 * the current frontend view */
 export function getApiDetailEndpoint() {
  const pageURL = new URL(window.location.href);
  const pageOrigin = pageURL.origin;
  const pagePath = pageURL.pathname;
  return `${pageOrigin}/api${pagePath}/`;
}

/** Return the endoint for the GameListCreate API view */
export function getGameListCreateEndpoint() {
  const pageURL = new URL(window.location.href);
  const pageOrigin = pageURL.origin;
  return `${pageOrigin}/api/game/`
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