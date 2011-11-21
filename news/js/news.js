$(function() {
    map = new OpenLayers.Map("map");
    map.addLayer(new OpenLayers.Layer.OSM());
    loc = {
        latitude: 55.950175,
        longitude: -3.187535
    }

    $.geolocation.find(function(location){
        loc = location;
    }, function(){
        //alert("Your device doesn't support jquery.geolocation.js");
    });

    $("#right").resizable({
        stop: function(event, ui) {
            var width = ($("html").width() - ui.size.width) - 40;
            $('#map').css('width', width);
        }
    });

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
            var loc = map.getLonLatFromViewPortPx(e.xy).transform(
                new OpenLayers.Projection("EPSG:900913"),
                new OpenLayers.Projection("EPSG:4326")
            );

            url='/geoencode/json?latlng=' + loc.lat + ',' +  loc.lon + '&sensor=false';

            var jqxhr = $.get(url, function(data) {
                if (data.status === 'OK'){
                    if (data.results.length > 0){
                        var ac = data.results[0].address_components;
                        for (var i = 0; i < ac.length; i++){
                            if (ac[i].types[0] === 'country'){
                                //get_feed( ac[i].long_name);
                                console.log(ac[i].long_name);
                                //msg = '<p>' + ac[i].long_name + '</p>';
                                $('#country').html(ac[i].long_name);
                                //$('#right').css('border', 'solid red 1px');
                            }
                        }
                    }
                }
            })
        },
        
        onMove: function(evt) {
            // if this control sent an Ajax request (e.g. GetFeatureInfo) when
            // the mouse pauses the onMove callback could be used to abort that
            // request.
        }
    });

    controls = {
        'long': new OpenLayers.Control.Hover({
            handlerOptions: {
                'delay': 500
            }
        }),
    }

    for(var key in controls) {
        control = controls[key];
        // only to route output here
        control.key = key;
        map.addControl(control);
        control.activate();
    }

    map.setCenter(new OpenLayers.LonLat(loc.longitude, loc.latitude).transform(
        new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
        new OpenLayers.Projection("EPSG:900913") // to Spherical Mercator Projection
    ), 5);
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