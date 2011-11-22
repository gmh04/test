var map;

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
    $("#right").resizable({
        stop: function(event, ui) {
            var width = ($("html").width() - ui.size.width) - 40;
            $('#map').css('width', width);
        }
    });

});

function get_feed(country){
    head = '<h2>Fetching for ' + country + '</h2>';
    wait = '<div id="loader"><img src="images/ajax-loader.gif"></img></div>'
    url = '/ms'

    //msg = '<p>' + ac[i].long_name + '</p>';
    $('#right-content').html(head);
    $('#right-content').append(wait);

    // $.get(url, function(data) {
    //     console.log(data);
    //     var title = data.find('channel');
    //     console.log(title);
    // });

    $.ajax({
	type: "GET",
	url: url,
	dataType: "xml",
	success: function(xml) {
            console.log('=>');
            console.log(xml);
            var channel = $(xml).find('channel');
            console.log(channel);
            //console.log($(channel.find('description'));
	    $(xml).find('channel').each(function(c){
                console.log(c);
                console.log($this);
            });
        }
    });


}

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
                    console.log(country);
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
                        //console.log('-->' + ac[i].long_name);
                        //country = ac[i].long_name;
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
