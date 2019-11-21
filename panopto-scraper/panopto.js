chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.text == 'canvas_scrape') {
    let should_dl_videos = confirm('Starting scrape. Do you want to also download the videos?\n(Cancel means no, but still scrape viewing data)');
    let promises = Array.from(document.body.querySelectorAll('.detail-title')).map(
      (el) => {
        let href = el.href;
        if (!href) { return; }
        let id = href.match(/id=(.*)/i)[1];
        console.assert(id);
        let date = el.textContent.match(/\d+\/\d+\/\d+/)[0];
        console.assert(date);

        if (should_dl_videos) {
          let download_url = `https://stanford-pilot.hosted.panopto.com/Panopto/Podcast/Download/${id}.mp4?mediaTargetType=videoPodcast`;
          window.open(download_url, '_blank');
        }

        let url = `https://stanford-pilot.hosted.panopto.com/Panopto/Services/Export.ashx?action=ExportDeliveryAnalytics&delivery=${id}&type=HeatMap&timezone=America%2FLos_Angeles`;
        return fetch(url).then((response) =>
          response.blob().then((blob) => {
            let form = new FormData();
            form.append(`${date.replace(/\//g, "_")}.zip`, blob);
            return fetch('http://localhost:5000/api/upload_viewing_data', {
              method: 'POST',
              body: form
            });
          }));
      });

    Promise
      .all(promises)
      .then(() => fetch('http://localhost:5000/api/generate_lecture_json'))
      .then(() => {
        alert('Successfully scraped video data');
      });

    sendResponse("");
  }
});
