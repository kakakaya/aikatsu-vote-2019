function render() {
    $.ajax('/api/v1/history').done(e => {
        let rankingLog = {};
        e.forEach(entry => {
            if (!rankingLog.hasOwnProperty(entry.timestamp)) {
                rankingLog[entry.timestamp] = [];
            }
            rankingLog[entry.timestamp][entry.rank - 1] = entry.name;
            // tables.push(
            //     '<thead>' +
            //     '<tr>' +
            //     '<tr><td class="mdl-data-table__cell--non-numeric">' +
            //     moment(entry.timestamp).format('MM月DD日 HH時') +
            //     '</td><td>' + entry.rank + '</td></tr>'
            // )
        });
        let times = Object.keys(rankingLog);
        times.sort().reverse();

        // let thead = [];
        // let tbody = [];


        times.forEach(e => {
            let thead = '<thead>' + '<th class="mdl-data-table__cell--non-numeric">' + (moment(e).format('MM月DD日 HH時')) + '</th>' + '</thead>';

            let rows = '';
            console.log(rankingLog[e]);
            rankingLog[e].forEach((entry, rank)=> {
                rows += '<tr><td class="mdl-data-table__cell--non-numeric">' +
                    (rank+1) + '位' + entry.slice(1) +
                    '</td></tr>';

            });

            let tbody = '<tbody>' + rows + '</tbody>';
            let table = '<table class="mdl-data-table mdl-js-data-table mdl-shadow--2dp">'+thead + tbody+'</table>';
            $("#container").append(table);

        });


        // <thead>
        // <tr>
        // <th class="mdl-data-table__cell--non-numeric">時刻</th>
        // <th>順位</th>
        // </tr>
        // </thead>
        // <tbody id="rows">
        // </tbody>
        // $('#tables').append(tables);
    });
}

render();
