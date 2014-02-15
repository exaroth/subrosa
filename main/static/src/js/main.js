(function($)
{
    /**
     * Auto-growing textareas; technique ripped from Facebook
     *
     * http://github.com/jaz303/jquery-grab-bag/tree/master/javascripts/jquery.autogrow-textarea.js
     */
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

// ------------------------------ My code here -----------------------------


})(jQuery);

$(window).load(function(){
var
$textarea = $("textarea"),
$articleInputBody = $(".article-input-body"),
$editForm = $(".edit-article-form"),
$createForm = $(".new-article-form"),
$updateArticleButton = $(".update-button"),
$createArticleButton = $(".create-button"),
$sidepanelToggler = $("#sidepanel-toggler"),
$miniIcons = $(".mini-icon"),
$editingButtons = $(".editing-button"),
$articleBody = $(".article-body"),
$gallery = $(".gallery-wrapper");

$updateArticleButton.click(function(e){
    e.preventDefault();
    $editForm.submit();
});
$createArticleButton.click(function(e){
    e.preventDefault();
    $createForm.submit();
});

enableTab($articleInputBody);

processArticleImages($articleBody)

// Disable tab trigger in textarea
function enableTab(el) {
    el.on("keydown", function(e){
        if (e.keyCode === 9) { // tab was pressed

            // get caret position/selection
            var val = this.value,
            start = this.selectionStart,
            end = this.selectionEnd;

            // set textarea value to: text before caret + tab + text after caret
            this.value = val.substring(0, start) + '\t' + val.substring(end);

            // put caret at right position again
            this.selectionStart = this.selectionEnd = start + 1;

            // prevent the focus lose
            return false;

        }

    })
};

// Check if image is Horizontal

function imgIsHorizontal(el){
    return el.width() > el.height();
};

function processArticleImages(articleBody){

    articleBody.find("img").each(function(e){

        var self = $(this);

        // If parent element is anchor move it otherwise move image
        var elToMove = self.parent().is("a") ? self.parent() : self;
        // Wrap image element or anchor with div and return it
        var imgWrapper = elToMove
                     .wrap('<div class="image-wrapper"></div>')
                     .parent();
        if (imgIsHorizontal(self)){
            elToMove.addClass("centered-image");
            imgWrapper.addClass("centered-image-wrapper");
            } else {
            elToMove.addClass("floated-image");
            imgWrapper.addClass("floated-image-wrapper");
            }


        elToMove.addClass("centered-image");
        var imageDescription = $("<span></span>")
                             .text(self.attr("alt"))
                             .addClass("image-desc")
                             .appendTo(imgWrapper)
        console.log(imageDescription)


    })

};



$textarea.autogrow();
$sidepanelToggler.pageslide();
$miniIcons.tooltip();
$editingButtons.tooltip();
$gallery.masonry({
    columnWidth: 200,
    itemSelector: '.image-gallery-wrapper',
    gutter: 12
})
})


