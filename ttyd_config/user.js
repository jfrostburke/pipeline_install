if (window.tty) {
  tty.on('open', function () {
    window.tty.socket.on('connect', function() {
      var w = new window.tty.Window();
      setTimeout(function () {
        w.maximize();
      }, 100);
    });
  });
}
