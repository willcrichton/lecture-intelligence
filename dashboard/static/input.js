$(() => {
  $.get('/api/lectures').then((lectures) => {
    $('#add-lecture').click(() => {
      lectures.push({
        name: '', index: 1, date: ''
      })
    });

    $('#remove-lecture').click(() => {
      lectures.pop();
    });

    const lecture_table = new Tabulator('#lectures', {
      layout: "fitColumns",
      data: lectures,
      reactiveData: true,
      columns: [
        {title: "Index", field:"index", editor:"input"},
        {title: "Name", field:"name", editor:"input"},
        {title: "Date", field:"date", editor:"input"}
      ],
      dataEdited: (data) => {
        $.post({
          url: '/api/lectures',
          data: JSON.stringify(data),
          contentType: "application/json"
        });
      }
    });
  });

  $.get('/api/assignments').then((assignments) => {
    $('#add-assignment').click(() => {
      assignments.push({
        name: '', index: 1, duedate: '', lectures: ''
      })
    });

    $('#remove-assignment').click(() => {
      assignments.pop();
    });

    const assignment_table = new Tabulator('#assignments', {
      layout: "fitColumns",
      data: assignments,
      reactiveData: true,
      columns: [
        {title: "Index", field:"index", editor:"input"},
        {title: "Name", field:"name", editor:"input"},
        {title: "Due date", field:"duedate", editor:"input"},
        {title: "Related lectures", field:"lectures", editor:"input"}
      ],
      dataEdited: (data) => {
        $.post({
          url: '/api/assignments',
          data: JSON.stringify(data),
          contentType: "application/json"
        });
      }
    });
  });});
