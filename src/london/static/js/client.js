(function() {
  /*

    Mobile London Guide `Coffeescript`_ client.

    .. _`Coffeescript`: http://jashkenas.github.com/coffee-script/


  */  var $, Locater, handle, locater, locations;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  $ = jQuery;
  locations = {
    central_london: {
      title: 'Central London',
      latlng: new google.maps.LatLng(51.5001524, -0.1262362)
    }
  };
  Locater = (function() {
    /* Encapsulates location detection and storage.
    */    function Locater(latlng, timeout, delay) {
      this.latlng = latlng;
      this.timeout = timeout;
      this.delay = delay != null ? delay : 60000;
      this.initial_delay = this.delay;
    }
    Locater.prototype.update = function() {
      /* Tries to fetch and store an updated location.
        If the location can't be got, backs off slowly.
      */      return $.geolocation.find(__bind(function(location) {
        this.store(location);
        if (this.delay > this.initial_delay) {
          this.delay = this.initial_delay;
        }
        return this.schedule_update();
      }, this), __bind(function() {
        if (this.delay < this.initial_delay * 5) {
          this.delay += this.delay;
        }
        return this.schedule_update();
      }, this));
    };
    Locater.prototype.schedule_update = function() {
      /* Queue up a call to update.
      */      return this.timeout = setTimeout(__bind(function() {
        return this.update();
      }, this), this.delay);
    };
    Locater.prototype.store = function(location) {
      /* Store ``location`` as ``this.latlng`` and in the 'll' cookie.
      */      console.log('store location', location);
      this.latlng = new google.maps.LatLng(location.latitude, location.longitude);
      return $.cookie('ll', "" + location.latitude + "," + location.longitude);
    };
    Locater.prototype.locate = function(callback, prompt_on_failure) {
      if (prompt_on_failure == null) {
        prompt_on_failure = true;
      }
      /* Try to get the user's location.  If we can, store it and
        optionally call the callback with it. If we can't, display
        the no location dialog.
      */
      if (this.timeout != null) {
        clearTimeout(this.timeout);
      }
      return $.geolocation.find(__bind(function(location) {
        this.store(location);
        this.schedule_update();
        if (callback != null) {
          return callback(location);
        }
      }, this), function() {
        if (prompt_on_failure) {
          return $.mobile.changePage('/nolocation/', 'pop');
        }
      });
    };
    return Locater;
  })();
  locater = new Locater(locations.central_london.latlng);
  handle = {
    /* Event handlers.
        */
    /*

          @@:

          - swipeleft
              Triggers when a swipe event occurred moving in the left direction.
          - swiperight
              Triggers when a swipe event occurred moving in the right direction.

        */
    ready: function() {
      /* Handle the application loading into the browser for the first time.
      */      var ll, location, pages, parts;
      ll = $.cookie('ll');
      if (ll) {
        parts = ll.split(',');
        location = {
          latitude: parts[0],
          longitude: parts[1]
        };
        locater.store(location);
      } else {
        locater.locate();
      }
      pages = $('div:jqmData(role="page")');
      return pages.live('pagebeforecreate', function(event) {
        return handle.pageinserted(event);
      });
    },
    pageinserted: function(event) {
      /* Handle a new page being inserted into the DOM.
      */      var map, options, page, path, target;
      page = $(event.target);
      path = page.jqmData('url');
      if (path === '/nolocation/') {
        return $('#try-again').click(function() {
          location.locate();
          page.dialog('close');
          return false;
        });
      } else if (path.match(/\/categories\/\w*\/map\//)) {
        target = $('#map');
        options = {
          center: locater.latlng,
          mapTypeId: google.maps.MapTypeId.ROADMAP,
          zoom: 13
        };
        return map = new google.maps.Map(target.get(0), options);
        /*

          - size the map
          - respond to resizes
          - parse places out of the page, onto the map
          - icons
          - info windows


        */
      }
    }
  };
  $(document).bind('mobileinit', function() {
    return $(document).ready(handle.ready);
  });
}).call(this);
