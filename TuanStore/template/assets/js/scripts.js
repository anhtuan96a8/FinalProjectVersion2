﻿(function($) {
    "use strict";

    
    /*  WOW */

    $(document).ready(function () {
        new WOW().init();
    });
    
    /*  OWL CAROUSEL*/

    $(document).ready(function () {
        
        var dragging = true;
        var owlElementID = "#owl-main";
        
        function fadeInReset() {
            if (!dragging) {
                $(owlElementID + " .caption .fadeIn-1, " + owlElementID + " .caption .fadeIn-2, " + owlElementID + " .caption .fadeIn-3").stop().delay(50).animate({ opacity: 0 }, { duration: 100, easing: "easeInCubic" });
            }
            else {
                $(owlElementID + " .caption .fadeIn-1, " + owlElementID + " .caption .fadeIn-2, " + owlElementID + " .caption .fadeIn-3").css({ opacity: 0 });
            }
        }
        
        function fadeInDownReset() {
            if (!dragging) {
                $(owlElementID + " .caption .fadeInDown-1, " + owlElementID + " .caption .fadeInDown-2, " + owlElementID + " .caption .fadeInDown-3").stop().delay(800).animate({ opacity: 0, top: "-15px" }, { duration: 400, easing: "easeInCubic" });
            }
            else {
                $(owlElementID + " .caption .fadeInDown-1, " + owlElementID + " .caption .fadeInDown-2, " + owlElementID + " .caption .fadeInDown-3").css({ opacity: 0, top: "-15px" });
            }
        }
        
        function fadeInUpReset() {
            if (!dragging) {
                $(owlElementID + " .caption .fadeInUp-1, " + owlElementID + " .caption .fadeInUp-2, " + owlElementID + " .caption .fadeInUp-3").stop().delay(800).animate({ opacity: 0, top: "15px" }, { duration: 400, easing: "easeInCubic" });
            }
            else {
                $(owlElementID + " .caption .fadeInUp-1, " + owlElementID + " .caption .fadeInUp-2, " + owlElementID + " .caption .fadeInUp-3").css({ opacity: 0, top: "15px" });
            }
        }
        
        function fadeInLeftReset() {
            if (!dragging) {
                $(owlElementID + " .caption .fadeInLeft-1, " + owlElementID + " .caption .fadeInLeft-2, " + owlElementID + " .caption .fadeInLeft-3").stop().delay(800).animate({ opacity: 0, left: "15px" }, { duration: 400, easing: "easeInCubic" });
            }
            else {
                $(owlElementID + " .caption .fadeInLeft-1, " + owlElementID + " .caption .fadeInLeft-2, " + owlElementID + " .caption .fadeInLeft-3").css({ opacity: 0, left: "15px" });
            }
        }
        
        function fadeInRightReset() {
            if (!dragging) {
                $(owlElementID + " .caption .fadeInRight-1, " + owlElementID + " .caption .fadeInRight-2, " + owlElementID + " .caption .fadeInRight-3").stop().delay(800).animate({ opacity: 0, left: "-15px" }, { duration: 400, easing: "easeInCubic" });
            }
            else {
                $(owlElementID + " .caption .fadeInRight-1, " + owlElementID + " .caption .fadeInRight-2, " + owlElementID + " .caption .fadeInRight-3").css({ opacity: 0, left: "-15px" });
            }
        }
        
        function fadeIn() {
            $(owlElementID + " .active .caption .fadeIn-1").stop().delay(500).animate({ opacity: 1 }, { duration: 800, easing: "easeOutCubic" });
            $(owlElementID + " .active .caption .fadeIn-2").stop().delay(700).animate({ opacity: 1 }, { duration: 800, easing: "easeOutCubic" });
            $(owlElementID + " .active .caption .fadeIn-3").stop().delay(1000).animate({ opacity: 1 }, { duration: 800, easing: "easeOutCubic" });
        }
        
        function fadeInDown() {
            $(owlElementID + " .active .caption .fadeInDown-1").stop().delay(500).animate({ opacity: 1, top: "0" }, { duration: 800, easing: "easeOutCubic" });
            $(owlElementID + " .active .caption .fadeInDown-2").stop().delay(700).animate({ opacity: 1, top: "0" }, { duration: 800, easing: "easeOutCubic" });
            $(owlElementID + " .active .caption .fadeInDown-3").stop().delay(1000).animate({ opacity: 1, top: "0" }, { duration: 800, easing: "easeOutCubic" });
        }
        
        function fadeInUp() {
            $(owlElementID + " .active .caption .fadeInUp-1").stop().delay(500).animate({ opacity: 1, top: "0" }, { duration: 800, easing: "easeOutCubic" });
            $(owlElementID + " .active .caption .fadeInUp-2").stop().delay(700).animate({ opacity: 1, top: "0" }, { duration: 800, easing: "easeOutCubic" });
            $(owlElementID + " .active .caption .fadeInUp-3").stop().delay(1000).animate({ opacity: 1, top: "0" }, { duration: 800, easing: "easeOutCubic" });
        }
        
        function fadeInLeft() {
            $(owlElementID + " .active .caption .fadeInLeft-1").stop().delay(500).animate({ opacity: 1, left: "0" }, { duration: 800, easing: "easeOutCubic" });
            $(owlElementID + " .active .caption .fadeInLeft-2").stop().delay(700).animate({ opacity: 1, left: "0" }, { duration: 800, easing: "easeOutCubic" });
            $(owlElementID + " .active .caption .fadeInLeft-3").stop().delay(1000).animate({ opacity: 1, left: "0" }, { duration: 800, easing: "easeOutCubic" });
        }
        
        function fadeInRight() {
            $(owlElementID + " .active .caption .fadeInRight-1").stop().delay(500).animate({ opacity: 1, left: "0" }, { duration: 800, easing: "easeOutCubic" });
            $(owlElementID + " .active .caption .fadeInRight-2").stop().delay(700).animate({ opacity: 1, left: "0" }, { duration: 800, easing: "easeOutCubic" });
            $(owlElementID + " .active .caption .fadeInRight-3").stop().delay(1000).animate({ opacity: 1, left: "0" }, { duration: 800, easing: "easeOutCubic" });
        }
        
        $(owlElementID).owlCarousel({
            
            autoPlay: 5000,
            stopOnHover: true,
            navigation: true,
            pagination: true,
            singleItem: true,
            addClassActive: true,
            transitionStyle: "fade",
            navigationText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"],
                
            afterInit: function() {
                fadeIn();
                fadeInDown();
                fadeInUp();
                fadeInLeft();
                fadeInRight();
            },
            
            afterMove: function() {
                fadeIn();
                fadeInDown();
                fadeInUp();
                fadeInLeft();
                fadeInRight();
            },
            
            afterUpdate: function() {
                fadeIn();
                fadeInDown();
                fadeInUp();
                fadeInLeft();
                fadeInRight();
            },
            
            startDragging: function() {
                dragging = true;
            },
            
            afterAction: function() {
                fadeInReset();
                fadeInDownReset();
                fadeInUpReset();
                fadeInLeftReset();
                fadeInRightReset();
                dragging = false;
            }
            
        });
        
        if ($(owlElementID).hasClass("owl-one-item")) {
            $(owlElementID + ".owl-one-item").data('owlCarousel').destroy();
        }
        
        $(owlElementID + ".owl-one-item").owlCarousel({
            singleItem: true,
            navigation: false,
            pagination: false
        });
        
        $('#transitionType li a').click(function () {
            
            $('#transitionType li a').removeClass('active');
            $(this).addClass('active');
            
            var newValue = $(this).attr('data-transition-type');
            
            $(owlElementID).data("owlCarousel").transitionTypes(newValue);
            $(owlElementID).trigger("owl.next");
            
            return false;
            
        });

        $("#owl-recently-viewed").owlCarousel({
            stopOnHover: true,
            rewindNav: true,
            items: 6,
            pagination: false,
            itemsTablet: [768,3]
        });

        $("#owl-recently-viewed-2").owlCarousel({
            stopOnHover: true,
            rewindNav: true,
            items: 4,
            pagination: false,
            itemsTablet: [768,3],
            itemsDesktopSmall: [1199,3],
        });

        $("#owl-brands").owlCarousel({
            stopOnHover: true,
            rewindNav: true,
            items: 6,
            pagination: false,
            itemsTablet : [768, 4]
        });

        $('#owl-single-product').owlCarousel({
            singleItem: true,
            pagination: false
        });

        $('#owl-single-product-thumbnails').owlCarousel({
            items: 6,
            pagination: false,
            rewindNav: true,
            itemsTablet : [768, 4]
        });

        $('#owl-recommended-products').owlCarousel({
            rewindNav: true,
            items: 4,
            pagination: false,
            itemsTablet: [768, 3],
            itemsDesktopSmall: [1199,3],
        });

        $('.single-product-slider').owlCarousel({
            stopOnHover: true,
            rewindNav: true,
            singleItem: true,
            pagination: false
        });
        
        $(".slider-next").click(function () {
            var owl = $($(this).data('target'));
            owl.trigger('owl.next');
            return false;
        });
        
        $(".slider-prev").click(function () {
            var owl = $($(this).data('target'));
            owl.trigger('owl.prev');
            return false;
        });

        $('.single-product-gallery .horizontal-thumb').click(function(){
            var $this = $(this), owl = $($this.data('target')), slideTo = $this.data('slide');
            owl.trigger('owl.goTo', slideTo);
            $this.addClass('active').parent().siblings().find('.active').removeClass('active');
            return false;
        });
        
    });

    
    $(document).ready(function () {
        if ($('.star').length > 0) {
            $('.star').each(function () {
                var $star = $(this);
                $star.raty({
                    readOnly: true,
                    starOff: 'images/icon/star-none.png',
                    starOn: 'images/icon/star.png',
                    path: document.location.origin,
                    space: false,
                    score: function () {
                        return $(this).attr('data-score');
                    }
                });
            });
        }
        if ($('.star-big').length > 0) {
            $('.star-big').each(function () {
                var $star = $(this);
                $star.raty({
                    readOnly: true,
                    starOff: 'images/icon/star-none.png',
                    starOn: 'images/icon/star.png',
                    path: document.location.origin,
                    space: false,
                    score: function () {
                        return $(this).attr('data-score');
                    }
                });
            });
        }
        $('.star-big').raty({
            starOff: 'images/icon/star-none.png',
            starOn: 'images/icon/star.png',
            path: document.location.origin,
            space: false,
            score: function () {
                return $(this).attr('data-score');
            },
            click: function (score, evt) {
                $('#RateDanhGia').val(score);
            }
        });
        $('#NoiDungDanhGia').on('input', function (e) {
            var comment = $('#NoiDungDanhGia').val();

            if (comment.length > 3) {
                var index = comment.length - 1;
                if (index != -1) {
                    if ((comment.charAt(index) == ' ' || comment.charAt(index) == '.')) {
                        $.ajax({
                            url: "http://localhost:9874/sav",
                            type: "post",
                            dataType: 'text',
                            data: {
                                Comment: comment
                            },
                            success: function (result) {
                                $('.star-big').raty({
                                    showCancel: true,
                                    starOff: 'images/icon/star-none.png',
                                    starOn: 'images/icon/star.png',
                                    path: document.location.origin,
                                    space: false,
                                    score: result,
                                    click: function (score, evt) {
                                        $('#RateDanhGia').val(score);
                                        if (score == 1) {
                                            $('#name_rate').html('Không Tốt')
                                        }
                                        else if (score == 2) {
                                            $('#name_rate').html('Trung Bình Khá')
                                        } else if (score == 3) {
                                            $('#name_rate').html('Trung Bình')
                                        } else if (score == 4) {
                                            $('#name_rate').html('Tốt')
                                        } else if (score == 5) {
                                            $('#name_rate').html('Rất Tốt')
                                        }
                                    }
                                });
                                $('#RateDanhGia').val(result);
                                if (result == 1) {
                                    $('#name_rate').html('Không Tốt')
                                }
                                else if (result == 2) {
                                    $('#name_rate').html('Trung Bình Khá')
                                } else if (result == 3) {
                                    $('#name_rate').html('Trung Bình')
                                } else if (result == 4) {
                                    $('#name_rate').html('Tốt')
                                } else if (result == 5) {
                                    $('#name_rate').html('Rất Tốt')
                                }
                                else $('#name_rate').html('')
                            }
                        });
                    }
                }
            }
            else {
                $('.star-big').raty({
                    starOff: 'images/icon/star-none.png',
                    starOn: 'images/icon/star.png',
                    path: document.location.origin,
                    space: false,
                    score: 0
                });
            }
        });
    });

    
    /*  SHARE THIS BUTTONS*/

    $(document).ready(function () {
        if($('.social-row').length > 0){
            stLight.options({publisher: "2512508a-5f0b-47c2-b42d-bde4413cb7d8", doNotHash: false, doNotCopy: false, hashAddressBar: false});
        }
    });

    
    /*  CUSTOM CONTROLS*/

    $(document).ready(function () {
        
        // Select Dropdown
        if($('.le-select').length > 0){
            $('.le-select select').customSelect({customClass:'le-select-in'});
        }

        // Checkbox
        if($('.le-checkbox').length>0){
            $('.le-checkbox').after('<i class="fake-box"></i>');
        }

        //Radio Button
        if($('.le-radio').length>0){
            $('.le-radio').after('<i class="fake-box"></i>');
        }

        // Buttons
        $('.le-button.disabled').click(function(e){
            e.preventDefault();
        });

        
        // Price Slider
        if ($('.price-slider').length > 0) {
            $('.price-slider').slider({
                min: 0,
                max: 30000000,
                step: 500000,
                value: [1000, 500000],
                handle: "square"

            });
        }

        // Data Placeholder for custom controls

        $('[data-placeholder]').focus(function() {
            var input = $(this);
            if (input.val() == input.attr('data-placeholder')) {
                input.val('');

            }
        }).blur(function() {
            var input = $(this);
            if (input.val() === '' || input.val() == input.attr('data-placeholder')) {
                input.addClass('placeholder');
                input.val(input.attr('data-placeholder'));
            }
        }).blur();

        $('[data-placeholder]').parents('form').submit(function() {
            $(this).find('[data-placeholder]').each(function() {
                var input = $(this);
                if (input.val() == input.attr('data-placeholder')) {
                    input.val('');
                }
            });
        });

    });

    /*===================================================================================*/
    /*  LIGHTBOX ACTIVATOR
    /*===================================================================================*/
    $(document).ready(function(){
        if ($('a[data-rel="prettyphoto"]').length > 0) {
            //$('a[data-rel="prettyphoto"]').prettyPhoto();
        }
    });


    /*===================================================================================*/
    /*  SELECT TOP DROP MENU
    /*===================================================================================*/
    $(document).ready(function() {
        $('.top-drop-menu').change(function() {
            var loc = ($(this).find('option:selected').val());
            window.location = loc;
        });
    });

    /*  LAZY LOAD IMAGES USING ECHO*/
    $(document).ready(function(){
        echo.init({
            offset: 100,
            throttle: 250,
            unload: false
        });
    });

   
    
})(jQuery);