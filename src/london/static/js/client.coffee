#!/usr/local/bin coffee
# -*- coding: utf-8 -*-

### 
  
  Mobile London Guide `Coffeescript`_ client.
  
  .. _`Coffeescript`: http://jashkenas.github.com/coffee-script/
  
  
###

$ = jQuery

locations =
    central_london:
        title: 'Central London'
        location: new google.maps.LatLng(
            51.5001524, 
            -0.1262362
        )
    


class Locater
    ### Encapsulates location detection and storage.
    ###
    
    constructor: (@location, @timeout, @delay=60000) ->
        this.initial_delay = @delay
        
    
    update: ->
        ### Tries to fetch and store an updated location.
          If the location can't be got, backs off slowly.
        ###
        
        $.geolocation.find(
            (location) => 
                this.store(location)
                if this.delay > this.initial_delay
                    this.delay = this.initial_delay 
                this.schedule_update()
            , => 
                if this.delay < this.initial_delay * 5
                    this.delay += this.delay
                this.schedule_update()
        )
        
    
    schedule_update: ->
        ### Queue up a call to update.
        ###
        
        this.timeout = setTimeout(
            => this.update(),
            this.delay
        )
        
    
    store: (location) ->
        ### Store ``location`` as ``this.location`` and in the 'll' cookie.
        ###
        
        console.log('store location', location)
        
        this.location = new google.maps.LatLng(
            location.latitude,
            location.longitude
        )
        
        $.cookie('ll', "#{location.latitude},#{location.longitude}")
        
    
    locate: (callback, prompt_on_failure=true) ->
        ### Try to get the user's location.  If we can, store it and
          optionally call the callback with it. If we can't, display
          the no location dialog.
        ###
        
        if this.timeout?
            clearTimeout(this.timeout)
        
        $.geolocation.find(
            (location) => 
                this.store(location)
                this.schedule_update()
                if callback?
                    callback(location)
            , ->
                if prompt_on_failure
                    $.mobile.changePage('/nolocation/', 'pop')
        )
        
    
    

locater = new Locater(locations.central_london.location)

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
        ll = $.cookie('ll')
        if ll
            parts = ll.split(',')
            location =
                latitude: parts[0]
                longitude: parts[1]
            locater.store(location)
        else
            locater.locate()
        
        # listen for page inserted events
        pages = $('div:jqmData(role="page")')
        pages.live(
            'pagebeforecreate', 
            (event) -> handle.pageinserted(event)
        )
        
    
    pageinserted: (event) ->
        ### Handle a new page being inserted into the DOM.
        ###
        
        page = $(event.target)
        path = page.jqmData('url')
        
        if path is '/nolocation/'
            $('#try-again').click(
                ->
                    location.locate()
                    page.dialog('close')
                    return false
            )
        else if path.match(/\/categories\/\w*\/map\//)
            target = $('#map')
            options =
                center: locater.location
                mapTypeId: google.maps.MapTypeId.ROADMAP
                zoom: 13
            map = new google.maps.Map(target.get(0), options)
            ###
              
              - size the map
              - respond to resizes
              - parse places out of the page, onto the map
              - icons
              - info windows
              
              
            ###
        
    

$(document).bind(
    'mobileinit', 
    -> $(document).ready(handle.ready)
)
