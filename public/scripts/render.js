var RssBox = React.createClass({
  loadRssFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    this.loadRssFromServer();
    setInterval(this.loadRssFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="rssBox">
        <h1 className="siteTitle">GIGAZINE RSS</h1>
        <RssList data={this.state.data} />
      </div>
    );
  }
});

var RssList = React.createClass({
  render: function() {
    var rssNodes = this.props.data.map(function (rss) {
      return (
        <div className="rss" key={rss.id}>
          <h3 className="title">
            <a href={rss.link}>
              {rss.title}
            </a>
          </h3>
          <p className="updated">{rss.updated}</p>
          <p className="summary">{rss.summary}</p>
        </div>
      );
    });
    return (
      <div className="rssList">
        {rssNodes}
      </div>
    );
  }
});

ReactDOM.render(
  <RssBox url="/api/rss" pollInterval={2000000} />,
  document.getElementById('content')
);
