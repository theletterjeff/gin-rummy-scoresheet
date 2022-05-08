export function fillTitle(titleString) {
  let title = document.getElementsByTagName('title')[0];
  title.innerHTML = titleString;
}