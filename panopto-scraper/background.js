chrome.browserAction.onClicked.addListener((tab) => {
  chrome.tabs.sendMessage(tab.id, {text: 'canvas_scrape'}, () => {});
});
