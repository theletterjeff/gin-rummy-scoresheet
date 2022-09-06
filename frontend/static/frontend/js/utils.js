export async function getJsonResponse(endpoint) {
  let json = await fetch(endpoint)
             .then((response) => response.json());
  return json;
}

export async function getJsonResponseArray(endpointArray) {
  let jsonArray = [];
  for (let endpoint of endpointArray) {
    jsonArray.push(await getJsonResponse(endpoint));
  };
  return jsonArray;
}

export function fillTitle(titleString) {
  let title = document.getElementsByTagName('title')[0];
  title.innerHTML = titleString;
}

/** Get cookie value (used to pass CSRF token to POST requests) */
export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

export function setFormElemAsDisabled(elemName) {
  document.getElementById(elemName).setAttribute('disabled', '');
}

export function formatDate(dateObj) {
  if ((dateObj instanceof Date) == false) {
    dateObj = new Date(dateObj);
  };
  let monthNum = dateObj.getMonth() + 1;
  let dateNum = dateObj.getDate();
  let yearNum = dateObj.getUTCFullYear();
  return `${monthNum}/${dateNum}/${yearNum}`;
}

export function formatDateRange(dateObjStart, dateObjEnd) {
  let formattedStart = formatDate(dateObjStart);
  let formattedEnd = formatDate(dateObjEnd);
  return `${formattedStart}-${formattedEnd}`;
}

/**
 * Extract a username from a URL that is configured to put the username at
 * the end of the URL. This applies to match-list and player-detail URLs.
 */
export function getUsernameFromEndOfURL(urlStr) {
  urlArray = urlStr.split('/')
  return urlArray[urlArray.length - 1]
}