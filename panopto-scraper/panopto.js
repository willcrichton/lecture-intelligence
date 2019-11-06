chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.text == 'canvas_scrape') {
    let promises = Array.from(document.body.querySelectorAll('.detail-title')).map(
      (el) => {
        let href = el.href;
        if (!href) { return; }
        let id = href.match(/id=(.*)/i)[1];
        console.assert(id);
        let date = el.textContent.match(/\d+\/\d+\/\d+/)[0];
        console.assert(date);
        let url = `https://stanford-pilot.hosted.panopto.com/Panopto/Services/Export.ashx?action=ExportDeliveryAnalytics&delivery=${id}&type=HeatMap&timezone=America%2FLos_Angeles`;
        return fetch(url).then((response) =>
          response.blob().then((blob) => {
            let form = new FormData();
            form.append(`${date.replace(/\//g, "_")}.zip`, blob);
            return fetch('http://localhost:5000', {
              method: 'POST',
              body: form
            });
          }));
      });

    Promise
      .all(promises)
      .then((responses) => {
        console.log(responses[0]);
        alert('Successfully scraped video data');
      });

    sendResponse("");
  }
});
