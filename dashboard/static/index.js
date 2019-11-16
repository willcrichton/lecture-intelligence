$(() => {
  $.get('/api/lectures').then((lectures) => {
    lectures.append
    lectures.forEach((lec, i) => {
      const active = i == 0 ? "active" : "";
      $('.lecture-nav').append(`
<li class="nav-item">
  <a class="nav-link ${active}" href="#lec${lec.index}" data-toggle="tab">
    Lecture ${lec.index}
  </a>
</li>
      `);
      $('.lecture-tabs').append(`
<div class="lecture tab-pane ${active}" id="lec${lec.index}">
  <img src="/api/plot.svg?kind=lecture_heatmap&lec=${lec.index}" class="plot"/>
</div>
      `);
    });
  });
});
