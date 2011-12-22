var map;

var doHover = true;

SERVER_URL='/srv'

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

    var offset = 69;
    $('#main').css('height', $(window).height() - ($('#header').height() + $('#footer').height() + offset));
    var h = $(window).height() - ($('#header').height() + $('#footer').height() + offset);
    $('#feed').css('max-height', h + 'px');
    $('#map').css('height', '100%');

    // create map
    initMap(loc);

    $('.article-remove').live('click', function(event){
        console.log( $(this).parent().attr('id'));
        var id = $(this).parent().attr('id');
        $('#' + id).slideUp('slow');
    });

    $('#login-btn').live('click', function(e){
        // cancel the link behavior
        e.preventDefault();

        //Get the screen height and width
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();

        //Set height and width to mask to fill up the whole screen
        $('#mask').css({'width':maskWidth,'height':maskHeight});

        //transition effect
        $('#mask').fadeIn(1000);
        $('#mask').fadeTo("slow", 0.8);

        //Get the window height and width
        var winH = $(window).height();
        var winW = $(window).width();

        //Set the popup window to center
        $('#dialog').css('top',  winH/2-$('#dialog').height()/2);
        $('#dialog').css('left', winW/2-$('#dialog').width()/2);

        $("#dialog").show();

        //transition effect
        $("#dialog").fadeIn(1000);
        $('#username').focus();

    });

    //if close button is clicked
    $('.window .close').click(function (e) {
        //Cancel the link behavior
        e.preventDefault();
        $('#mask, .window').hide();
    });

    //if mask is clicked
    $('#mask').click(function () {
        $(this).hide();
        $('.window').hide();
    });

    $('.news-visibility').click(function () {
        $('#edit-btn').toggle();
        $('#view-btn').toggle();
    });

    $('#view-btn').hide();

    var e,
    a = /\+/g,  // Regex for replacing addition symbol with a space
    r = /([^&=]+)=?([^&]*)/g,
    d = function (s) { return decodeURIComponent(s.replace(a, " ")); },
    q = window.location.search.substring(1);

    var country, source;
    while (e = r.exec(q)){
        //rams[d(e[1])] = d(e[2]);
        //console.log(d(e[1]) + ' : '  +  d(e[2]));
        if (d(e[1]) === 'source'){
            source = d(e[2]);
        }
        else if(d(e[1]) === 'country'){
            country = d(e[2]);
        }
    }

    if (country !== undefined && source !== undefined){
        console.log('=>');
        editSource(country, source);
    }
});

// get country for a position on the map
function get_country(event, func){
    var selection = {};
    var point = map.getLonLatFromViewPortPx(event.xy).transform(
        new OpenLayers.Projection("EPSG:900913"),
        new OpenLayers.Projection("EPSG:4326")
    );

    url='/geoencode/json?latlng=' + point.lat + ',' +  point.lon + '&sensor=false';
    var jqxhr = $.get(url, function(data) {
        if (data.status === 'OK'){
            if (data.results.length > 0){
                country = data.results[data.results.length - 1];
                selection['id'] = country.address_components[0].short_name;
                selection['name'] = country.address_components[0].long_name;

                region = data.results[data.results.length - 2];
                selection['region'] = region.address_components[0].short_name;

                func(selection);
            }
        }
    });
}

function closeArticle(country, source_id){
    console.log(s);
    console.log(s);
}

function editSource(country, source){
    url = '/feed/edit/' + country + '/' + source;
    $.get(url, function(sources) {
        $('#feed-content').css('overflow-y','hidden');
        $('#feed-content').html(sources);
        $('#feed-content').trigger("create");
    });
}

function submitFeedSugestion(){
    var feed_url = $(this).find('input[name="url"]').val();

    if (feed_url.length > 0) {
        var data = {
            'url': feed_url
        }
        $.mobile.showPageLoadingMsg();
        $.ajax({
            url: this.action,
            data: data,
            success: function(response){
                $('#suggest-feed-response').html(response);
                $.mobile.hidePageLoadingMsg();
            },
            //dataType: dataType
            error: function(response) {
                $('#suggest-feed-response').html(response);
                $.mobile.hidePageLoadingMsg();
            },
            headers: {
                'X-CSRFToken': $(this).find('input[name="csrfmiddlewaretoken"]').val(),
            },
        });
    }
    else{
        response = 'Invalid URL';
    }

    return false;
}

function enableHover(enableHover){
    doHover = enableHover;
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
            console.log('hover ' + doHover);
            if(doHover){
                get_country(e, function(country){
                    if(country){
                        var text;
                        if(country.region === undefined){
                            text = country.name;
                        }
                        else{
                            text = country.region + ", " +  country.name;
                        }

                        $('#header h1').text(text);
                    }
                });
            }
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
            doHover = false;
            $.mobile.showPageLoadingMsg();
            get_country(e, function(country){
                if(country){
                    if($('#view-btn').is(":visible")){
                        url = '/feed/edit/' + country.id;
                    }
                    else{
                        url = '/feed/' + country.id;
                    }
                    $.get(url, function(sources) {
                        $('#feed-content').html(sources).trigger('create');
                        $("#suggest-feed-form").submit(submitFeedSugestion);
                        doHover = true;
                        $.mobile.hidePageLoadingMsg();
                    });
                }
            });

            //$.mobile.hidePageLoadingMsg()
        }
    });

    var hover = new OpenLayers.Control.Hover();
    map.addControl(hover);
    hover.activate();
    var click = new OpenLayers.Control.Click();
    map.addControl(click);
    click.activate();

    //map.addControl(new OpenLayers.Control.LayerSwitcher());

    map.addControl(new OpenLayers.Control.PanZoomBar());

    map.setCenter(new OpenLayers.LonLat(loc.longitude, loc.latitude).transform(
        new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
        new OpenLayers.Projection("EPSG:900913") // to Spherical Mercator Projection
    ), 5);
}
