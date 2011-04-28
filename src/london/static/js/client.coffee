#!/usr/local/bin coffee
# -*- coding: utf-8 -*-

### 
  
  Mobile London Guide `Coffeescript`_ client.
  
  .. _`Coffeescript`: http://jashkenas.github.com/coffee-script/
  
  
###

central_london =
    latitude: 51.5001524
    longitude: -0.1262362

class Location
    ### Encapsulates location detection and storage.
    ###
    
    constructor: (@location, @timeout, @delay=60000) ->
        ### ``@location`` will be null unless passed in or already set in the
          'll' session cookie.
        ###
        
        this.location = @location ? jQuery.cookie 'll'
        this.initial_delay = @delay
    
    update: ->
        ### Tries to fetch and store an updated location.
          If the location can't be got, backs off slowly.
        ###
        
        $.geolocation.find (location) => 
            this.store location
            if this.delay > this.initial_delay
                this.delay = this.initial_delay 
            this.schedule_update()
        , =>
            if this.delay < this.initial_delay * 5
                this.delay += this.delay
            this.schedule_update()
        
        
    
    schedule_update: ->
        ### Queue up a call to update.
        ###
        
        this.timeout = setTimeout => 
            this.update()
        , this.delay
        
    
    store: (location) ->
        ### Store ``location`` as ``this.location`` and in the 'll' cookie.
        ###
        
        console.log 'location', location
        
        this.location = location
        $.cookie 'll', "#{location.latitude},#{location.longitude}"
        
    
    locate: (callback, prompt_on_failure=true) ->
        ### Try to get the user's location.  If we can, store it and
          optionally call the callback with it. If we can't, display
          the no location dialog.
        ###
        
        clearTimeout this.timeout if this.timeout?
        
        $.geolocation.find (location) =>
            this.store location
            this.schedule_update()
            if callback?
                callback location 
        , ->
            if prompt_on_failure
                jQuery.mobile.changePage '/nolocation/', 'pop'
            
        
        
    

location = new Location central_london

handle = 
    ### Event handlers.
    ###
    
    ###
      
      @@:
      
      - swipeleft
          Triggers when a swipe event occurred moving in the left direction.
      - swiperight
          Triggers when a swipe event occurred moving in the right direction.
      
    ###
    
    ready: ->
        ### Handle the application loading into the browser for the first time.
        ###
        
        # detect the user's location
        location.locate()
        
        # listen for page inserted events
        pages = jQuery 'div:jqmData(role="page")'
        pages.live 'pagebeforecreate', (event) -> handle.pageinserted event
        
    
    pageinserted: (event) ->
        ### Handle a new page being inserted into the DOM.
        ###
        
        page = jQuery event.target
        path = page.jqmData 'url'
        
        console.log path
        
        if path is '/nolocation/'
            target = jQuery '#try-again'
            target.click ->
                location.locate()
                page.dialog 'close'
                return false
        else if path.match(/\/categories\/\w*\/map\//)
            target = jQuery '#map'
            node = target.get 0
            loc = location.location
            ll = new google.maps.LatLng loc.latitude, loc.longitude
            options =
                zoom: 13
                center: ll
                mapTypeId: google.maps.MapTypeId.ROADMAP
            map = new google.maps.Map node, options
            
            ###
              
              @@:
              
              - size the map
              - respond to resizes
              - demand location (do a get_location with callback rather than default)
                also perhaps force the user to choose location from a map rather than
                default to central london?
              - parse places out of the page, onto the map
              - icons
              - info windows
            
            
            ###
            
        
    
    

doc = jQuery document
doc.bind 'mobileinit', -> doc.ready handle.ready

