(function() {
  /*

    Mobile London Guide `Coffeescript`_ client.

    .. _`Coffeescript`: http://jashkenas.github.com/coffee-script/


  */  var Location, central_london, doc, handle, location;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  central_london = {
    latitude: 51.5001524,
    longitude: -0.1262362
  };
  Location = (function() {
    /* Encapsulates location detection and storage.
    */    function Location(location, timeout, delay) {
      var _ref;
      this.location = location;
      this.timeout = timeout;
      this.delay = delay != null ? delay : 60000;
      /* ``@location`` will be null unless passed in or already set in the
        'll' session cookie.
      */
      this.location = (_ref = this.location) != null ? _ref : jQuery.cookie('ll');
      this.initial_delay = this.delay;
    }
    Location.prototype.update = function() {
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
    Location.prototype.schedule_update = function() {
      /* Queue up a call to update.
      */      return this.timeout = setTimeout(__bind(function() {
        return this.update();
      }, this), this.delay);
    };
    Location.prototype.store = function(location) {
      /* Store ``location`` as ``this.location`` and in the 'll' cookie.
      */      console.log('location', location);
      this.location = location;
      return $.cookie('ll', "" + location.latitude + "," + location.longitude);
    };
    Location.prototype.locate = function(callback, prompt_on_failure) {
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
          return jQuery.mobile.changePage('/nolocation/', 'pop');
        }
      });
    };
    return Location;
  })();
  location = new Location(central_london);
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
      */      var pages;
      location.locate();
      pages = jQuery('div:jqmData(role="page")');
      return pages.live('pagebeforecreate', function(event) {
        return handle.pageinserted(event);
      });
    },
    pageinserted: function(event) {
      /* Handle a new page being inserted into the DOM.
      */      var ll, loc, map, node, options, page, path, target;
      page = jQuery(event.target);
      path = page.jqmData('url');
      console.log(path);
      if (path === '/nolocation/') {
        target = jQuery('#try-again');
        return target.click(function() {
          location.locate();
          page.dialog('close');
          return false;
        });
      } else if (path.match(/\/categories\/\w*\/map\//)) {
        target = jQuery('#map');
        node = target.get(0);
        loc = location.location;
        ll = new google.maps.LatLng(loc.latitude, loc.longitude);
        options = {
          zoom: 13,
          center: ll,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        return map = new google.maps.Map(node, options);
        /*

          @@:

          - size the map
          - respond to resizes
          - demand location (do a get_location with callback rather than default)
            also perhaps force the user to choose location from a map rather than
            default to central london?
          - parse places out of the page, onto the map
          - icons
          - info windows


        */
      }
    }
  };
  doc = jQuery(document);
  doc.bind('mobileinit', function() {
    return doc.ready(handle.ready);
  });
}).call(this);
