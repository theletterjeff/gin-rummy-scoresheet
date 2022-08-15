/** Export functions for player-profile.js and player-edit.js */

export function getPlayerFullName(playerJson) {
  return playerJson.first_name + " " + playerJson.last_name;
}
