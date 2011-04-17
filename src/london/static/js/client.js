$(document).bind(
  'mobileinit', 
  function () {
    $.extend(
      $.mobile, {
        'loadingMessage': 'Loading ...'
      }
    );
  }
);

$.london = {
  'store_location': function (location) {
    $.cookie('ll', location.latitude + ',' + location.longitude);
  },
  'try_to_update_location': function () {
    $.geolocation.find($.london.store_location, function () {});
  },
  'locate': function () {
    $.geolocation.find(
      function (location) {
        $.london.store_location(location);
        window.setInterval(
          function () {
            $.london.try_to_update_location();
          },
          45000
        );
      },
      function () {
        $.mobile.changePage("/confirmlocation/", "pop");
      }
    );
  }
};

$(document).ready(
  function (){
    $.london.locate();
  }
);
