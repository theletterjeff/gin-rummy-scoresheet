import { 
  getFrontendURL,
  getGameListPlayerEndpoint,
  getOutcomeListPlayerEndpoint,
  getPlayersListAllEndpoint,
  getRequestPlayerEndpoint,
} from "../endpoints.js";
import {
  formatAsPct,
  getJsonResponse,
  getValFromUrl,
} from '../utils.js';

// Page constants
const playerListAllEndpoint = getPlayersListAllEndpoint();
const requestPlayerEndpoint = getRequestPlayerEndpoint();

fillPlayerListPage();

/**
 * Main execution function
 */
async function fillPlayerListPage() {
  // Data
  const playerListAllData = await getJsonResponse(playerListAllEndpoint);
  const requestPlayerData = await getJsonResponse(requestPlayerEndpoint);

  // Execution
  fillPlayerListTable(playerListAllData);
}
/**
 * Fill the player list table.
 */
async function fillPlayerListTable(playerListAllData) {
  for (let playerData of playerListAllData.results) {
    let playerUrl = getFrontendURL(playerData.url);
    let playerPk = getPlayerPk(playerData);
    let username = playerData.username;

    let matchWinPct = await getMatchWinPct(username);
    matchWinPct = formatAsPct(matchWinPct);

    let gameWinPct = await getGameWinPct(username);
    gameWinPct = formatAsPct(gameWinPct);

    let playersBody = document.getElementById('players-table-body');

    fillPlayersTableRow(
      playerUrl, playerPk, username, matchWinPct, gameWinPct, playersBody);
  }
}
/**
 * Add a row to the player's table
 */
function fillPlayersTableRow(playerUrl, playerPk, username, matchWinPct, gameWinPct, playersBody) {
  const rowHTML = `
  <tr id="row-player-${playerPk}" class="row-player">
    <td id="player-username-${playerPk}"><a href="${playerUrl}">${username}</a></td>
    <td id="player-match-win-pct-${playerPk}">${matchWinPct}</td>
    <td id="player-game-win-pct-${playerPk}">${gameWinPct}</td>
  `;
  playersBody.innerHTML += rowHTML;
}
/**
 * Get the record ID (PK) of the player.
 */
function getPlayerPk(playerData) {
  return getValFromUrl(playerData.url, 'players');
}
/**
 * Calculate the percentage of matches the player has won.
 */
async function getMatchWinPct(username) {
  const outcomeListPlayerEndpoint = getOutcomeListPlayerEndpoint(username);
  const outcomeData = await getJsonResponse(outcomeListPlayerEndpoint);
  
  // If no completed matches
  if (outcomeData.count == 0) {
    return '--';
  };
  // Add up wins, divide by number of completed matches
  let playerWins = null;
  for (let outcome of outcomeData.results) {
    if (outcome.player_outcome == 1) {
      playerWins += 1;
    };
  };
  return playerWins / outcomeData.count;
}
/**
 * Calculate the percentage of games the player has won.
 */
 async function getGameWinPct(username) {
  const gameListPlayerEndpoint = getGameListPlayerEndpoint(username);
  const gameData = await getJsonResponse(gameListPlayerEndpoint);
  
  // If no completed matches
  if (gameData.count == 0) {
    return '--';
  };
  // Add up wins, divide by number of completed games
  let playerWins = null;
  for (let game of gameData.results) {
    let winnerUsername = getValFromUrl(game.winner, 'players');
    if (winnerUsername == username) {
      playerWins += 1;
    };
  };
  return playerWins / gameData.count;
}
