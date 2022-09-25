import { 
  fillTitle,
  getJsonResponse,
  getRequestPlayerUsername,
  getValFromUrl
} from './utils.js';
import { getGameDetailEndpoint, getMatchDetailEndpoint } from './endpoints.js';

fillTitles();
fillNavbarLinks();

// Base template functions
function fillNavbarLinks() {
  fillNavbarLink('navbar-brand', '');
  if (document.getElementById('login-link')) {
    fillNavbarLink('login-link', '/accounts/login/');
    fillNavbarLink('signup-link', '/accounts/signup/');
  } else {
    getRequestPlayerUsername().then(function(username) {
      fillNavbarLink('matches-nav-link', `/players/${username}/matches/`);
      fillNavbarLink('players-nav-link', `/players/`);
      fillNavbarLink('account-nav-link', `/players/${username}/`);
      fillNavbarLink('logout-nav-link', '/accounts/logout/');
    });
  };
}

function fillNavbarLink(elemName, urlExtension) {
  let navbarElem = document.getElementById(elemName);
  navbarElem.href = window.location.origin + urlExtension
}
/**
 * Title filling for all pages in the project.
 */
async function fillTitles() {
  const path = window.location.pathname;
  const playerListRegex = new RegExp('^/players/$'),
        playerProfileRegex = new RegExp('^/players/([a-zA-Z]+\w*)/$'),
        playerEditRegex = new RegExp('^/players/([a-zA-Z]+\w*)/edit-profile/$'),
        matchListRegex = new RegExp('^/players/([a-zA-Z]+\w*)/matches/$'),
        matchDetailRegex = new RegExp('^/matches/([0-9]+)/$'),
        matchEditRegex = new RegExp('^/matches/([0-9]+)/edit/$'),
        gameEditRegex = new RegExp('^/matches/([0-9]+)/games/([0-9]+)/edit/$'),
        loginRegex = new RegExp('^/accounts/login/$'),
        logoutRegex = new RegExp('^/accounts/logout/$'),
        signupRegex = new RegExp('^/accounts/signup/$');
  let username = getValFromUrl(path, 'players'),
      matchPk = getValFromUrl(path, 'matches'),
      matchDetailEndpoint = getMatchDetailEndpoint(matchPk),
      matchData = null,
      gamePk = getValFromUrl(path, 'games'),
      gameDetailEndpoint = getGameDetailEndpoint(matchPk, gamePk),
      gameData = null,
      usernames = [];

  switch (true) {
    case playerListRegex.test(path):
      fillTitle('Players');
      break;
    case playerProfileRegex.test(path):
      fillTitle(`Player Profile - ${username}`);
      break;
    case playerEditRegex.test(path):
      fillTitle(`Edit Profile - ${username}`);
      break;     
    case matchListRegex.test(path):
      fillTitle(`Matches - ${username}`);
      break;
    case matchDetailRegex.test(path):
      matchData = await getJsonResponse(matchDetailEndpoint);
      for (let playerUrl of matchData.players) {
        let playerData = await getJsonResponse(playerUrl);
        usernames.push(playerData.username);
      };
      fillTitle(`Match - ${usernames[0]} v. ${usernames[1]}`);
      break;
    case matchEditRegex.test(path):
      matchData = await getJsonResponse(matchDetailEndpoint);
      for (let playerUrl of matchData.players) {
        let playerData = await getJsonResponse(playerUrl);
        usernames.push(playerData.username);
      };
      fillTitle(`Edit Match - ${usernames[0]} v. ${usernames[1]}`);
      break;
    case gameEditRegex.test(path):
      gameData = await getJsonResponse(gameDetailEndpoint);
      for (let playerUrl of [gameData.winner, gameData.loser]) {
        let playerData = await getJsonResponse(playerUrl);
        usernames.push(playerData.username);
      };
      fillTitle(`Edit Game - ${usernames[0]} v. ${usernames[1]}`);
      break;
    case loginRegex.test(path):
      fillTitle('Log In');
      break;
    case logoutRegex.test(path):
      fillTitle('Logged Out');
      break;
    case signupRegex.test(path):
      fillTitle('Sign Up');
      break;
  };
}