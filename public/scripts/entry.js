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

    let dialog = document.querySelector('dialog');

    $.ajax({
        url: '/api/v1/entry/' + entry
    }).done(e => {
        console.log(this);
        let thisRender = this;

        let rows = [];
        e.forEach(entry => {
            rows.push(
                '<tr class="entry-row"><td class="mdl-data-table__cell--non-numeric">' +
                    moment(entry.timestamp).format('MM月DD日 HH時') +
                    '</td><td>' + entry.rank + '</td><td>' +
                    '<a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-url="https://example.com" data-text="tweet_text" data-hashtags="アイカツ総選挙2019" data-related="kakakaya" data-show-count="false">Tweet</a>' +
                    '</td></tr >'
            );
        });
        $('#rows').append(rows);

        // window.twttr = (function(d, s, id) {
        //     var js, fjs = d.getElementsByTagName(s)[0],
        //         t = window.twttr || {};
        //     if (d.getElementById(id)) return t;
        //     js = d.createElement(s);
        //     js.id = id;
        //     js.src = "https://platform.twitter.com/widgets.js";
        //     fjs.parentNode.insertBefore(js, fjs);

        //     t._e = [];
        //     t.ready = function(f) {
        //         t._e.push(f);
        //     };

        //     return t;
        // }(document, "script", "twitter-wjs"));
    });

    $('.close').on('click', () => {
        dialog.close();
        $('#twitter-share-link').remove();
    });



    // let showDialogButton = document.querySelector('#show-dialog');

    // if (! dialog.showModal) {
    //     dialogPolyfill.registerDialog(dialog);
    // }
    // showDialogButton.addEventListener('click', function() {
    //     dialog.showModal();
    // });
}

render();
