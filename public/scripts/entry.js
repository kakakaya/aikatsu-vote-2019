function render() {
    let path = window.location.pathname.split("/");
    let entry = decodeURI(path[path.length - 1]);

    if (entry === "霧矢あおい") {
        $('h1#entry').text(entry + 'さん');
    } else if (entry === "藤堂ユリカ") {
        $('h1#entry').text(entry + '様');
    } else {
        $('h1#entry').text(entry);
    }

    $.ajax({
        url: '/api/v1/entry/' + entry
    }).done(e => {
        let rankingLog = {};
        e.forEach(entry => {
            let entry_date = moment(entry.timestamp);
            let date_str = entry_date.format('YYYY-MM-DD');
            let hour_str = entry_date.format('H');

            if (!rankingLog.hasOwnProperty(date_str)) {
                rankingLog[date_str] = {};
            }
            rankingLog[date_str][hour_str] = entry;
        });
        let days = Object.keys(rankingLog);
        days.sort().reverse();

        days.forEach(e => {
            let thead = '<thead>' + '<th class="mdl-data-table__cell--non-numeric">' + (moment(e).format('MM月DD日')) + '</th>' + '</thead>';

            let rows = '';
            console.log(rankingLog[e]);
            for (var i = 0; i < 24; i++) {
                let entry = rankingLog[e][i];
                if (entry === undefined) {
                    entry = {
                        rank: '？',
                        name: '？取得失敗',
                    };
                }
                console.log(entry);

                rows += '<tr>' +
                    '<td class="mdl-data-table__cell--non-numeric">' +
                    ('0' + i).slice(1) + '時'+
                    '</td><td class="mdl-data-table__cell--non-numeric">' +
                    (entry.rank==='？'?entry.rank:entry.rank+1) + '位' +
                    '</td><td class="mdl-data-table__cell--non-numeric">' +
                    entry.name.slice(1) +
                    '</td>' +
                    '</tr>';
            }

            let tbody = '<tbody>' + rows + '</tbody>';
            let table = '<table class="mdl-data-table mdl-js-data-table mdl-shadow--2dp">' + thead + tbody + '</table>';
            $("#container").append(table);

        });

    });
}

render();
