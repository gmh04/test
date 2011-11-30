var map;


//SERVER_URL='http://localhost/srv/feed/'
SERVER_URL='/srv/feed/'

$(function() {

    // default location
    loc = {
        latitude: 55.950175,
        longitude: -3.187535
    }

    // try and get user location
    $.geolocation.find(function(location){
        loc = location;
    });

    // create map
    initMap(loc);

    // make panes resizeable
    $("#feed-wrapper").resizable({
        stop: function(event, ui) {
            var width = ($("html").width() - ui.size.width) - 40;
            $('#map').css('width', width);
        }
    });

  
});

function initMap(location){
    map = new OpenLayers.Map("map");
    map.addLayer(new OpenLayers.Layer.OSM());

    OpenLayers.Control.Hover = OpenLayers.Class(OpenLayers.Control, {
        defaultHandlerOptions: {
            'delay': 500,
            'pixelTolerance': null,
            'stopMove': false
        },

        initialize: function(options) {
            this.handlerOptions = OpenLayers.Util.extend(
                {}, this.defaultHandlerOptions
            );
            OpenLayers.Control.prototype.initialize.apply(
                this, arguments
            );
            this.handler = new OpenLayers.Handler.Hover(
                this,
                {'pause': this.onPause, 'move': this.onMove},
                this.handlerOptions
            );
        },

        onPause: function(e) {

            get_country(e, function(country){
                if(country){
                    if (!$('#country').length){
                        $('#map').prepend('<div id="country"></div>');
                    }

                    $('#country').text(country.name);
                }
            });
        },

        onMove: function(evt) {
            // if this control sent an Ajax request (e.g. GetFeatureInfo) when
            // the mouse pauses the onMove callback could be used to abort that
            // request.
        }
    });

    OpenLayers.Control.Click = OpenLayers.Class(OpenLayers.Control, {
        defaultHandlerOptions: {
            'single': true,
            'double': false,
            'pixelTolerance': 0,
            'stopSingle': false,
            'stopDouble': false
        },

        initialize: function(options) {
            this.handlerOptions = OpenLayers.Util.extend(
                {}, this.defaultHandlerOptions
            );
            OpenLayers.Control.prototype.initialize.apply(
                this, arguments
            );
            this.handler = new OpenLayers.Handler.Click(
                this, {
                    'click': this.trigger
                }, this.handlerOptions
            );
        },

        trigger: function(e) {
            get_country(e, function(country){
                if(country){
                    url = SERVER_URL + country.id;
                    var jqxhr = $.get(url, function(sources) {
                        $('#feed-content').html(sources);
                        $("#suggest-feed-form").submit(submitFeedSugestion);
                    });
                }
            });
        }
    });

    var hover = new OpenLayers.Control.Hover();
    map.addControl(hover);
    hover.activate();
    var click = new OpenLayers.Control.Click();
    map.addControl(click);
    click.activate();

    map.addControl(new OpenLayers.Control.PanZoomBar());

    map.setCenter(new OpenLayers.LonLat(loc.longitude, loc.latitude).transform(
        new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
        new OpenLayers.Projection("EPSG:900913") // to Spherical Mercator Projection
    ), 5);
}

// get country for a position on the map
function get_country(event, func){
    var country = {};
    var point = map.getLonLatFromViewPortPx(event.xy).transform(
        new OpenLayers.Projection("EPSG:900913"),
        new OpenLayers.Projection("EPSG:4326")
    );

    url='/geoencode/json?latlng=' + point.lat + ',' +  point.lon + '&sensor=false';
    var jqxhr = $.get(url, function(data) {
        if (data.status === 'OK'){
            if (data.results.length > 0){
                // take first result
                var ac = data.results[0].address_components;
                for (var i = 0; i < ac.length; i++){
                    if (ac[i].types[0] === 'country'){
                        country = {
                            'id': ac[i].short_name,
                            'name': ac[i].long_name
                        }

                        break;
                    }
                }

                func(country);
            }
        }
    });
}

function submitFeedSugestion(arg, arg2){
    console.log($('input[name="url"]').val());
    console.log($('#country').val());

    
    var url = SERVER_URL + 'suggest/' + $('#country').val() + '/?url=' + encodeURIComponent($('input[name="url"]').val());

    console.log('->');
    console.log( url);
    var jqxhr = $.get(url, function(result){
        //console.log('crivvens');
        $('#suggest-feed-response').html(result);
    });


    return false;
}