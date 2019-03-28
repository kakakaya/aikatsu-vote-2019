function render() {
    let path = window.location.pathname.split("/");
    let entry = decodeURI(path[path.length - 1]);

    if (entry === "霧矢あおい") {
        $('h1#entry').text(entry + 'さん');
    } else if (entry === "藤堂ユリカ") {
        $('h1#entry').text(entry + '様');
    }
    $.ajax('/api/v1/entry/' + entry).done(e => {
        let rows = [];
        e.forEach(entry => {
            rows.push(
                '<tr><td class="mdl-data-table__cell--non-numeric">' +
                moment(entry.timestamp).format('MM月DD日 HH時') +
                '</td><td>' + entry.rank + '</td></tr>'
            );
        });
        $('#rows').append(rows);
    });
}

render();
