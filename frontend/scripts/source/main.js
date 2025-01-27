;
(function($, window, document, undefined) {
    "use strict";
    var $win = $(window);
    var $doc = $(document);

    window.Component = window.Component || {};
    window.Helpers = window.Helpers || {};

    /* ------------------------------------------------------------ *\
    	#FUNCTION DEFINITIONS
    \* ------------------------------------------------------------ */

    /**
     * Create a function that only can be called once every 400 ms.
     *
     * Example:
     * var df = debounce(function() {
     * 		... func body ...
     * }, 500)
     *
     * @public
     * @param  {function}
     * @param  {number}
     * @return {function}
     */
    Helpers.debounce = function(fn, wait) {
        var timeout;

        return function() {
            var ctx = this,
                args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                fn.apply(ctx, args);
            }, wait || 100);
        };
    };
    /**
     * Get input form multiple fields, send ajax request with key phase parameter to backend and display result.
     *
     * @public
     * @return {Object} All public methods
     */
    Helpers.autocomplete = (function() {
        var options = {
            $searchFields: null,
            $searchResults: null,
            url: null,
            classNames: {
                active: 'has-flag'
            }
        };

        function _init(url) {
            options.$searchFields = $('.form-search input');
            options.$searchResults = $('.js-search-results');
            options.url = url;
            // stop execution when elements does missing
            if (!options.$searchFields.length || !options.$searchResults.length) {
                return;
            }

            _handleEvents();
        }

        function _handleEvents() {
            // type and focus on field
            options.$searchFields.on('keyup focusin', function() {
                var currentValue = $(this).val();

                if (currentValue.length > 1) {
                    _getSearchResultsDebounced(currentValue);
                } else {
                    _clean();
                }
            });

            // click outside and esc press
            $doc.on('click keyup touchstart', function(e) {
                var $target = $(e.target);
                var keyEsc = 27;

                if ((!$target.closest(options.$searchResults).length) || (e.keyCode == keyEsc)) {
                    _clean();
                }
            });
        }

        var _getSearchResultsDebounced = Helpers.debounce(function(value) {
            _getSearchResults(value);
        }, 400);

        function _getSearchResults(query) {
            var q = query;

            $.ajax({
                url: '../../ajax/search.json',
                type: 'POST',
                dataType: 'json',
                data: { query: q },
                success: function(result) {
                    if (result.success) {
                        _render(result);
                    }
                }
            });
        }

        function _render(data) {
            _clean();

            options.$searchResults.each(function() {
                var $this = $(this);

                $this.addClass(options.classNames.active);
                $this.append(data.html);
            });
        }

        function _clean() {
            options.$searchResults.each(function() {
                var $this = $(this);

                $this.removeClass(options.classNames.active);
                $this.html('');
            });
        }

        return {
            init: function(url) {
                _init(url);
            }
        };
    })();

    /**
     * Create Google map with panTo function.
     *
     * https://developers.google.com/maps/documentation/javascript/tutorial
     *
     * TODO:
     * - refactor functions
     * - advanced validation
     */
    Component.GoogleMap = (function() {
        var $mapHolder = null;
        var map = null;
        var locations = [];
        var pin = {
            src: $('.js-map-location').attr('data-pin'),
            x: 40,
            y: 40
        };
        var tooltips = true;
        var config = {};
        var markers = [];

        function _init(configuration) {
            config = $.extend(true, {}, config, configuration);
            _validateInput();
        }

        function _validateInput() {
            if (typeof google !== 'object') {
                console.error('Component.GoogleMap: Please link Google Maps API!');
                console.error('Component.GoogleMap: Stop execution!');
                return false;
            }
            if (!config.$mapHolder.length) {
                console.error('Component.GoogleMap: Map element missing!');
                console.error('Component.GoogleMap: Stop execution!');
                return false;
            }
            if (!config.locations.length) {
                console.error('Component.GoogleMap: Require array with all the locations!');
                console.error('Component.GoogleMap: Stop execution!');
                return false;
            }
            _cacheConfig();
        }

        function _cacheConfig() {
            $mapHolder = config.$mapHolder;
            locations = config.locations;

            if (typeof config.pin !== 'undefined') {
                pin = config.pin;
            }
            if (typeof config.tooltips !== 'undefined') {
                tooltips = config.tooltips;
            }
            _createMap();
        }

        function _createMarker(location) {
            var latLng = new google.maps.LatLng(location[0], location[1]);
            var infoWindow = new google.maps.InfoWindow();
            var marker = new google.maps.Marker({
                position: latLng,
                map: map,
                animation: google.maps.Animation.DROP,
                // icon: {
                //  url: pin.src,
                //  scaledSize: pinSize,
                //  // pin point position
                //  // anchor: new google.maps.Point(23, 64)
                // }
            });
            markers.push(marker);
            if (typeof config.tooltips !== 'undefined') {
                tooltips = config.tooltips;
            }
            // if (tooltips) {
            //  google.maps.event.addListener(marker, 'click', function() {
            //      infoWindow.close(); // close previously opened infowindow
            //      infoWindow.setContent('<div class="map-tooltip">' + location[2] + '</div>');
            //      infoWindow.open(map, marker);
            //      var iwOuter = $('.gm-style-iw');
            //      /* Since this div is in a position prior to .gm-div style-iw.
            //       * We use jQuery and create a iwBackground variable,
            //       * and took advantage of the existing reference .gm-style-iw for the previous div with .prev().
            //      */
            //      var iwBackground = iwOuter.prev();
            //      iwBackground.addClass('popup-container');
            //      iwBackground.children(':nth-child(1)').addClass('pointer-border');
            //      iwBackground.children(':nth-child(3)').addClass('pointer');
            //      // Removes background shadow DIV
            //      iwBackground.children(':nth-child(2)').css({'display' : 'none'});
            //      // Removes white background DIV
            //      iwBackground.children(':nth-child(4)').css({'display' : 'none'});
            //      // Reference to the div that groups the close button elements.
            //      var iwCloseBtn = iwOuter.next();
            //      // Apply the desired effect to the close button
            //      iwCloseBtn.css({opacity: '1', right: '20px', top: '20px', border: '1px solid var(--color-secondary)', 'border-radius': '13px', 'box-shadow': '0 0 5px #3990B9'});
            //  });
            // }
            return marker;
        }

        function _createMap() {
            var mapStyles = [];
            var pinSize = new google.maps.Size(pin.x, pin.y);
            var mapSettings = {
                zoom: 10, // work only when there is one pin on the map
                center: locations ? new google.maps.LatLng(locations[0][0], locations[0][1]) : new google.maps.LatLng('42.6194', '25.3930'),
                scrollwheel: false,
                styles: mapStyles,
                disableDefaultUI: false,
                draggable: false,
                panControl: false,
                zoomControl: false,
                mapTypeControl: false,
                scaleControl: false,
                streetViewControl: false,
                overviewMapControl: false,
                fullscreenControl: false,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            var bounds = new google.maps.LatLngBounds();
            var infoWindow;
            var i;
            if (tooltips) {
                infoWindow = new google.maps.InfoWindow();
                // check for html in locations array
                try {
                    if (locations[0][2].length) {}
                } catch (e) {
                    console.warn('Component.GoogleMap: Requre html from locations array!');
                    tooltips = false;
                }
            }
            // Display a map on the page.
            map = new google.maps.Map(document.getElementById($mapHolder[0].id), mapSettings);

            function createMarker(location) {
                var latLng = location;
                var marker = new google.maps.Marker({
                    position: latLng,
                    map: map,
                    animation: google.maps.Animation.DROP,
                    icon: {
                        url: pin.src,
                        scaledSize: pinSize,
                        // pin point position
                        // anchor: new google.maps.Point(23, 64)
                    }
                });
                markers.push(marker);
                // if (tooltips) {
                //  google.maps.event.addListener(marker, 'click', function() {
                //      infoWindow.close(); // close previously opened infowindow
                //      infoWindow.setContent('<div class="map-tooltip">' + location[2] + '</div>');
                //      infoWindow.open(map, marker);
                //      var iwOuter = $('.gm-style-iw');
                //      /* Since this div is in a position prior to .gm-div style-iw.
                //       * We use jQuery and create a iwBackground variable,
                //       * and took advantage of the existing reference .gm-style-iw for the previous div with .prev().
                //      */
                //      var iwBackground = iwOuter.prev();
                //      iwBackground.addClass('popup-container');
                //      iwBackground.children(':nth-child(1)').addClass('pointer-border');
                //      iwBackground.children(':nth-child(3)').addClass('pointer');
                //      // Removes background shadow DIV
                //      iwBackground.children(':nth-child(2)').css({'display' : 'none'});
                //      // Removes white background DIV
                //      iwBackground.children(':nth-child(4)').css({'display' : 'none'});
                //      // Reference to the div that groups the close button elements.
                //      var iwCloseBtn = iwOuter.next();
                //      // Apply the desired effect to the close button
                //      iwCloseBtn.css({opacity: '1', right: '20px', top: '20px', border: '1px solid var(--color-secondary)', 'border-radius': '13px', 'box-shadow': '0 0 5px #3990B9'});
                //  });
                // }
            }
            createMarker(mapSettings.center);
            // // Create markers for all locations.
            // for (i = 0; i < locations.length; i++) {
            //  createMarker(locations[i]);
            // }
            // // Automatically center the map fitting all markers on the screen. Ignore zoom from settings.
            // if (locations.length > 1) {
            //  map.fitBounds(bounds);
            // }
            // var markerCluster = new MarkerClusterer(map, markers, {
            //  imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
            // });
        }

        function _switchLocation(lat, lng, content) {
            markers.map(function(k, v) {
                k.setMap(null);
            });
            markers = [];
            map.panTo({
                lat: Number(lat),
                lng: Number(lng)
            });
            // _createMarker([Number(lat),Number(lng)]);
            _showTooltip(_createMarker([Number(lat), Number(lng)]), map, content);
        }

        function _showTooltip(marker, map, content) {
            if (tooltips) {
                var infoWindow = new google.maps.InfoWindow();
                infoWindow.close(); // close previously opened infowindow
                infoWindow.setContent('<div class="map-tooltip">' + content + '</div>');
                infoWindow.open(map, marker);
                var iwOuter = $('.gm-style-iw');
                /* Since this div is in a position prior to .gm-div style-iw.
                 * We use jQuery and create a iwBackground variable,
                 * and took advantage of the existing reference .gm-style-iw for the previous div with .prev().
                 */
                var iwBackground = iwOuter.prev();
                iwBackground.addClass('popup-container');
                iwBackground.children(':nth-child(1)').addClass('pointer-border');
                iwBackground.children(':nth-child(3)').addClass('pointer');
                // Removes background shadow DIV
                iwBackground.children(':nth-child(2)').css({ 'display': 'none' });
                // Removes white background DIV
                iwBackground.children(':nth-child(4)').css({ 'display': 'none' });
                // Reference to the div that groups the close button elements.
                var iwCloseBtn = iwOuter.next();
                // Apply the desired effect to the close button
                iwCloseBtn.css({ opacity: '1', right: '20px', top: '20px', border: '1px solid var(--color-secondary)', 'border-radius': '13px', 'box-shadow': '0 0 5px #3990B9' });
                // infoWindow.open();
            }
        }

        function _panTo(lat, lng) {
            // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
            // var boundsListener = google.maps.event.addListener(map, 'bounds_changed', function(event) {
            //  this.setZoom(15);
            //  google.maps.event.removeListener(boundsListener);
            // });
            map.panTo({
                lat: Number(lat),
                lng: Number(lng)
            });
            _createMarker([Number(lat), Number(lng)]);
        }
        return {
            init: function(configuration) {
                _init(configuration);
            },
            panTo: function(lat, lng) {
                _panTo(lat, lng);
            },
            switchLocation: function(lat, lng, content) {
                _switchLocation(lat, lng, content);
            },
            getMarkers: function() {
                return markers;
            }
        };
    })();

    //UNIFY CLUMNS V1 REALLY BUGGY
    // function unifyCols() {
    // $('.row').each(function(){
    // 	$(this).css('height', $(this).height());
    // 		$(this).children('.col').css('height', 'inherit');
    // 	});
    // }

    //UNIFY CLUMNS V2 NOT THAT BUGGY BUT STILL BUGGY
    function unifyCols() {
        function unify() {
            $('.row').each(function() {
                $(this).css('height', $(this).height());
                $(this).children('.col').css('height', 'inherit');
            });
        }

        unify();
        $(window).resize(unify);
    }

    Component.GoogleMap = (function() {
        var $mapHolder = null;
        var map = null;
        var locations = [];
        var pin = {
            src: $('.js-map-location').attr('data-pin'),
            x: 40,
            y: 40
        };
        var tooltips = false;
        var config = {};
        var markers = [];

        function _init(configuration) {
            config = $.extend(true, {}, config, configuration);

            _validateInput();
        }

        function _validateInput() {
            if (typeof google !== 'object') {
                console.error('Component.GoogleMap: Please link Google Maps API!');
                console.error('Component.GoogleMap: Stop execution!');
                return false;
            }

            if (!config.$mapHolder.length) {
                console.error('Component.GoogleMap: Map element missing!');
                console.error('Component.GoogleMap: Stop execution!');
                return false;
            }

            if (!config.locations.length) {
                console.error('Component.GoogleMap: Require array with all the locations!');
                console.error('Component.GoogleMap: Stop execution!');
                return false;
            }

            _cacheConfig();
        }

        function _cacheConfig() {
            $mapHolder = config.$mapHolder;
            locations = config.locations;

            if (typeof config.pin !== 'undefined') {
                pin = config.pin;
            }

            if (typeof config.tooltips !== 'undefined') {
                tooltips = config.tooltips;
            }

            _createMap();
        }

        function _createMap() {
            var mapStyles = [];
            var pinSize = new google.maps.Size(pin.x, pin.y);
            var mapSettings = {
                zoom: 15, // work only when there is one pin on the map
                center: new google.maps.LatLng(locations[0][0], locations[0][1]),
                scrollwheel: false,
                styles: mapStyles,
                disableDefaultUI: false,
                panControl: true,
                zoomControl: true,
                mapTypeControl: true,
                scaleControl: true,
                streetViewControl: true,
                overviewMapControl: true,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            var bounds = new google.maps.LatLngBounds();
            var infoWindow;
            var i;

            if (tooltips) {
                infoWindow = new google.maps.InfoWindow();

                // check for html in locations array
                try {
                    if (locations[0][2].length) {}
                } catch (e) {
                    console.warn('Component.GoogleMap: Requre html from locations array!');

                    tooltips = false;
                }
            }

            // Display a map on the page.
            map = new google.maps.Map(document.getElementById($mapHolder[0].id), mapSettings);

            function createMarker(location) {
                var latLng = new google.maps.LatLng(location[0], location[1]);
                var marker = new google.maps.Marker({
                    position: latLng,
                    map: map,
                    animation: google.maps.Animation.DROP,
                    icon: {
                        url: pin.src,
                        scaledSize: pinSize,
                        // pin point position
                        // anchor: new google.maps.Point(23, 64)
                    }
                });
                markers.push(marker);

                bounds.extend(latLng);

                if (tooltips) {
                    google.maps.event.addListener(marker, 'click', function() {
                        infoWindow.close(); // close previously opened infowindow
                        infoWindow.setContent('<div class="map-tooltip">' + location[2] + '</div>');
                        infoWindow.open(map, marker);

                        var iwOuter = $('.gm-style-iw');

                        /* Since this div is in a position prior to .gm-div style-iw.
                         * We use jQuery and create a iwBackground variable,
                         * and took advantage of the existing reference .gm-style-iw for the previous div with .prev().
                         */
                        var iwBackground = iwOuter.prev();

                        iwBackground.addClass('popup-container');
                        iwBackground.children(':nth-child(1)').addClass('pointer-border');
                        iwBackground.children(':nth-child(3)').addClass('pointer');

                        // Removes background shadow DIV
                        iwBackground.children(':nth-child(2)').css({ 'display': 'none' });

                        // Removes white background DIV
                        iwBackground.children(':nth-child(4)').css({ 'display': 'none' });


                        // Reference to the div that groups the close button elements.
                        var iwCloseBtn = iwOuter.next();

                        // Apply the desired effect to the close button
                        iwCloseBtn.css({ opacity: '1', right: '20px', top: '20px', border: '1px solid var(--color-secondary)', 'border-radius': '13px', 'box-shadow': '0 0 5px #3990B9' });
                    });
                }
            }

            // Create markers for all locations.
            for (i = 0; i < locations.length; i++) {
                createMarker(locations[i]);
            }

            // Automatically center the map fitting all markers on the screen. Ignore zoom from settings.
            if (locations.length > 1) {
                map.fitBounds(bounds);
            }

            var markerCluster = new MarkerClusterer(map, markers, { imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
        }

        function _panTo(lat, lng) {
            // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
            // var boundsListener = google.maps.event.addListener(map, 'bounds_changed', function(event) {
            // 	this.setZoom(15);
            // 	google.maps.event.removeListener(boundsListener);
            // });

            map.panTo({
                lat: Number(lat),
                lng: Number(lng)
            });
        }

        return {
            init: function(configuration) {
                _init(configuration);
            },
            panTo: function(lat, lng) {
                _panTo(lat, lng);
            }
        };
    })();

    $.fn.transform_select = function() {
        return function() {
            return $(this).each(function() {
                var $this = $(this),
                    numberOfOptions = $this.children('option').length;
                $this.addClass('select-hidden');
                $this.after('<div class="select-head"><span class="head-text"></span></div>');
                var $select_head = $this.next('div.select-head');
                var $head_text = $select_head.find('.head-text');
                if ($this.hasClass('has-error')) {
                    $select_head.addClass('error');
                } else {
                    $select_head.removeClass('error');
                }
                $head_text.text($this.children('option').eq(0).text()); /// use first option for placeholder ( disabled selected props)
                var $list = $('<ul />', {
                    'class': 'select-options'
                }).insertAfter($select_head);
                for (var i = 1; i < numberOfOptions; i++) {
                    var title = $this.children('option').eq(i).text();
                    var data_index = $this.children('option').eq(i).val();
                    var $li = $('<li />');
                    var $link = $('<a />');
                    if ($this.hasClass('link-select')) {
                        $li.attr('data-index', data_index);
                        $link.attr('href', data_index);
                        $link.text(title);
                        $li.append($link);
                    } else {
                        $li.text(title);
                        $li.attr('data-index', data_index);
                    }
                    if ($this.children('option').eq(i).is(':selected')) {
                        $li.addClass('selected');
                        $head_text.text($li.text());
                    }
                    $li.appendTo($list);
                }
                var $listItems = $list.children('li');
                $select_head.on('click', function(e) {
                    e.stopPropagation();
                    $('div.select-head.active').not(this).each(function() {
                        $(this).removeClass('active').next('ul.select-options').removeClass('open');
                        // $(this).removeClass('active').next('ul.select-options').hide();
                    });
                    $(this).toggleClass('active').next('ul.select-options').toggleClass('open');
                    // $(this).toggleClass('active').next('ul.select-options').toggle();
                });
                $listItems.on('click', function(e) {
                    e.stopPropagation();
                    var $that = $(this);
                    var $option = $($this.children('option[value="' + $that.data('index') + '"]')[0]);
                    $option.attr('selected', 'selected');
                    $option.siblings('option').removeAttr('selected');
                    $that.addClass('selected');
                    $this[0].value = $option[0].value;
                    $this.trigger('change');
                    $that.siblings('li').removeAttr('class');
                    // $this.val($option.val()); // doesnt work on iOS
                    $head_text.text($that.text()).removeClass('active');
                    $list.removeClass('open');
                    $select_head.removeClass('active');
                });
                $(document).on('click', function() {
                    $select_head.removeClass('active');
                    $list.removeClass('open');
                });
            });
        };
    }();

    function accentCarouselInit() {
        $('.accent-carousel').slick({
            infinite: true,
            autoplay: true,
            autoplaySpeed: 2000,
            slidesToScroll: 1
        });
    }



    function productsCarousel() {
        var $sliderWrapper = $('.products-slider');
        var $elementsWrapper = $sliderWrapper.find('.boxes-products');
        if ($elementsWrapper.children().length > 1) {
            $($elementsWrapper).slick({
                infinite: true,
                slidesToShow: 4,
                slidesToScroll: 1,
                prevArrow: $sliderWrapper.find($('.prev-arrow')),
                nextArrow: $sliderWrapper.find($('.next-arrow')),
                responsive: [{
                        breakpoint: 1200,
                        settings: {
                            slidesToShow: 3,
                        }
                    },
                    {
                        breakpoint: 991,
                        settings: {
                            slidesToShow: 2,
                        }
                    },
                    {
                        breakpoint: 679,
                        settings: {
                            slidesToShow: 1,
                        }
                    }
                ]
            });
        }
    }

    function textPageCartouselInit() {
        $('.c-carousel-container .img-carousel').slick({
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 1,
            prevArrow: $('.prev-arrow'),
            nextArrow: $('.next-arrow'),
            responsive: [{
                    breakpoint: 1024,
                    settings: {
                        slidesToShow: 2
                    }
                },
                {
                    breakpoint: 620,
                    settings: {
                        slidesToShow: 1
                    }
                }
            ]
        });

    }

    function openLevelTwoNav() {

        $('.nav-primary .level-1 > li').on('click', function(e) {
            var $this = $(this);
            if(!$this.hasClass("promo-tab")){
                $this.toggleClass('selected');
                $this.find('.dropdown-menu').toggleClass('has-flag');
                $this.siblings().find('.dropdown-menu').removeClass('has-flag');
            }
        });
    }

    // function priceSlider() {
    // 	var $that = $('.range-slider-values');
    // 	var min = $('#min-value').attr('data-value');
    // 	var max = $('#max-value').attr('data-value');

    // 	if ($that.find('input[name="rating_min"]').length) {
    // 		min = $that.find('input[name="rating_min"]')[0].value ? $that.find('input[name="rating_min"]')[0].value : 2;
    // 		max = $that.find('input[name="rating_max"]')[0].value ? $that.find('input[name="rating_max"]')[0].value : 4;
    // 	}
    // 	var values = [min ,max];
    // 	$('#range_slider').slider({
    // 		range: true,
    // 		min: Number(min),
    // 		max: Number(max),
    // 		values: values,
    // 		slide: function(event, ui) {
    // 			$('#min-value').val(ui.values[0]);
    // 			$('#max-value').val(ui.values[1]);
    // 		}
    // 	});
    // 	$('#min-value').val($('#range_slider').slider('values',0));
    // 	$('#max-value').val($('#range_slider').slider('values',1));

    // $('#range_slider').on('slidechange', function(event, ui) {
    // 	alert('promqna');
    // });
    // }

    function showFilterDropdown() {
        $('.filter-type').on('click', function() {
            $(this).toggleClass('has-flag');
        });
        if ($('.filter-content .form-row input:checked').length) {
            var $this = $('.filter-content input:checked');
            $this.parents('.filter-content').prev('.filter-type').addClass('has-flag');
        }
    }

    function changeImg() {
        $('.c-img-galery img').on('click', function() {
            $('.c-large-galery-img img').attr('src', $(this).attr('src'));
        });
    }

    function openDropdownFilter() {
        $('.level2-container .filter-heading').on('click', function() {
            $('.level2-container .filter-heading').toggleClass('active');
            $('.filter-content-level2').toggleClass('open');
        });

        if ($('.filter-content-level2 .form-row input:checked').length) {
            console.log('here');
            $('.level2-container').parents('.filter-content').prev('.filter-type').addClass('has-flag');
            $('.level2-container .filter-heading').addClass('active');
            $('.filter-content-level2').addClass('open');
        }
    }

    function changeFilterColor() {
        $('.form-filters a').on('click', function() {
            $('.form-filters a').toggleClass('selected');
        });
    }

    function changeProductQuantity() {
        $('.decrease, .increase').on('click', function() {
            var $this = $(this),
                quantityValue = parseInt($this.siblings('input').val()),
                singlePrice = parseFloat($this.parents('.c-quantity').prev('.c-single-price').find('.price').text()),
                finalPrice = parseFloat($this.parents('.c-quantity').next('.c-final-price').find('.price').text());

            if ($('.cart-product-list').length) {
                if ($this.hasClass('decrease')) {
                    quantityValue = quantityValue - 1;
                    finalPrice = finalPrice - singlePrice;
                } else if ($this.hasClass('increase')) {
                    quantityValue = quantityValue + 1;
                    finalPrice = finalPrice + singlePrice;
                }
                if (quantityValue < 1) {
                    quantityValue = 1;
                    finalPrice = singlePrice;
                }

                $this.siblings('input').val(quantityValue);
                $this.parents('.c-quantity').next('.c-final-price').find('.price').text(finalPrice.toFixed(2) + ' лв.');

            } else {
                if ($this.hasClass('decrease')) {
                    quantityValue = quantityValue - 1;
                } else if ($this.hasClass('increase')) {
                    quantityValue = quantityValue + 1;
                }
                if (quantityValue < 1) {
                    quantityValue = 1;
                }
                $this.siblings('input').val(quantityValue);
            }

        });
        $('.quantity-input input[type="number"]').on('change', function(evt) {
            var $this = $(this),
                singlePrice = parseFloat($this.parents('.c-quantity').prev('.c-single-price').find('.price').text()),
                finalPrice = parseFloat($this.parents('.c-quantity').next('.c-final-price').find('.price').text());

            if ((parseFloat($this.val()) < 1) || ($this.val() == '')) {
                $this.val(1);
            }
            finalPrice = singlePrice * parseFloat($this.val());
            $this.parents('.c-quantity').next('.c-final-price').find('.price').text(finalPrice.toFixed(2) + ' лв.');

        });
        $('.quantity-input input[type="number"]').on('keyup', function(evt) {
            var $this = $(this),
                singlePrice = parseFloat($this.parents('.c-quantity').prev('.c-single-price').find('.price').text()),
                finalPrice = parseFloat($this.parents('.c-quantity').next('.c-final-price').find('.price').text());

            if ((evt.which <= 48 && evt.which >= 57) || (evt.which <= 96 && evt.which >= 105)) {
                evt.preventDefault();
            } else {
                if ((parseFloat($this.val()) < 1)) {
                    $this.val(1);
                }
                if ($this.val() == '') {
                    finalPrice = 0;
                } else {
                    finalPrice = singlePrice * parseFloat($this.val());
                }
                $this.parents('.c-quantity').next('.c-final-price').find('.price').text(finalPrice.toFixed(2) + ' лв.');
            }
        });
    }

    function changeProductVariation(){
        $(".product-variations").on('change', function(){
            var $option = $(this);
            var variationId = $option.val();
            var url = $option.children("option:selected").data('details-url');
            var internal_id = $option.children("option:selected").data('internal-id');
            $.ajax({
                url: url,
                type: 'GET',
                dataType: 'json',
                success: function(result) {
                    $('.variations-input').val(variationId);
                    $('.product-number mark').text(internal_id);
                    if (result.price){
                        $('.current-price .number').text(result.price);
                    }
                }
            });
        });
    }

    function tabsNavigation() {
        $('.tab-heading').on('click', function() {
            var $this = $(this);
            if ($this.hasClass('description-heading') && !($this.hasClass('has-flag'))) {
                $this.addClass('has-flag');
                $this.siblings().removeClass('has-flag');
                $('.description-content').addClass('has-flag');
                $('.description-content').siblings().removeClass('has-flag');
            } else if ($this.hasClass('characteristics-heading')) {
                $this.addClass('has-flag');
                $this.siblings().removeClass('has-flag');
                $('.characteristics-content').addClass('has-flag');
                $('.characteristics-content').siblings().removeClass('has-flag');
            } else if ($this.hasClass('docs-heading')) {
                $this.addClass('has-flag');
                $this.siblings().removeClass('has-flag');
                $('.boxes-attached-files').addClass('has-flag');
                $('.boxes-attached-files').siblings().removeClass('has-flag');
            } else if ($this.hasClass('credit-heading')) {
                $this.addClass('has-flag');
                $this.siblings().removeClass('has-flag');
                $('.credit-content').addClass('has-flag');
                $('.credit-content').siblings().removeClass('has-flag');
            }
        });
    }

    function regTabs() {
        $('.c-reg-tabs span').on('click', function() {
            var $this = $(this);
            if ($this.hasClass('tab-personal') && !($this.hasClass('has-flag'))) {
                $this.addClass('has-flag');
                $('.tab-business').removeClass('has-flag');
                $('.form-personal-acc').addClass('has-flag');
                $('.form-business-acc').removeClass('has-flag');
            } else if ($this.hasClass('tab-business') && !($this.hasClass('has-flag'))) {
                $this.addClass('has-flag');
                $('.tab-personal').removeClass('has-flag');
                $('.form-business-acc').addClass('has-flag');
                $('.form-personal-acc').removeClass('has-flag');
            }
        });
    }

    // function PopUp(title, description, refLink){
    // 	if ($(this).is('#finish_order_js')) {
    // 		var stepFour = $(this).parents('.b-cart-step3').find('.step-node').last();
    // 		stepFour.siblings().removeClass('has-flag');
    // 		stepFour.addClass('has-flag');
    // 	}
    // 	$('.pop-up .title').text(title);
    // 	$('.pop-up .short-desc').text(description);
    // 	$('.pop-ups-container').fadeIn();
    // 	$('.pop-up').fadeIn();
    // 	$('body, html').addClass('no-scroll');
    // 	$('#navigate_to_js').attr('href', refLink);

    // 	$('#navigate_to_js').on('click', function(){
    // 		$('.pop-ups-container').fadeOut();
    // 		$('.pop-up').fadeOut();
    // 		$('body, html').removeClass('no-scroll');
    // 	});
    // }

    Component.Popup = (function() {
        var $element = null;

        function init(element) {
            $element = $(element) ? $(element) : $('.pop-up');
        }

        function _open() {
            $('.pop-ups-container').fadeIn();
            $('.pop-up').fadeIn();
            $('body, html').addClass('no-scroll');
            $('#navigate_to_js').on('click', function() {
                $('.pop-ups-container').fadeOut();
                $('.pop-up').fadeOut();
                $('body, html').removeClass('no-scroll');
            });
        }

        function _set_content(title, content, refLink) {
            if (title) {
                $element.find('.title').text(title);
            }
            if (content) {
                $element.find('.short-desc').text(content);
            }
            if (content) {
                $('#navigate_to_js').attr('href', refLink);
            }
        }
        return {
            init: function(element) {
                init(element);
            },
            open: function(title, content, refLink) {
                _set_content(title, content, refLink);
                _open();
            },
            set_content: function(title, content, refLink) {
                _set_content(title, content, refLink);
            }
        };
    })();

    function moveToStepFour() {
        $('#finish_order_js, #finish_order_business_js').on('click', function() {
            var stepFour = $(this).parents('.b-cart-step3').find('.step-node').last();
            stepFour.siblings().removeClass('has-flag');
            stepFour.addClass('has-flag');
            // Component.Popup.open('Test', 'Test desc', 'products.html');
        });
    }

    function searchAutocompleteInit() {
        $('#search').on('keydown', function() {
            $('.search-dropdown').addClass('active');
        });
        $('#search').on('focusout', function() {
            $('.search-dropdown').removeClass('active');
        });
    }

    function profileNavigation() {
        $('.profile-tab').on('click', function() {
            var $this = $(this);

            if ($this.is('#edit_profile') && !$this.hasClass('has-flag')) {
                $this.addClass('has-flag');
                $this.siblings().removeClass('has-flag');
                $('.c-tab-edit-content').addClass('has-flag');
                $('.c-tab-edit-content').siblings().removeClass('has-flag');
            } else if ($this.is('#order_history') && !$this.hasClass('has-flag')) {
                $this.addClass('has-flag');
                $this.siblings().removeClass('has-flag');
                $('.c-tab-history-content').addClass('has-flag');
                $('.c-tab-history-content').siblings().removeClass('has-flag');
            }

        });
    }

    function mapChangeLocation() {
        $('.address-container').on('click', function() {
            var $this = $(this);
            var content = $this.find('.address-text').html() + '<br/><a href="https://google.com">check more!</a>';
            var location = $this.find('js-map-location');
            Component.GoogleMap.switchLocation(location.data('lat'), location.data('lng'), content);

        });
    }

    function openHamburgerMenu() {
        $('.hamburger').on('click', function() {
            $(this).toggleClass('has-flag');
            $(this).parents('.header-container').find('.header-bottom').toggleClass('has-flag');
        });
    }

    function doubleClickSearch() {

        if ($(window).width() <= 479) {
            var onHover = false;

            $('#search_js').on('click', function(e) {
                if (!onHover) {
                    e.preventDefault();
                    onHover = true;
                } else {
                    $('.nav-secondary .search-box form').submit();
                }
            });

        }

    }

    function productImageCarousel() {
        $('.product-image-slider').slick({
            arrows: true,
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 1,
            vertical: true,
            nextArrow: $('#product_slider_next'),
            prevArrow: $('#product_slider_prev'),
            responsive: [{
                    breakpoint: 1024,
                    settings: {
                        vertical: false,
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        verical: true,
                    }
                },
                {
                    breakpoint: 480,
                    settings: {
                        vertical: false,
                    }
                }
            ]
        });
    }

    /* ------------------------------------------------------------ *\
    	# Events
    \* ------------------------------------------------------------ */

    $(document).ready(function() {
        /**
         * Google maps init.
         */
        var locations = [];

        if ($('#js_map').length) {

            locations = [];
            $('.js-map-location').each(function() {
                var $this = $(this);
                locations.push([$this.attr('data-lat'), $this.attr('data-lng')]);
            });

            Component.GoogleMap.init({
                $mapHolder: $('#js_map'),
                locations: locations,
                customPin: false,
                tooltips: true,
            });
        }

        Helpers.autocomplete.init();
        Component.Popup.init('.pop-up');

        accentCarouselInit();
        textPageCartouselInit();
        showFilterDropdown();
        changeImg();
        openDropdownFilter();
        changeFilterColor();
        changeProductQuantity();
        tabsNavigation();
        regTabs();
        moveToStepFour();
        searchAutocompleteInit();
        profileNavigation();
        mapChangeLocation();
        openHamburgerMenu();
        openLevelTwoNav();
        doubleClickSearch();
        productsCarousel();
        productImageCarousel();
        changeProductVariation();



        /* Transform selects */
        $('#languages_js').transform_select();
        $('#manufacture_js').transform_select();
        $('#order_by_js').transform_select();
        $('#show_type_js').transform_select();
        $('#accessories_js').transform_select();
        $('#delivery_type_js').transform_select();
        $('#payment_type_js').transform_select();
        $('#credit_duration').transform_select();
        $('.product-variations').transform_select();

        $('#manufactures_search').select2({
            placeholder: 'Избери Производител'
        });
        $('#manufactures_search').select2({
            placeholder: 'Избери Производител'
        });

        /**
         * All notifications configuration
         *
         * plugin: toastr
         * https://github.com/CodeSeven/toastr
         */
        toastr.options = {
            "closeButton": true,
            "debug": false,
            "newestOnTop": false,
            "progressBar": true,
            "positionClass": "toast-top-full-width",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "10000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        };

    });
})(jQuery, window, document);