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
  /*
    
    swipeleft
        Triggers when a swipe event occurred moving in the left direction.
    swiperight
        Triggers when a swipe event occurred moving in the right direction.
        
    wip, needs t work with confirm location
    
    <script type="text/javascript">
      $(document).ready(
        function () {
          $("div:jqmData(role='page')").bind('pagecreate', $.london.locate);
        }
      );
    </script>
    
    <script type="text/javascript">
      $(document).ready(
        function () {
          var ll = new google.maps.LatLng(
            location.latitude, 
            location.longitude
          );
          var options = {
            'zoom': 14,
            //'disableDefaultUI': true,
            'center': ll,
            'mapTypeId': google.maps.MapTypeId.ROADMAP
          };
          var map = new google.maps.Map(target.get(0), options);
        }
      );
    </script>
    
  */
  'get_location': function (callback) {
    var location;
    var ll = $.cookie('ll');
    if (ll) {
      var parts = ll.split(',');
      location = {
        'latitude': parts[0],
        'longitude': parts[1]
      };
      callback(location);
    }
    else {
      $.london.locate(callback);
    }
  },
  'store_location': function (location) {
    $.cookie('ll', location.latitude + ',' + location.longitude);
  },
  'try_to_update_location': function () {
    $.geolocation.find($.london.store_location, function () {});
  },
  'locate': function (callback) {
    $.geolocation.find(
      function (location) {
        $.london.store_location(location);
        if (callback) {
          callback(location);
        }
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
