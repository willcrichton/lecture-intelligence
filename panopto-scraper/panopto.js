const LOCAL_URL = `http://localhost:5000`;

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

const run_download = async (init_callback, counter_callback, complete_callback) => {
  let counter = 0;
  const videos = document.body.querySelectorAll('.detail-title');
  const promises = Array.from(videos).map(
    (el) => {
      const href = el.href;
      if (!href) { return; }
      const id = href.match(/id=(.*)/i)[1];
      console.assert(id);
      const date = el.textContent.match(/\d+\/\d+\/\d+/)[0];
      console.assert(date);

      /* if (should_dl_videos) {
       *   let download_url = `${origin}/Panopto/Podcast/Download/${id}.mp4?mediaTargetType=videoPodcast`;
       *   window.open(download_url, '_blank');
       * }
       */

      const url = `${origin}/Panopto/Services/Export.ashx?action=ExportDeliveryAnalytics&delivery=${id}&type=HeatMap&timezone=America%2FLos_Angeles`;
      return [url, date];
    }).filter((tuple) => tuple).map(async ([url, date]) => {
      const response = await fetch(url);
      const blob = await response.blob();
      let form = new FormData();
      form.append(`${date.replace(/\//g, "_")}.zip`, blob);
      await fetch(`${LOCAL_URL}/api/upload_viewing_data`, {
        method: 'POST',
        body: form
      });
      counter += 1;
      counter_callback(counter);
    });

  init_callback(promises.length);

  await Promise.all(promises);
  await fetch(`${LOCAL_URL}/api/generate_lecture_json`);

  complete_callback();
}

chrome.runtime.onMessage.addListener(async (msg, sender, sendResponse) => {
  if (msg.text == 'canvas_scrape') {
    const origin = window.location.origin;

    try {
      await fetch(`${LOCAL_URL}/api/ping`);
    } catch (e) {
      alert('You must start the Lecture Intelligence local server before running this script. Please review the setup instructions.');
      return;
    }

    document.querySelector('#resultsSizeLinks a:nth-child(13)').click();

    const popup = document.createElement('div');
    popup.innerHTML = `
      <h1 style='margin-bottom: 10px;'>Download Panopto metadata</h1>

      <div id="li-step1">
        This script will download all lecture viewing metadata for each course listed on this page. Do you want to proceed?<br /><br />

        <button id='li-yes'>Yes</button> <button id='li-no'>No</button>
      </div>

      <div id="li-step2" style="display: none">
        Downloading video metadata. Current progress:<br />
        <span id='li-counter'>0</span>/<span id='li-total'>0</span>
      </div>
    `;

    Object.assign(popup.style, {
      position: 'absolute',
      'z-index': 1000,
      width: '400px',
      top: '20px',
      left: 'calc(50% - 200px)',
      background: 'white',
      border: '1px solid #ddd',
      padding: '10px',
      'box-shadow': '3px 3px 4px #eee'
    });

    const counter = popup.querySelector('#li-counter');
    const total = popup.querySelector('#li-total');

    popup.querySelector('#li-yes').addEventListener('click', () => {
      popup.querySelector('#li-step1').style.display = 'none';
      popup.querySelector('#li-step2').style.display = 'block';

      try {
        run_download((n) => {
          total.innerHTML = n;
        }, (n) => {
          counter.innerHTML = n;
        }, () => {
          popup.remove();
          window.open(`${LOCAL_URL}`, '_blank')
        });
      } catch (e) {
        alert(`Script failed with error:\n${e.stack}`);
      }
    });

    popup.querySelector('#li-no').addEventListener('click', () => {
      popup.remove();
    });

    document.body.appendChild(popup);
  }

  sendResponse("");
});
