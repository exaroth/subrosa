//
// Subrosa Scripts files
// Copyright @2014 Konrad Wasowicz
//
// https://github.com/exaroth/subrosa
//
(function($) {


$(document).ready(function(){


    // Variables Caching

    var
    $body                = $('body'),
    $window              = $(window),
    $scratcharea            = $("textarea.scratch"),
    $articleInputBody    = $(".article-input-body"),
    $articleInputTitle   = $(".article-input-title"),
    $editForm            = $(".edit-article-form"),
    $createForm          = $(".new-article-form"),
    $editingTools        = $(".editing-tools"),
    $updateArticleButton = $(".update-button"),
    $submitButton        = $(".form-submit"),
    $hintIcons           = $(".hint-icon"),
    $articleBody         = $(".article-main").find(".article-body"),
    $articleList         = $(".article-list"),
    $indexWrapper        = $(".index-wrapper"),
    $editingButtons      = $(".editing-button"),
    $gallery             = $(".gallery-wrapper"),
    $dashboardArea       = $(".dashboard-area"),
    $lamp                = $(".lamp-button"),
    $imageLinks          = $(".show-img"),
    // base thumbnail size for gallery
    thumbSize            = 200,
    // variable referring to whether editing window is darkened
    dark                 = false,
    // variables referring to color of input fields in article edit
    articleTitleLight    = "#191919",
    articleBodyLight     = "#666",
    articleTitleDark     = "#b7b7b7",
    articleBodyDark      = "#848383",
    wWidth               = null,
    wHeight              = null,
    fadeoutIntVal        = null,
    fadeout              = false,
    // width of window where most responsive events are occuring
    majorBreakpoint      = 740,
    tocTemplate = "\
      <div class='toc'>\
        <div class='toc-header'><h3>Table of Contents</h3></div>\
        <ul class='toc-body list-unstyled'>\
        </ul>\
      </div>"


    // initialization function
    // =======================


    function init(){

        $articleBody.createToC();
        
        wWidth  = $window.width();
        wHeight = $window.height();

        // setDashboardBackground('#6a6a6e');

        $updateArticleButton.click(function(e){
            e.preventDefault();
            $editForm.submit();
        });

        matchIndexContents();

        $submitButton.click(function(e){
            e.preventDefault();
            $("#categories-hidden").val($("#categories").val());
            $("#series-hidden").val($("#series").val());
            $("#article-image-hidden").val($("#article-image").val());
            $("#article-image-small-hidden").val($("#article-image-small").val());
            $createForm.submit();
        });

        $("img.lazy").unveil(200, function(){
            $(this).load(function(){
                $(this).positionArticleImage();
                this.style.opacity = 1;
            });
        });

        enableTab($articleInputBody);

        $lamp.on('click', function(e){
            e.preventDefault();
            dimLight();
        });

        $('#imgur-upload').change(function(){
            $('#subfile').val($(this).val());
        });

        $('#upload-img').click(function(){
            $(".loading").fadeIn(200);
        });

        $imageLinks.magnificPopup({
            type: 'image',
            closeBtnInside: false,
            mainClass: 'mfp-fade',
            gallery: {
                enabled: true,
                preload: [1,2],
                navigateByImgClick: true,
                arrowMarkup: '<button type="button" class="mfp-arrow mfp-arrow-%dir%"></button>',

            }
        });

        $('.show-src').magnificPopup({
            type:'inline',
            midClick: true,
            callbacks: {
                beforeOpen: function() {
                    var mp   = $.magnificPopup.instance,
                    t        = $(mp.st.el),
                    full_src = t.data('fullsrc'),
                    thumb    = t.data('thumb'),
                    inputs   = $('.source-window').find('input[type="text"]');

                    $(inputs[0]).val(full_src);
                    $(inputs[1]).val(thumb);

                }
            }
        });

        // Prevent double clicks
        $("a, button").one("dblclick", function(e) {
            e.preventDefault();

        });

    };


    //functions to be initialised when window has loaded
    function start(){

        processGalleryImages($gallery);

        $scratcharea.autogrow();

        $hintIcons.tooltip({
            container: 'body'
        });

        $editingButtons.tooltip();

        $articleInputBody.focusin(function(){;
            fadeout = true;
            checkFadeout()
        })
		.focusout(function(){
            $editingTools.stop().fadeTo(100, '1')
            fadeout = false;
            clearInterval(fadeoutIntVal)
        });

        $window.mousemove(function(){
            if (fadeout){
                $editingTools.stop().fadeTo(100, '1');
            }
        });


        function checkFadeout(){
             fadeoutIntVal = setInterval(function(){
                if (fadeout){
                    $editingTools.stop().delay(6000).fadeTo(500, '0.2')
                };

            }, 1000)

        };

        
        $gallery.nested({
            selector : '.gallery-image',
            minWidth : 200,
            gutter: 10,
            resizeToFit: true,
            resizeToFitOptions: {
                resizeAny: true
            }
        });


        // if ($smallImgInput.length){
        //     if ($("#article-image").val().length > 0){
        //             $("#article-image-small-container").fadeTo(100, 1)
        //             $("#article-image-small").attr("disabled", false);
        //     };
        // }

        // $("#article-image").on("change keyup", function(e){
        //
        //     if ($(this).val().length > 0){
        //         $("#article-image-small").attr("disabled", false);
        //         $("#article-image-small-container").fadeTo(100, 1)
        //     } else {
        //         $("#article-image-small").attr("disabled", true);
        //         $("#article-image-small").val("")
        //         $("#article-image-small-container").fadeTo(100, 0.4);
        //     };
        // });


        $('.modal-toggle').magnificPopup({
            midClick: true,
            type: 'inline'
        });

        $('[data-toggle="confirmation"]').confirmation({
            popout: true,
            singleton: true,
            container: 'body',
            btnOkClass: 'btn btn-default btn-sm btn-confirm',
            btnCancelClass: 'btn btn-default btn-sm btn-cancel',
            btnOkLabel: '<i class="icon-ok"></i>Yes',
            btnCancelLabel: '<i class="icon-cancel"></i>No'
        });

        $("#link-fields").change(toggleSelectables);

    };




//======  Functions ========
	
	
    function matchIndexContents(){
        if(wWidth > majorBreakpoint){
            if($articleList.height() > $indexWrapper.height()){
                $indexWrapper.height($articleList.height());
            };
        }

    };


	// Toggle link fields in dashboard menu
    function toggleSelectables(){


        $("div[id^='selectable']")
        .hide()
        .filter("[id=selectable-" + this.value + "]").show();
    };
 
    // Darken/lighten screen in scratchpad view
    function dimLight(){
        if (!dark){
            $body.stop().animate({
                backgroundColor: "#222"
            }, 1200);
            $articleInputTitle.stop().animate({
                color: articleTitleDark
            }, 1200);
            $articleInputBody.stop().animate({
                color: articleBodyDark
            }, 1200);
            dark = true;

        } else {
         $body.stop().animate({
            backgroundColor: "#fff"
        }, 1200);
         $articleInputTitle.stop().animate({
            color: articleTitleLight
        }, 1200);
         $articleInputBody.stop().animate({
            color: articleBodyLight
        }, 1200);
         dark = false;

         }
     };



    // Disable tab trigger in textarea
    function enableTab(el) {

        el.on("keydown", function(e){
            if (e.keyCode === 9) { // tab was pressed

                // get caret position/selection
                var val = this.value,
                start   = this.selectionStart,
                end     = this.selectionEnd;

                // set textarea value to: text before caret + tab + text after caret
                this.value = val.substring(0, start) + '\t' + val.substring(end);

                // put caret at right position again
                this.selectionStart = this.selectionEnd = start + 1;

                // prevent the focus lose
                return false;

            }

        });
    };


    // Check if image is Horizontal
    function imgIsHorizontal(el){
        return el.width() > el.height();
    };


    // Get random value from given range
    function getRandomArbitary (min, max) {
        return Math.random() * (max - min) + min;
    };

    $.fn.positionArticleImage = function(){

        var self = $(this);
        var elToMove   = self.parent().is("a") ? self.parent() : self;
        var imgWrapper = elToMove
        .wrap('<div class="image-wrapper"></div>')
        .parent();
        if (imgIsHorizontal(self)){
            imgWrapper.addClass("centered-image-wrapper");
        } else {
            imgWrapper.addClass("floated-image-wrapper");
        }
        var imageDescription = $("<span></span>")
        .text(self.attr("alt"))
        .addClass("image-desc")
        .appendTo(imgWrapper);

    };

    // Create table of contents if h1
    // tags are in article body
    $.fn.createToC = function(){

        var self = $(this);
        var headers = self.find('h1');
        if ( headers.length > 1){

            var toc = $(tocTemplate)
            .appendTo($articleBody)
            .find('ul');

            headers.each(function(index){
                var $this = $(this)
                var link = $this.attr('id'),
                    name = $this.text();
                    var item = $('<a href="' + '#' + link + '">' + name + '</a>')
                    item
                    .wrap('<li></li>')
                    .parent()
                    .appendTo(toc);
            });

        };


    };


    // Randomize Image width in gallery
    function processGalleryImages(galleryBody){

        var imgs = galleryBody.find(".gallery-image");

        if(!imgs) { return };

        if(imgs.length < 5) {

            // If less than 5 images make each one big square;

            imgs.each(function(){
                $(this).addClass("size22");
            });

        } else {
            imgs.each(function(){

                var self     = $(this);
                var isSmall  = Math.round(Math.random() - 0.2);

                if (isSmall) {
                    self.addClass("size11");

                }
                else {
                    var isSquare        = Math.round(Math.random());
                    var imageIsVertical = self.data('vert')
                    if (isSquare){
                        self.addClass("size22");
                    } else {
                        if (imageIsVertical) {
                            self.addClass("size12");
                        } else {
                            self.addClass("size21")
                        }
                    }
                }
            });
        }

    };


   // Autogrowing textarea
   $.fn.autogrow = function(options)
   {
      return this.filter('textarea').each(function() {
       var self         = this;
       var $self        = $(self);
       var minHeight    = $self.height();
       var noFlickerPad = $self.hasClass('autogrow-short') ? 0 : parseInt($self.css('lineHeight')) || 0;

       var shadow = $('<div></div>').css({
        position:    'absolute',
        top:         -10000,
        left:        -10000,
        width:       $self.width(),
        fontSize:    $self.css('fontSize'),
        fontFamily:  $self.css('fontFamily'),
        fontWeight:  $self.css('fontWeight'),
        lineHeight:  $self.css('lineHeight'),
        resize:      'none',
        'word-wrap': 'break-word'
    }).appendTo(document.body);

       var update = function(event)
       {
        var times = function(string, number)
        {
         for (var i=0, r=''; i<number; i++) r += string;
          return r;
      };

      var val = self.value.replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/&/g, '&amp;')
      .replace(/\n$/, '<br/>&nbsp;')
      .replace(/\n/g, '<br/>')
      .replace(/ {2,}/g, function(space){ return times('&nbsp;', space.length - 1) + ' ' });

                    // Did enter get pressed?  Resize in this keydown event so that the flicker doesn't occur.
                    if (event && event.data && event.data.event === 'keydown' && event.keyCode === 13) {
                        val += '<br />';
                    }

                    shadow.css('width', $self.width());
                    shadow.html(val + (noFlickerPad === 0 ? '...' : '')); // Append '...' to resize pre-emptively.
                    $self.height(Math.max(shadow.height() + noFlickerPad, minHeight));
                }

                $self.change(update).keyup(update).keydown({event:'keydown'},update);
                $(window).resize(update);

                update();
            });
    };

// ====== Initialization ========

init();

$window.load(function(){
    start();
});

$window.bind('resize scroll', function(){
});

$window.resize(function(){
    wHeight = $window.height();
    wWidth = $window.width();
    matchIndexContents();
});


});



})(jQuery);



