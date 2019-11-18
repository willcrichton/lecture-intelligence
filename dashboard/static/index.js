$(() => {
  let fill_tab = (kind) => {
    $.get(`/api/${kind}`).then((objs) => {
      objs.forEach((obj, i) => {
        const active = i == 0 ? "active" : "";
        $(`.${kind}-nav`).append(`
<li class="nav-item">
  <a class="nav-link ${active}" href="#${kind}${obj.index}" data-toggle="tab">
    ${obj.index}
  </a>
</li>
        `);

        let plots;
        if (kind == 'lectures') {
          plots =`
<img src="/api/plot.svg?kind=lecture_heatmap&lec=${obj.index}" class="plot"/>
          `;
        } else {
          plots = `
<img src="/api/plot.svg?kind=plot_assignment&assignment_index=${obj.index}" class="plot"/>
          `;
        }
;
        $(`.${kind}-tabs`).append(`
<div class="${kind} tab-pane ${active}" id="${kind}${obj.index}">${plots}</div>
        `);
      });
    });
  }

  fill_tab('lectures');
  fill_tab('assignments');
});
