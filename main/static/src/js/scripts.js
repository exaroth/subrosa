/*!
 * jQuery Color Animations v@VERSION
 * https://github.com/jquery/jquery-color
 *
 * Copyright 2013 jQuery Foundation and other contributors
 * Released under the MIT license.
 * http://jquery.org/license
 *
 * Date: @DATE
 */
(function( jQuery, undefined ) {

	var stepHooks = "backgroundColor borderBottomColor borderLeftColor borderRightColor borderTopColor color columnRuleColor outlineColor textDecorationColor textEmphasisColor",

	// plusequals test for += 100 -= 100
	rplusequals = /^([\-+])=\s*(\d+\.?\d*)/,
	// a set of RE's that can match strings and generate color tuples.
	stringParsers = [{
			re: /rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*(\d?(?:\.\d+)?)\s*)?\)/,
			parse: function( execResult ) {
				return [
					execResult[ 1 ],
					execResult[ 2 ],
					execResult[ 3 ],
					execResult[ 4 ]
				];
			}
		}, {
			re: /rgba?\(\s*(\d+(?:\.\d+)?)\%\s*,\s*(\d+(?:\.\d+)?)\%\s*,\s*(\d+(?:\.\d+)?)\%\s*(?:,\s*(\d?(?:\.\d+)?)\s*)?\)/,
			parse: function( execResult ) {
				return [
					execResult[ 1 ] * 2.55,
					execResult[ 2 ] * 2.55,
					execResult[ 3 ] * 2.55,
					execResult[ 4 ]
				];
			}
		}, {
			// this regex ignores A-F because it's compared against an already lowercased string
			re: /#([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})/,
			parse: function( execResult ) {
				return [
					parseInt( execResult[ 1 ], 16 ),
					parseInt( execResult[ 2 ], 16 ),
					parseInt( execResult[ 3 ], 16 )
				];
			}
		}, {
			// this regex ignores A-F because it's compared against an already lowercased string
			re: /#([a-f0-9])([a-f0-9])([a-f0-9])/,
			parse: function( execResult ) {
				return [
					parseInt( execResult[ 1 ] + execResult[ 1 ], 16 ),
					parseInt( execResult[ 2 ] + execResult[ 2 ], 16 ),
					parseInt( execResult[ 3 ] + execResult[ 3 ], 16 )
				];
			}
		}, {
			re: /hsla?\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\%\s*,\s*(\d+(?:\.\d+)?)\%\s*(?:,\s*(\d?(?:\.\d+)?)\s*)?\)/,
			space: "hsla",
			parse: function( execResult ) {
				return [
					execResult[ 1 ],
					execResult[ 2 ] / 100,
					execResult[ 3 ] / 100,
					execResult[ 4 ]
				];
			}
		}],

	// jQuery.Color( )
	color = jQuery.Color = function( color, green, blue, alpha ) {
		return new jQuery.Color.fn.parse( color, green, blue, alpha );
	},
	spaces = {
		rgba: {
			props: {
				red: {
					idx: 0,
					type: "byte"
				},
				green: {
					idx: 1,
					type: "byte"
				},
				blue: {
					idx: 2,
					type: "byte"
				}
			}
		},

		hsla: {
			props: {
				hue: {
					idx: 0,
					type: "degrees"
				},
				saturation: {
					idx: 1,
					type: "percent"
				},
				lightness: {
					idx: 2,
					type: "percent"
				}
			}
		}
	},
	propTypes = {
		"byte": {
			floor: true,
			max: 255
		},
		"percent": {
			max: 1
		},
		"degrees": {
			mod: 360,
			floor: true
		}
	},
	support = color.support = {},

	// element for support tests
	supportElem = jQuery( "<p>" )[ 0 ],

	// colors = jQuery.Color.names
	colors,

	// local aliases of functions called often
	each = jQuery.each;

// determine rgba support immediately
supportElem.style.cssText = "background-color:rgba(1,1,1,.5)";
support.rgba = supportElem.style.backgroundColor.indexOf( "rgba" ) > -1;

// define cache name and alpha properties
// for rgba and hsla spaces
each( spaces, function( spaceName, space ) {
	space.cache = "_" + spaceName;
	space.props.alpha = {
		idx: 3,
		type: "percent",
		def: 1
	};
});

function clamp( value, prop, allowEmpty ) {
	var type = propTypes[ prop.type ] || {};

	if ( value == null ) {
		return (allowEmpty || !prop.def) ? null : prop.def;
	}

	// ~~ is an short way of doing floor for positive numbers
	value = type.floor ? ~~value : parseFloat( value );

	// IE will pass in empty strings as value for alpha,
	// which will hit this case
	if ( isNaN( value ) ) {
		return prop.def;
	}

	if ( type.mod ) {
		// we add mod before modding to make sure that negatives values
		// get converted properly: -10 -> 350
		return (value + type.mod) % type.mod;
	}

	// for now all property types without mod have min and max
	return 0 > value ? 0 : type.max < value ? type.max : value;
}

function stringParse( string ) {
	var inst = color(),
		rgba = inst._rgba = [];

	string = string.toLowerCase();

	each( stringParsers, function( i, parser ) {
		var parsed,
			match = parser.re.exec( string ),
			values = match && parser.parse( match ),
			spaceName = parser.space || "rgba";

		if ( values ) {
			parsed = inst[ spaceName ]( values );

			// if this was an rgba parse the assignment might happen twice
			// oh well....
			inst[ spaces[ spaceName ].cache ] = parsed[ spaces[ spaceName ].cache ];
			rgba = inst._rgba = parsed._rgba;

			// exit each( stringParsers ) here because we matched
			return false;
		}
	});

	// Found a stringParser that handled it
	if ( rgba.length ) {

		// if this came from a parsed string, force "transparent" when alpha is 0
		// chrome, (and maybe others) return "transparent" as rgba(0,0,0,0)
		if ( rgba.join() === "0,0,0,0" ) {
			jQuery.extend( rgba, colors.transparent );
		}
		return inst;
	}

	// named colors
	return colors[ string ];
}

color.fn = jQuery.extend( color.prototype, {
	parse: function( red, green, blue, alpha ) {
		if ( red === undefined ) {
			this._rgba = [ null, null, null, null ];
			return this;
		}
		if ( red.jquery || red.nodeType ) {
			red = jQuery( red ).css( green );
			green = undefined;
		}

		var inst = this,
			type = jQuery.type( red ),
			rgba = this._rgba = [];

		// more than 1 argument specified - assume ( red, green, blue, alpha )
		if ( green !== undefined ) {
			red = [ red, green, blue, alpha ];
			type = "array";
		}

		if ( type === "string" ) {
			return this.parse( stringParse( red ) || colors._default );
		}

		if ( type === "array" ) {
			each( spaces.rgba.props, function( key, prop ) {
				rgba[ prop.idx ] = clamp( red[ prop.idx ], prop );
			});
			return this;
		}

		if ( type === "object" ) {
			if ( red instanceof color ) {
				each( spaces, function( spaceName, space ) {
					if ( red[ space.cache ] ) {
						inst[ space.cache ] = red[ space.cache ].slice();
					}
				});
			} else {
				each( spaces, function( spaceName, space ) {
					var cache = space.cache;
					each( space.props, function( key, prop ) {

						// if the cache doesn't exist, and we know how to convert
						if ( !inst[ cache ] && space.to ) {

							// if the value was null, we don't need to copy it
							// if the key was alpha, we don't need to copy it either
							if ( key === "alpha" || red[ key ] == null ) {
								return;
							}
							inst[ cache ] = space.to( inst._rgba );
						}

						// this is the only case where we allow nulls for ALL properties.
						// call clamp with alwaysAllowEmpty
						inst[ cache ][ prop.idx ] = clamp( red[ key ], prop, true );
					});

					// everything defined but alpha?
					if ( inst[ cache ] && jQuery.inArray( null, inst[ cache ].slice( 0, 3 ) ) < 0 ) {
						// use the default of 1
						inst[ cache ][ 3 ] = 1;
						if ( space.from ) {
							inst._rgba = space.from( inst[ cache ] );
						}
					}
				});
			}
			return this;
		}
	},
	is: function( compare ) {
		var is = color( compare ),
			same = true,
			inst = this;

		each( spaces, function( _, space ) {
			var localCache,
				isCache = is[ space.cache ];
			if (isCache) {
				localCache = inst[ space.cache ] || space.to && space.to( inst._rgba ) || [];
				each( space.props, function( _, prop ) {
					if ( isCache[ prop.idx ] != null ) {
						same = ( isCache[ prop.idx ] === localCache[ prop.idx ] );
						return same;
					}
				});
			}
			return same;
		});
		return same;
	},
	_space: function() {
		var used = [],
			inst = this;
		each( spaces, function( spaceName, space ) {
			if ( inst[ space.cache ] ) {
				used.push( spaceName );
			}
		});
		return used.pop();
	},
	transition: function( other, distance ) {
		var end = color( other ),
			spaceName = end._space(),
			space = spaces[ spaceName ],
			startColor = this.alpha() === 0 ? color( "transparent" ) : this,
			start = startColor[ space.cache ] || space.to( startColor._rgba ),
			result = start.slice();

		end = end[ space.cache ];
		each( space.props, function( key, prop ) {
			var index = prop.idx,
				startValue = start[ index ],
				endValue = end[ index ],
				type = propTypes[ prop.type ] || {};

			// if null, don't override start value
			if ( endValue === null ) {
				return;
			}
			// if null - use end
			if ( startValue === null ) {
				result[ index ] = endValue;
			} else {
				if ( type.mod ) {
					if ( endValue - startValue > type.mod / 2 ) {
						startValue += type.mod;
					} else if ( startValue - endValue > type.mod / 2 ) {
						startValue -= type.mod;
					}
				}
				result[ index ] = clamp( ( endValue - startValue ) * distance + startValue, prop );
			}
		});
		return this[ spaceName ]( result );
	},
	blend: function( opaque ) {
		// if we are already opaque - return ourself
		if ( this._rgba[ 3 ] === 1 ) {
			return this;
		}

		var rgb = this._rgba.slice(),
			a = rgb.pop(),
			blend = color( opaque )._rgba;

		return color( jQuery.map( rgb, function( v, i ) {
			return ( 1 - a ) * blend[ i ] + a * v;
		}));
	},
	toRgbaString: function() {
		var prefix = "rgba(",
			rgba = jQuery.map( this._rgba, function( v, i ) {
				return v == null ? ( i > 2 ? 1 : 0 ) : v;
			});

		if ( rgba[ 3 ] === 1 ) {
			rgba.pop();
			prefix = "rgb(";
		}

		return prefix + rgba.join() + ")";
	},
	toHslaString: function() {
		var prefix = "hsla(",
			hsla = jQuery.map( this.hsla(), function( v, i ) {
				if ( v == null ) {
					v = i > 2 ? 1 : 0;
				}

				// catch 1 and 2
				if ( i && i < 3 ) {
					v = Math.round( v * 100 ) + "%";
				}
				return v;
			});

		if ( hsla[ 3 ] === 1 ) {
			hsla.pop();
			prefix = "hsl(";
		}
		return prefix + hsla.join() + ")";
	},
	toHexString: function( includeAlpha ) {
		var rgba = this._rgba.slice(),
			alpha = rgba.pop();

		if ( includeAlpha ) {
			rgba.push( ~~( alpha * 255 ) );
		}

		return "#" + jQuery.map( rgba, function( v ) {

			// default to 0 when nulls exist
			v = ( v || 0 ).toString( 16 );
			return v.length === 1 ? "0" + v : v;
		}).join("");
	},
	toString: function() {
		return this._rgba[ 3 ] === 0 ? "transparent" : this.toRgbaString();
	}
});
color.fn.parse.prototype = color.fn;

// hsla conversions adapted from:
// https://code.google.com/p/maashaack/source/browse/packages/graphics/trunk/src/graphics/colors/HUE2RGB.as?r=5021

function hue2rgb( p, q, h ) {
	h = ( h + 1 ) % 1;
	if ( h * 6 < 1 ) {
		return p + (q - p) * h * 6;
	}
	if ( h * 2 < 1) {
		return q;
	}
	if ( h * 3 < 2 ) {
		return p + (q - p) * ((2/3) - h) * 6;
	}
	return p;
}

spaces.hsla.to = function ( rgba ) {
	if ( rgba[ 0 ] == null || rgba[ 1 ] == null || rgba[ 2 ] == null ) {
		return [ null, null, null, rgba[ 3 ] ];
	}
	var r = rgba[ 0 ] / 255,
		g = rgba[ 1 ] / 255,
		b = rgba[ 2 ] / 255,
		a = rgba[ 3 ],
		max = Math.max( r, g, b ),
		min = Math.min( r, g, b ),
		diff = max - min,
		add = max + min,
		l = add * 0.5,
		h, s;

	if ( min === max ) {
		h = 0;
	} else if ( r === max ) {
		h = ( 60 * ( g - b ) / diff ) + 360;
	} else if ( g === max ) {
		h = ( 60 * ( b - r ) / diff ) + 120;
	} else {
		h = ( 60 * ( r - g ) / diff ) + 240;
	}

	// chroma (diff) == 0 means greyscale which, by definition, saturation = 0%
	// otherwise, saturation is based on the ratio of chroma (diff) to lightness (add)
	if ( diff === 0 ) {
		s = 0;
	} else if ( l <= 0.5 ) {
		s = diff / add;
	} else {
		s = diff / ( 2 - add );
	}
	return [ Math.round(h) % 360, s, l, a == null ? 1 : a ];
};

spaces.hsla.from = function ( hsla ) {
	if ( hsla[ 0 ] == null || hsla[ 1 ] == null || hsla[ 2 ] == null ) {
		return [ null, null, null, hsla[ 3 ] ];
	}
	var h = hsla[ 0 ] / 360,
		s = hsla[ 1 ],
		l = hsla[ 2 ],
		a = hsla[ 3 ],
		q = l <= 0.5 ? l * ( 1 + s ) : l + s - l * s,
		p = 2 * l - q;

	return [
		Math.round( hue2rgb( p, q, h + ( 1 / 3 ) ) * 255 ),
		Math.round( hue2rgb( p, q, h ) * 255 ),
		Math.round( hue2rgb( p, q, h - ( 1 / 3 ) ) * 255 ),
		a
	];
};


each( spaces, function( spaceName, space ) {
	var props = space.props,
		cache = space.cache,
		to = space.to,
		from = space.from;

	// makes rgba() and hsla()
	color.fn[ spaceName ] = function( value ) {

		// generate a cache for this space if it doesn't exist
		if ( to && !this[ cache ] ) {
			this[ cache ] = to( this._rgba );
		}
		if ( value === undefined ) {
			return this[ cache ].slice();
		}

		var ret,
			type = jQuery.type( value ),
			arr = ( type === "array" || type === "object" ) ? value : arguments,
			local = this[ cache ].slice();

		each( props, function( key, prop ) {
			var val = arr[ type === "object" ? key : prop.idx ];
			if ( val == null ) {
				val = local[ prop.idx ];
			}
			local[ prop.idx ] = clamp( val, prop );
		});

		if ( from ) {
			ret = color( from( local ) );
			ret[ cache ] = local;
			return ret;
		} else {
			return color( local );
		}
	};

	// makes red() green() blue() alpha() hue() saturation() lightness()
	each( props, function( key, prop ) {
		// alpha is included in more than one space
		if ( color.fn[ key ] ) {
			return;
		}
		color.fn[ key ] = function( value ) {
			var vtype = jQuery.type( value ),
				fn = ( key === "alpha" ? ( this._hsla ? "hsla" : "rgba" ) : spaceName ),
				local = this[ fn ](),
				cur = local[ prop.idx ],
				match;

			if ( vtype === "undefined" ) {
				return cur;
			}

			if ( vtype === "function" ) {
				value = value.call( this, cur );
				vtype = jQuery.type( value );
			}
			if ( value == null && prop.empty ) {
				return this;
			}
			if ( vtype === "string" ) {
				match = rplusequals.exec( value );
				if ( match ) {
					value = cur + parseFloat( match[ 2 ] ) * ( match[ 1 ] === "+" ? 1 : -1 );
				}
			}
			local[ prop.idx ] = value;
			return this[ fn ]( local );
		};
	});
});

// add cssHook and .fx.step function for each named hook.
// accept a space separated string of properties
color.hook = function( hook ) {
	var hooks = hook.split( " " );
	each( hooks, function( i, hook ) {
		jQuery.cssHooks[ hook ] = {
			set: function( elem, value ) {
				var parsed, curElem,
					backgroundColor = "";

				if ( value !== "transparent" && ( jQuery.type( value ) !== "string" || ( parsed = stringParse( value ) ) ) ) {
					value = color( parsed || value );
					if ( !support.rgba && value._rgba[ 3 ] !== 1 ) {
						curElem = hook === "backgroundColor" ? elem.parentNode : elem;
						while (
							(backgroundColor === "" || backgroundColor === "transparent") &&
							curElem && curElem.style
						) {
							try {
								backgroundColor = jQuery.css( curElem, "backgroundColor" );
								curElem = curElem.parentNode;
							} catch ( e ) {
							}
						}

						value = value.blend( backgroundColor && backgroundColor !== "transparent" ?
							backgroundColor :
							"_default" );
					}

					value = value.toRgbaString();
				}
				try {
					elem.style[ hook ] = value;
				} catch( e ) {
					// wrapped to prevent IE from throwing errors on "invalid" values like 'auto' or 'inherit'
				}
			}
		};
		jQuery.fx.step[ hook ] = function( fx ) {
			if ( !fx.colorInit ) {
				fx.start = color( fx.elem, hook );
				fx.end = color( fx.end );
				fx.colorInit = true;
			}
			jQuery.cssHooks[ hook ].set( fx.elem, fx.start.transition( fx.end, fx.pos ) );
		};
	});

};

color.hook( stepHooks );

jQuery.cssHooks.borderColor = {
	expand: function( value ) {
		var expanded = {};

		each( [ "Top", "Right", "Bottom", "Left" ], function( i, part ) {
			expanded[ "border" + part + "Color" ] = value;
		});
		return expanded;
	}
};

// Basic color names only.
// Usage of any of the other color names requires adding yourself or including
// jquery.color.svg-names.js.
colors = jQuery.Color.names = {
	// 4.1. Basic color keywords
	aqua: "#00ffff",
	black: "#000000",
	blue: "#0000ff",
	fuchsia: "#ff00ff",
	gray: "#808080",
	green: "#008000",
	lime: "#00ff00",
	maroon: "#800000",
	navy: "#000080",
	olive: "#808000",
	purple: "#800080",
	red: "#ff0000",
	silver: "#c0c0c0",
	teal: "#008080",
	white: "#ffffff",
	yellow: "#ffff00",

	// 4.2.3. "transparent" color keyword
	transparent: [ null, null, null, 0 ],

	_default: "#ffffff"
};

})( jQuery );
;/* ========================================================================
 * Bootstrap: alert.js v3.1.1
 * http://getbootstrap.com/javascript/#alerts
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // ALERT CLASS DEFINITION
  // ======================

  var dismiss = '[data-dismiss="alert"]'
  var Alert   = function (el) {
    $(el).on('click', dismiss, this.close)
  }

  Alert.prototype.close = function (e) {
    var $this    = $(this)
    var selector = $this.attr('data-target')

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
    }

    var $parent = $(selector)

    if (e) e.preventDefault()

    if (!$parent.length) {
      $parent = $this.hasClass('alert') ? $this : $this.parent()
    }

    $parent.trigger(e = $.Event('close.bs.alert'))

    if (e.isDefaultPrevented()) return

    $parent.removeClass('in')

    function removeElement() {
      $parent.trigger('closed.bs.alert').remove()
    }

    $.support.transition && $parent.hasClass('fade') ?
      $parent
        .one($.support.transition.end, removeElement)
        .emulateTransitionEnd(150) :
      removeElement()
  }


  // ALERT PLUGIN DEFINITION
  // =======================

  var old = $.fn.alert

  $.fn.alert = function (option) {
    return this.each(function () {
      var $this = $(this)
      var data  = $this.data('bs.alert')

      if (!data) $this.data('bs.alert', (data = new Alert(this)))
      if (typeof option == 'string') data[option].call($this)
    })
  }

  $.fn.alert.Constructor = Alert


  // ALERT NO CONFLICT
  // =================

  $.fn.alert.noConflict = function () {
    $.fn.alert = old
    return this
  }


  // ALERT DATA-API
  // ==============

  $(document).on('click.bs.alert.data-api', dismiss, Alert.prototype.close)

}(jQuery);
;/* ========================================================================
 * Bootstrap: tooltip.js v3.1.1
 * http://getbootstrap.com/javascript/#tooltip
 * Inspired by the original jQuery.tipsy by Jason Frame
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // TOOLTIP PUBLIC CLASS DEFINITION
  // ===============================

  var Tooltip = function (element, options) {
    this.type       =
    this.options    =
    this.enabled    =
    this.timeout    =
    this.hoverState =
    this.$element   = null

    this.init('tooltip', element, options)
  }

  Tooltip.DEFAULTS = {
    animation: true,
    placement: 'top',
    selector: false,
    template: '<div class="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',
    trigger: 'hover focus',
    title: '',
    delay: 0,
    html: false,
    container: false
  }

  Tooltip.prototype.init = function (type, element, options) {
    this.enabled  = true
    this.type     = type
    this.$element = $(element)
    this.options  = this.getOptions(options)

    var triggers = this.options.trigger.split(' ')

    for (var i = triggers.length; i--;) {
      var trigger = triggers[i]

      if (trigger == 'click') {
        this.$element.on('click.' + this.type, this.options.selector, $.proxy(this.toggle, this))
      } else if (trigger != 'manual') {
        var eventIn  = trigger == 'hover' ? 'mouseenter' : 'focusin'
        var eventOut = trigger == 'hover' ? 'mouseleave' : 'focusout'

        this.$element.on(eventIn  + '.' + this.type, this.options.selector, $.proxy(this.enter, this))
        this.$element.on(eventOut + '.' + this.type, this.options.selector, $.proxy(this.leave, this))
      }
    }

    this.options.selector ?
      (this._options = $.extend({}, this.options, { trigger: 'manual', selector: '' })) :
      this.fixTitle()
  }

  Tooltip.prototype.getDefaults = function () {
    return Tooltip.DEFAULTS
  }

  Tooltip.prototype.getOptions = function (options) {
    options = $.extend({}, this.getDefaults(), this.$element.data(), options)

    if (options.delay && typeof options.delay == 'number') {
      options.delay = {
        show: options.delay,
        hide: options.delay
      }
    }

    return options
  }

  Tooltip.prototype.getDelegateOptions = function () {
    var options  = {}
    var defaults = this.getDefaults()

    this._options && $.each(this._options, function (key, value) {
      if (defaults[key] != value) options[key] = value
    })

    return options
  }

  Tooltip.prototype.enter = function (obj) {
    var self = obj instanceof this.constructor ?
      obj : $(obj.currentTarget)[this.type](this.getDelegateOptions()).data('bs.' + this.type)

    clearTimeout(self.timeout)

    self.hoverState = 'in'

    if (!self.options.delay || !self.options.delay.show) return self.show()

    self.timeout = setTimeout(function () {
      if (self.hoverState == 'in') self.show()
    }, self.options.delay.show)
  }

  Tooltip.prototype.leave = function (obj) {
    var self = obj instanceof this.constructor ?
      obj : $(obj.currentTarget)[this.type](this.getDelegateOptions()).data('bs.' + this.type)

    clearTimeout(self.timeout)

    self.hoverState = 'out'

    if (!self.options.delay || !self.options.delay.hide) return self.hide()

    self.timeout = setTimeout(function () {
      if (self.hoverState == 'out') self.hide()
    }, self.options.delay.hide)
  }

  Tooltip.prototype.show = function () {
    var e = $.Event('show.bs.' + this.type)

    if (this.hasContent() && this.enabled) {
      this.$element.trigger(e)

      if (e.isDefaultPrevented()) return
      var that = this;

      var $tip = this.tip()

      this.setContent()

      if (this.options.animation) $tip.addClass('fade')

      var placement = typeof this.options.placement == 'function' ?
        this.options.placement.call(this, $tip[0], this.$element[0]) :
        this.options.placement

      var autoToken = /\s?auto?\s?/i
      var autoPlace = autoToken.test(placement)
      if (autoPlace) placement = placement.replace(autoToken, '') || 'top'

      $tip
        .detach()
        .css({ top: 0, left: 0, display: 'block' })
        .addClass(placement)

      this.options.container ? $tip.appendTo(this.options.container) : $tip.insertAfter(this.$element)

      var pos          = this.getPosition()
      var actualWidth  = $tip[0].offsetWidth
      var actualHeight = $tip[0].offsetHeight

      if (autoPlace) {
        var $parent = this.$element.parent()

        var orgPlacement = placement
        var docScroll    = document.documentElement.scrollTop || document.body.scrollTop
        var parentWidth  = this.options.container == 'body' ? window.innerWidth  : $parent.outerWidth()
        var parentHeight = this.options.container == 'body' ? window.innerHeight : $parent.outerHeight()
        var parentLeft   = this.options.container == 'body' ? 0 : $parent.offset().left

        placement = placement == 'bottom' && pos.top   + pos.height  + actualHeight - docScroll > parentHeight  ? 'top'    :
                    placement == 'top'    && pos.top   - docScroll   - actualHeight < 0                         ? 'bottom' :
                    placement == 'right'  && pos.right + actualWidth > parentWidth                              ? 'left'   :
                    placement == 'left'   && pos.left  - actualWidth < parentLeft                               ? 'right'  :
                    placement

        $tip
          .removeClass(orgPlacement)
          .addClass(placement)
      }

      var calculatedOffset = this.getCalculatedOffset(placement, pos, actualWidth, actualHeight)

      this.applyPlacement(calculatedOffset, placement)
      this.hoverState = null

      var complete = function() {
        that.$element.trigger('shown.bs.' + that.type)
      }

      $.support.transition && this.$tip.hasClass('fade') ?
        $tip
          .one($.support.transition.end, complete)
          .emulateTransitionEnd(150) :
        complete()
    }
  }

  Tooltip.prototype.applyPlacement = function (offset, placement) {
    var replace
    var $tip   = this.tip()
    var width  = $tip[0].offsetWidth
    var height = $tip[0].offsetHeight

    // manually read margins because getBoundingClientRect includes difference
    var marginTop = parseInt($tip.css('margin-top'), 10)
    var marginLeft = parseInt($tip.css('margin-left'), 10)

    // we must check for NaN for ie 8/9
    if (isNaN(marginTop))  marginTop  = 0
    if (isNaN(marginLeft)) marginLeft = 0

    offset.top  = offset.top  + marginTop
    offset.left = offset.left + marginLeft

    // $.fn.offset doesn't round pixel values
    // so we use setOffset directly with our own function B-0
    $.offset.setOffset($tip[0], $.extend({
      using: function (props) {
        $tip.css({
          top: Math.round(props.top),
          left: Math.round(props.left)
        })
      }
    }, offset), 0)

    $tip.addClass('in')

    // check to see if placing tip in new offset caused the tip to resize itself
    var actualWidth  = $tip[0].offsetWidth
    var actualHeight = $tip[0].offsetHeight

    if (placement == 'top' && actualHeight != height) {
      replace = true
      offset.top = offset.top + height - actualHeight
    }

    if (/bottom|top/.test(placement)) {
      var delta = 0

      if (offset.left < 0) {
        delta       = offset.left * -2
        offset.left = 0

        $tip.offset(offset)

        actualWidth  = $tip[0].offsetWidth
        actualHeight = $tip[0].offsetHeight
      }

      this.replaceArrow(delta - width + actualWidth, actualWidth, 'left')
    } else {
      this.replaceArrow(actualHeight - height, actualHeight, 'top')
    }

    if (replace) $tip.offset(offset)
  }

  Tooltip.prototype.replaceArrow = function (delta, dimension, position) {
    this.arrow().css(position, delta ? (50 * (1 - delta / dimension) + '%') : '')
  }

  Tooltip.prototype.setContent = function () {
    var $tip  = this.tip()
    var title = this.getTitle()

    $tip.find('.tooltip-inner')[this.options.html ? 'html' : 'text'](title)
    $tip.removeClass('fade in top bottom left right')
  }

  Tooltip.prototype.hide = function () {
    var that = this
    var $tip = this.tip()
    var e    = $.Event('hide.bs.' + this.type)

    function complete() {
      if (that.hoverState != 'in') $tip.detach()
      that.$element.trigger('hidden.bs.' + that.type)
    }

    this.$element.trigger(e)

    if (e.isDefaultPrevented()) return

    $tip.removeClass('in')

    $.support.transition && this.$tip.hasClass('fade') ?
      $tip
        .one($.support.transition.end, complete)
        .emulateTransitionEnd(150) :
      complete()

    this.hoverState = null

    return this
  }

  Tooltip.prototype.fixTitle = function () {
    var $e = this.$element
    if ($e.attr('title') || typeof($e.attr('data-original-title')) != 'string') {
      $e.attr('data-original-title', $e.attr('title') || '').attr('title', '')
    }
  }

  Tooltip.prototype.hasContent = function () {
    return this.getTitle()
  }

  Tooltip.prototype.getPosition = function () {
    var el = this.$element[0]
    return $.extend({}, (typeof el.getBoundingClientRect == 'function') ? el.getBoundingClientRect() : {
      width: el.offsetWidth,
      height: el.offsetHeight
    }, this.$element.offset())
  }

  Tooltip.prototype.getCalculatedOffset = function (placement, pos, actualWidth, actualHeight) {
    return placement == 'bottom' ? { top: pos.top + pos.height,   left: pos.left + pos.width / 2 - actualWidth / 2  } :
           placement == 'top'    ? { top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2  } :
           placement == 'left'   ? { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth } :
        /* placement == 'right' */ { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width   }
  }

  Tooltip.prototype.getTitle = function () {
    var title
    var $e = this.$element
    var o  = this.options

    title = $e.attr('data-original-title')
      || (typeof o.title == 'function' ? o.title.call($e[0]) :  o.title)

    return title
  }

  Tooltip.prototype.tip = function () {
    return this.$tip = this.$tip || $(this.options.template)
  }

  Tooltip.prototype.arrow = function () {
    return this.$arrow = this.$arrow || this.tip().find('.tooltip-arrow')
  }

  Tooltip.prototype.validate = function () {
    if (!this.$element[0].parentNode) {
      this.hide()
      this.$element = null
      this.options  = null
    }
  }

  Tooltip.prototype.enable = function () {
    this.enabled = true
  }

  Tooltip.prototype.disable = function () {
    this.enabled = false
  }

  Tooltip.prototype.toggleEnabled = function () {
    this.enabled = !this.enabled
  }

  Tooltip.prototype.toggle = function (e) {
    var self = e ? $(e.currentTarget)[this.type](this.getDelegateOptions()).data('bs.' + this.type) : this
    self.tip().hasClass('in') ? self.leave(self) : self.enter(self)
  }

  Tooltip.prototype.destroy = function () {
    clearTimeout(this.timeout)
    this.hide().$element.off('.' + this.type).removeData('bs.' + this.type)
  }


  // TOOLTIP PLUGIN DEFINITION
  // =========================

  var old = $.fn.tooltip

  $.fn.tooltip = function (option) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.tooltip')
      var options = typeof option == 'object' && option

      if (!data && option == 'destroy') return
      if (!data) $this.data('bs.tooltip', (data = new Tooltip(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.tooltip.Constructor = Tooltip


  // TOOLTIP NO CONFLICT
  // ===================

  $.fn.tooltip.noConflict = function () {
    $.fn.tooltip = old
    return this
  }

}(jQuery);
;/*! Magnific Popup - v0.9.9 - 2013-11-15
* http://dimsemenov.com/plugins/magnific-popup/
* Copyright (c) 2013 Dmitry Semenov; */
(function(e){var t,n,i,o,r,a,s,l="Close",c="BeforeClose",d="AfterClose",u="BeforeAppend",p="MarkupParse",f="Open",m="Change",g="mfp",v="."+g,h="mfp-ready",C="mfp-removing",y="mfp-prevent-close",w=function(){},b=!!window.jQuery,I=e(window),x=function(e,n){t.ev.on(g+e+v,n)},k=function(t,n,i,o){var r=document.createElement("div");return r.className="mfp-"+t,i&&(r.innerHTML=i),o?n&&n.appendChild(r):(r=e(r),n&&r.appendTo(n)),r},T=function(n,i){t.ev.triggerHandler(g+n,i),t.st.callbacks&&(n=n.charAt(0).toLowerCase()+n.slice(1),t.st.callbacks[n]&&t.st.callbacks[n].apply(t,e.isArray(i)?i:[i]))},E=function(n){return n===s&&t.currTemplate.closeBtn||(t.currTemplate.closeBtn=e(t.st.closeMarkup.replace("%title%",t.st.tClose)),s=n),t.currTemplate.closeBtn},_=function(){e.magnificPopup.instance||(t=new w,t.init(),e.magnificPopup.instance=t)},S=function(){var e=document.createElement("p").style,t=["ms","O","Moz","Webkit"];if(void 0!==e.transition)return!0;for(;t.length;)if(t.pop()+"Transition"in e)return!0;return!1};w.prototype={constructor:w,init:function(){var n=navigator.appVersion;t.isIE7=-1!==n.indexOf("MSIE 7."),t.isIE8=-1!==n.indexOf("MSIE 8."),t.isLowIE=t.isIE7||t.isIE8,t.isAndroid=/android/gi.test(n),t.isIOS=/iphone|ipad|ipod/gi.test(n),t.supportsTransition=S(),t.probablyMobile=t.isAndroid||t.isIOS||/(Opera Mini)|Kindle|webOS|BlackBerry|(Opera Mobi)|(Windows Phone)|IEMobile/i.test(navigator.userAgent),i=e(document.body),o=e(document),t.popupsCache={}},open:function(n){var i;if(n.isObj===!1){t.items=n.items.toArray(),t.index=0;var r,s=n.items;for(i=0;s.length>i;i++)if(r=s[i],r.parsed&&(r=r.el[0]),r===n.el[0]){t.index=i;break}}else t.items=e.isArray(n.items)?n.items:[n.items],t.index=n.index||0;if(t.isOpen)return t.updateItemHTML(),void 0;t.types=[],a="",t.ev=n.mainEl&&n.mainEl.length?n.mainEl.eq(0):o,n.key?(t.popupsCache[n.key]||(t.popupsCache[n.key]={}),t.currTemplate=t.popupsCache[n.key]):t.currTemplate={},t.st=e.extend(!0,{},e.magnificPopup.defaults,n),t.fixedContentPos="auto"===t.st.fixedContentPos?!t.probablyMobile:t.st.fixedContentPos,t.st.modal&&(t.st.closeOnContentClick=!1,t.st.closeOnBgClick=!1,t.st.showCloseBtn=!1,t.st.enableEscapeKey=!1),t.bgOverlay||(t.bgOverlay=k("bg").on("click"+v,function(){t.close()}),t.wrap=k("wrap").attr("tabindex",-1).on("click"+v,function(e){t._checkIfClose(e.target)&&t.close()}),t.container=k("container",t.wrap)),t.contentContainer=k("content"),t.st.preloader&&(t.preloader=k("preloader",t.container,t.st.tLoading));var l=e.magnificPopup.modules;for(i=0;l.length>i;i++){var c=l[i];c=c.charAt(0).toUpperCase()+c.slice(1),t["init"+c].call(t)}T("BeforeOpen"),t.st.showCloseBtn&&(t.st.closeBtnInside?(x(p,function(e,t,n,i){n.close_replaceWith=E(i.type)}),a+=" mfp-close-btn-in"):t.wrap.append(E())),t.st.alignTop&&(a+=" mfp-align-top"),t.fixedContentPos?t.wrap.css({overflow:t.st.overflowY,overflowX:"hidden",overflowY:t.st.overflowY}):t.wrap.css({top:I.scrollTop(),position:"absolute"}),(t.st.fixedBgPos===!1||"auto"===t.st.fixedBgPos&&!t.fixedContentPos)&&t.bgOverlay.css({height:o.height(),position:"absolute"}),t.st.enableEscapeKey&&o.on("keyup"+v,function(e){27===e.keyCode&&t.close()}),I.on("resize"+v,function(){t.updateSize()}),t.st.closeOnContentClick||(a+=" mfp-auto-cursor"),a&&t.wrap.addClass(a);var d=t.wH=I.height(),u={};if(t.fixedContentPos&&t._hasScrollBar(d)){var m=t._getScrollbarSize();m&&(u.marginRight=m)}t.fixedContentPos&&(t.isIE7?e("body, html").css("overflow","hidden"):u.overflow="hidden");var g=t.st.mainClass;return t.isIE7&&(g+=" mfp-ie7"),g&&t._addClassToMFP(g),t.updateItemHTML(),T("BuildControls"),e("html").css(u),t.bgOverlay.add(t.wrap).prependTo(document.body),t._lastFocusedEl=document.activeElement,setTimeout(function(){t.content?(t._addClassToMFP(h),t._setFocus()):t.bgOverlay.addClass(h),o.on("focusin"+v,t._onFocusIn)},16),t.isOpen=!0,t.updateSize(d),T(f),n},close:function(){t.isOpen&&(T(c),t.isOpen=!1,t.st.removalDelay&&!t.isLowIE&&t.supportsTransition?(t._addClassToMFP(C),setTimeout(function(){t._close()},t.st.removalDelay)):t._close())},_close:function(){T(l);var n=C+" "+h+" ";if(t.bgOverlay.detach(),t.wrap.detach(),t.container.empty(),t.st.mainClass&&(n+=t.st.mainClass+" "),t._removeClassFromMFP(n),t.fixedContentPos){var i={marginRight:""};t.isIE7?e("body, html").css("overflow",""):i.overflow="",e("html").css(i)}o.off("keyup"+v+" focusin"+v),t.ev.off(v),t.wrap.attr("class","mfp-wrap").removeAttr("style"),t.bgOverlay.attr("class","mfp-bg"),t.container.attr("class","mfp-container"),!t.st.showCloseBtn||t.st.closeBtnInside&&t.currTemplate[t.currItem.type]!==!0||t.currTemplate.closeBtn&&t.currTemplate.closeBtn.detach(),t._lastFocusedEl&&e(t._lastFocusedEl).focus(),t.currItem=null,t.content=null,t.currTemplate=null,t.prevHeight=0,T(d)},updateSize:function(e){if(t.isIOS){var n=document.documentElement.clientWidth/window.innerWidth,i=window.innerHeight*n;t.wrap.css("height",i),t.wH=i}else t.wH=e||I.height();t.fixedContentPos||t.wrap.css("height",t.wH),T("Resize")},updateItemHTML:function(){var n=t.items[t.index];t.contentContainer.detach(),t.content&&t.content.detach(),n.parsed||(n=t.parseEl(t.index));var i=n.type;if(T("BeforeChange",[t.currItem?t.currItem.type:"",i]),t.currItem=n,!t.currTemplate[i]){var o=t.st[i]?t.st[i].markup:!1;T("FirstMarkupParse",o),t.currTemplate[i]=o?e(o):!0}r&&r!==n.type&&t.container.removeClass("mfp-"+r+"-holder");var a=t["get"+i.charAt(0).toUpperCase()+i.slice(1)](n,t.currTemplate[i]);t.appendContent(a,i),n.preloaded=!0,T(m,n),r=n.type,t.container.prepend(t.contentContainer),T("AfterChange")},appendContent:function(e,n){t.content=e,e?t.st.showCloseBtn&&t.st.closeBtnInside&&t.currTemplate[n]===!0?t.content.find(".mfp-close").length||t.content.append(E()):t.content=e:t.content="",T(u),t.container.addClass("mfp-"+n+"-holder"),t.contentContainer.append(t.content)},parseEl:function(n){var i=t.items[n],o=i.type;if(i=i.tagName?{el:e(i)}:{data:i,src:i.src},i.el){for(var r=t.types,a=0;r.length>a;a++)if(i.el.hasClass("mfp-"+r[a])){o=r[a];break}i.src=i.el.attr("data-mfp-src"),i.src||(i.src=i.el.attr("href"))}return i.type=o||t.st.type||"inline",i.index=n,i.parsed=!0,t.items[n]=i,T("ElementParse",i),t.items[n]},addGroup:function(e,n){var i=function(i){i.mfpEl=this,t._openClick(i,e,n)};n||(n={});var o="click.magnificPopup";n.mainEl=e,n.items?(n.isObj=!0,e.off(o).on(o,i)):(n.isObj=!1,n.delegate?e.off(o).on(o,n.delegate,i):(n.items=e,e.off(o).on(o,i)))},_openClick:function(n,i,o){var r=void 0!==o.midClick?o.midClick:e.magnificPopup.defaults.midClick;if(r||2!==n.which&&!n.ctrlKey&&!n.metaKey){var a=void 0!==o.disableOn?o.disableOn:e.magnificPopup.defaults.disableOn;if(a)if(e.isFunction(a)){if(!a.call(t))return!0}else if(a>I.width())return!0;n.type&&(n.preventDefault(),t.isOpen&&n.stopPropagation()),o.el=e(n.mfpEl),o.delegate&&(o.items=i.find(o.delegate)),t.open(o)}},updateStatus:function(e,i){if(t.preloader){n!==e&&t.container.removeClass("mfp-s-"+n),i||"loading"!==e||(i=t.st.tLoading);var o={status:e,text:i};T("UpdateStatus",o),e=o.status,i=o.text,t.preloader.html(i),t.preloader.find("a").on("click",function(e){e.stopImmediatePropagation()}),t.container.addClass("mfp-s-"+e),n=e}},_checkIfClose:function(n){if(!e(n).hasClass(y)){var i=t.st.closeOnContentClick,o=t.st.closeOnBgClick;if(i&&o)return!0;if(!t.content||e(n).hasClass("mfp-close")||t.preloader&&n===t.preloader[0])return!0;if(n===t.content[0]||e.contains(t.content[0],n)){if(i)return!0}else if(o&&e.contains(document,n))return!0;return!1}},_addClassToMFP:function(e){t.bgOverlay.addClass(e),t.wrap.addClass(e)},_removeClassFromMFP:function(e){this.bgOverlay.removeClass(e),t.wrap.removeClass(e)},_hasScrollBar:function(e){return(t.isIE7?o.height():document.body.scrollHeight)>(e||I.height())},_setFocus:function(){(t.st.focus?t.content.find(t.st.focus).eq(0):t.wrap).focus()},_onFocusIn:function(n){return n.target===t.wrap[0]||e.contains(t.wrap[0],n.target)?void 0:(t._setFocus(),!1)},_parseMarkup:function(t,n,i){var o;i.data&&(n=e.extend(i.data,n)),T(p,[t,n,i]),e.each(n,function(e,n){if(void 0===n||n===!1)return!0;if(o=e.split("_"),o.length>1){var i=t.find(v+"-"+o[0]);if(i.length>0){var r=o[1];"replaceWith"===r?i[0]!==n[0]&&i.replaceWith(n):"img"===r?i.is("img")?i.attr("src",n):i.replaceWith('<img src="'+n+'" class="'+i.attr("class")+'" />'):i.attr(o[1],n)}}else t.find(v+"-"+e).html(n)})},_getScrollbarSize:function(){if(void 0===t.scrollbarSize){var e=document.createElement("div");e.id="mfp-sbm",e.style.cssText="width: 99px; height: 99px; overflow: scroll; position: absolute; top: -9999px;",document.body.appendChild(e),t.scrollbarSize=e.offsetWidth-e.clientWidth,document.body.removeChild(e)}return t.scrollbarSize}},e.magnificPopup={instance:null,proto:w.prototype,modules:[],open:function(t,n){return _(),t=t?e.extend(!0,{},t):{},t.isObj=!0,t.index=n||0,this.instance.open(t)},close:function(){return e.magnificPopup.instance&&e.magnificPopup.instance.close()},registerModule:function(t,n){n.options&&(e.magnificPopup.defaults[t]=n.options),e.extend(this.proto,n.proto),this.modules.push(t)},defaults:{disableOn:0,key:null,midClick:!1,mainClass:"",preloader:!0,focus:"",closeOnContentClick:!1,closeOnBgClick:!0,closeBtnInside:!0,showCloseBtn:!0,enableEscapeKey:!0,modal:!1,alignTop:!1,removalDelay:0,fixedContentPos:"auto",fixedBgPos:"auto",overflowY:"auto",closeMarkup:'<button title="%title%" type="button" class="mfp-close">&times;</button>',tClose:"Close (Esc)",tLoading:"Loading..."}},e.fn.magnificPopup=function(n){_();var i=e(this);if("string"==typeof n)if("open"===n){var o,r=b?i.data("magnificPopup"):i[0].magnificPopup,a=parseInt(arguments[1],10)||0;r.items?o=r.items[a]:(o=i,r.delegate&&(o=o.find(r.delegate)),o=o.eq(a)),t._openClick({mfpEl:o},i,r)}else t.isOpen&&t[n].apply(t,Array.prototype.slice.call(arguments,1));else n=e.extend(!0,{},n),b?i.data("magnificPopup",n):i[0].magnificPopup=n,t.addGroup(i,n);return i};var P,O,z,M="inline",B=function(){z&&(O.after(z.addClass(P)).detach(),z=null)};e.magnificPopup.registerModule(M,{options:{hiddenClass:"hide",markup:"",tNotFound:"Content not found"},proto:{initInline:function(){t.types.push(M),x(l+"."+M,function(){B()})},getInline:function(n,i){if(B(),n.src){var o=t.st.inline,r=e(n.src);if(r.length){var a=r[0].parentNode;a&&a.tagName&&(O||(P=o.hiddenClass,O=k(P),P="mfp-"+P),z=r.after(O).detach().removeClass(P)),t.updateStatus("ready")}else t.updateStatus("error",o.tNotFound),r=e("<div>");return n.inlineElement=r,r}return t.updateStatus("ready"),t._parseMarkup(i,{},n),i}}});var F,H="ajax",L=function(){F&&i.removeClass(F)},A=function(){L(),t.req&&t.req.abort()};e.magnificPopup.registerModule(H,{options:{settings:null,cursor:"mfp-ajax-cur",tError:'<a href="%url%">The content</a> could not be loaded.'},proto:{initAjax:function(){t.types.push(H),F=t.st.ajax.cursor,x(l+"."+H,A),x("BeforeChange."+H,A)},getAjax:function(n){F&&i.addClass(F),t.updateStatus("loading");var o=e.extend({url:n.src,success:function(i,o,r){var a={data:i,xhr:r};T("ParseAjax",a),t.appendContent(e(a.data),H),n.finished=!0,L(),t._setFocus(),setTimeout(function(){t.wrap.addClass(h)},16),t.updateStatus("ready"),T("AjaxContentAdded")},error:function(){L(),n.finished=n.loadError=!0,t.updateStatus("error",t.st.ajax.tError.replace("%url%",n.src))}},t.st.ajax.settings);return t.req=e.ajax(o),""}}});var j,N=function(n){if(n.data&&void 0!==n.data.title)return n.data.title;var i=t.st.image.titleSrc;if(i){if(e.isFunction(i))return i.call(t,n);if(n.el)return n.el.attr(i)||""}return""};e.magnificPopup.registerModule("image",{options:{markup:'<div class="mfp-figure"><div class="mfp-close"></div><figure><div class="mfp-img"></div><figcaption><div class="mfp-bottom-bar"><div class="mfp-title"></div><div class="mfp-counter"></div></div></figcaption></figure></div>',cursor:"mfp-zoom-out-cur",titleSrc:"title",verticalFit:!0,tError:'<a href="%url%">The image</a> could not be loaded.'},proto:{initImage:function(){var e=t.st.image,n=".image";t.types.push("image"),x(f+n,function(){"image"===t.currItem.type&&e.cursor&&i.addClass(e.cursor)}),x(l+n,function(){e.cursor&&i.removeClass(e.cursor),I.off("resize"+v)}),x("Resize"+n,t.resizeImage),t.isLowIE&&x("AfterChange",t.resizeImage)},resizeImage:function(){var e=t.currItem;if(e&&e.img&&t.st.image.verticalFit){var n=0;t.isLowIE&&(n=parseInt(e.img.css("padding-top"),10)+parseInt(e.img.css("padding-bottom"),10)),e.img.css("max-height",t.wH-n)}},_onImageHasSize:function(e){e.img&&(e.hasSize=!0,j&&clearInterval(j),e.isCheckingImgSize=!1,T("ImageHasSize",e),e.imgHidden&&(t.content&&t.content.removeClass("mfp-loading"),e.imgHidden=!1))},findImageSize:function(e){var n=0,i=e.img[0],o=function(r){j&&clearInterval(j),j=setInterval(function(){return i.naturalWidth>0?(t._onImageHasSize(e),void 0):(n>200&&clearInterval(j),n++,3===n?o(10):40===n?o(50):100===n&&o(500),void 0)},r)};o(1)},getImage:function(n,i){var o=0,r=function(){n&&(n.img[0].complete?(n.img.off(".mfploader"),n===t.currItem&&(t._onImageHasSize(n),t.updateStatus("ready")),n.hasSize=!0,n.loaded=!0,T("ImageLoadComplete")):(o++,200>o?setTimeout(r,100):a()))},a=function(){n&&(n.img.off(".mfploader"),n===t.currItem&&(t._onImageHasSize(n),t.updateStatus("error",s.tError.replace("%url%",n.src))),n.hasSize=!0,n.loaded=!0,n.loadError=!0)},s=t.st.image,l=i.find(".mfp-img");if(l.length){var c=document.createElement("img");c.className="mfp-img",n.img=e(c).on("load.mfploader",r).on("error.mfploader",a),c.src=n.src,l.is("img")&&(n.img=n.img.clone()),n.img[0].naturalWidth>0&&(n.hasSize=!0)}return t._parseMarkup(i,{title:N(n),img_replaceWith:n.img},n),t.resizeImage(),n.hasSize?(j&&clearInterval(j),n.loadError?(i.addClass("mfp-loading"),t.updateStatus("error",s.tError.replace("%url%",n.src))):(i.removeClass("mfp-loading"),t.updateStatus("ready")),i):(t.updateStatus("loading"),n.loading=!0,n.hasSize||(n.imgHidden=!0,i.addClass("mfp-loading"),t.findImageSize(n)),i)}}});var W,R=function(){return void 0===W&&(W=void 0!==document.createElement("p").style.MozTransform),W};e.magnificPopup.registerModule("zoom",{options:{enabled:!1,easing:"ease-in-out",duration:300,opener:function(e){return e.is("img")?e:e.find("img")}},proto:{initZoom:function(){var e,n=t.st.zoom,i=".zoom";if(n.enabled&&t.supportsTransition){var o,r,a=n.duration,s=function(e){var t=e.clone().removeAttr("style").removeAttr("class").addClass("mfp-animated-image"),i="all "+n.duration/1e3+"s "+n.easing,o={position:"fixed",zIndex:9999,left:0,top:0,"-webkit-backface-visibility":"hidden"},r="transition";return o["-webkit-"+r]=o["-moz-"+r]=o["-o-"+r]=o[r]=i,t.css(o),t},d=function(){t.content.css("visibility","visible")};x("BuildControls"+i,function(){if(t._allowZoom()){if(clearTimeout(o),t.content.css("visibility","hidden"),e=t._getItemToZoom(),!e)return d(),void 0;r=s(e),r.css(t._getOffset()),t.wrap.append(r),o=setTimeout(function(){r.css(t._getOffset(!0)),o=setTimeout(function(){d(),setTimeout(function(){r.remove(),e=r=null,T("ZoomAnimationEnded")},16)},a)},16)}}),x(c+i,function(){if(t._allowZoom()){if(clearTimeout(o),t.st.removalDelay=a,!e){if(e=t._getItemToZoom(),!e)return;r=s(e)}r.css(t._getOffset(!0)),t.wrap.append(r),t.content.css("visibility","hidden"),setTimeout(function(){r.css(t._getOffset())},16)}}),x(l+i,function(){t._allowZoom()&&(d(),r&&r.remove(),e=null)})}},_allowZoom:function(){return"image"===t.currItem.type},_getItemToZoom:function(){return t.currItem.hasSize?t.currItem.img:!1},_getOffset:function(n){var i;i=n?t.currItem.img:t.st.zoom.opener(t.currItem.el||t.currItem);var o=i.offset(),r=parseInt(i.css("padding-top"),10),a=parseInt(i.css("padding-bottom"),10);o.top-=e(window).scrollTop()-r;var s={width:i.width(),height:(b?i.innerHeight():i[0].offsetHeight)-a-r};return R()?s["-moz-transform"]=s.transform="translate("+o.left+"px,"+o.top+"px)":(s.left=o.left,s.top=o.top),s}}});var Z="iframe",q="//about:blank",D=function(e){if(t.currTemplate[Z]){var n=t.currTemplate[Z].find("iframe");n.length&&(e||(n[0].src=q),t.isIE8&&n.css("display",e?"block":"none"))}};e.magnificPopup.registerModule(Z,{options:{markup:'<div class="mfp-iframe-scaler"><div class="mfp-close"></div><iframe class="mfp-iframe" src="//about:blank" frameborder="0" allowfullscreen></iframe></div>',srcAction:"iframe_src",patterns:{youtube:{index:"youtube.com",id:"v=",src:"//www.youtube.com/embed/%id%?autoplay=1"},vimeo:{index:"vimeo.com/",id:"/",src:"//player.vimeo.com/video/%id%?autoplay=1"},gmaps:{index:"//maps.google.",src:"%id%&output=embed"}}},proto:{initIframe:function(){t.types.push(Z),x("BeforeChange",function(e,t,n){t!==n&&(t===Z?D():n===Z&&D(!0))}),x(l+"."+Z,function(){D()})},getIframe:function(n,i){var o=n.src,r=t.st.iframe;e.each(r.patterns,function(){return o.indexOf(this.index)>-1?(this.id&&(o="string"==typeof this.id?o.substr(o.lastIndexOf(this.id)+this.id.length,o.length):this.id.call(this,o)),o=this.src.replace("%id%",o),!1):void 0});var a={};return r.srcAction&&(a[r.srcAction]=o),t._parseMarkup(i,a,n),t.updateStatus("ready"),i}}});var K=function(e){var n=t.items.length;return e>n-1?e-n:0>e?n+e:e},Y=function(e,t,n){return e.replace(/%curr%/gi,t+1).replace(/%total%/gi,n)};e.magnificPopup.registerModule("gallery",{options:{enabled:!1,arrowMarkup:'<button title="%title%" type="button" class="mfp-arrow mfp-arrow-%dir%"></button>',preload:[0,2],navigateByImgClick:!0,arrows:!0,tPrev:"Previous (Left arrow key)",tNext:"Next (Right arrow key)",tCounter:"%curr% of %total%"},proto:{initGallery:function(){var n=t.st.gallery,i=".mfp-gallery",r=Boolean(e.fn.mfpFastClick);return t.direction=!0,n&&n.enabled?(a+=" mfp-gallery",x(f+i,function(){n.navigateByImgClick&&t.wrap.on("click"+i,".mfp-img",function(){return t.items.length>1?(t.next(),!1):void 0}),o.on("keydown"+i,function(e){37===e.keyCode?t.prev():39===e.keyCode&&t.next()})}),x("UpdateStatus"+i,function(e,n){n.text&&(n.text=Y(n.text,t.currItem.index,t.items.length))}),x(p+i,function(e,i,o,r){var a=t.items.length;o.counter=a>1?Y(n.tCounter,r.index,a):""}),x("BuildControls"+i,function(){if(t.items.length>1&&n.arrows&&!t.arrowLeft){var i=n.arrowMarkup,o=t.arrowLeft=e(i.replace(/%title%/gi,n.tPrev).replace(/%dir%/gi,"left")).addClass(y),a=t.arrowRight=e(i.replace(/%title%/gi,n.tNext).replace(/%dir%/gi,"right")).addClass(y),s=r?"mfpFastClick":"click";o[s](function(){t.prev()}),a[s](function(){t.next()}),t.isIE7&&(k("b",o[0],!1,!0),k("a",o[0],!1,!0),k("b",a[0],!1,!0),k("a",a[0],!1,!0)),t.container.append(o.add(a))}}),x(m+i,function(){t._preloadTimeout&&clearTimeout(t._preloadTimeout),t._preloadTimeout=setTimeout(function(){t.preloadNearbyImages(),t._preloadTimeout=null},16)}),x(l+i,function(){o.off(i),t.wrap.off("click"+i),t.arrowLeft&&r&&t.arrowLeft.add(t.arrowRight).destroyMfpFastClick(),t.arrowRight=t.arrowLeft=null}),void 0):!1},next:function(){t.direction=!0,t.index=K(t.index+1),t.updateItemHTML()},prev:function(){t.direction=!1,t.index=K(t.index-1),t.updateItemHTML()},goTo:function(e){t.direction=e>=t.index,t.index=e,t.updateItemHTML()},preloadNearbyImages:function(){var e,n=t.st.gallery.preload,i=Math.min(n[0],t.items.length),o=Math.min(n[1],t.items.length);for(e=1;(t.direction?o:i)>=e;e++)t._preloadItem(t.index+e);for(e=1;(t.direction?i:o)>=e;e++)t._preloadItem(t.index-e)},_preloadItem:function(n){if(n=K(n),!t.items[n].preloaded){var i=t.items[n];i.parsed||(i=t.parseEl(n)),T("LazyLoad",i),"image"===i.type&&(i.img=e('<img class="mfp-img" />').on("load.mfploader",function(){i.hasSize=!0}).on("error.mfploader",function(){i.hasSize=!0,i.loadError=!0,T("LazyLoadError",i)}).attr("src",i.src)),i.preloaded=!0}}}});var U="retina";e.magnificPopup.registerModule(U,{options:{replaceSrc:function(e){return e.src.replace(/\.\w+$/,function(e){return"@2x"+e})},ratio:1},proto:{initRetina:function(){if(window.devicePixelRatio>1){var e=t.st.retina,n=e.ratio;n=isNaN(n)?n():n,n>1&&(x("ImageHasSize."+U,function(e,t){t.img.css({"max-width":t.img[0].naturalWidth/n,width:"100%"})}),x("ElementParse."+U,function(t,i){i.src=e.replaceSrc(i,n)}))}}}}),function(){var t=1e3,n="ontouchstart"in window,i=function(){I.off("touchmove"+r+" touchend"+r)},o="mfpFastClick",r="."+o;e.fn.mfpFastClick=function(o){return e(this).each(function(){var a,s=e(this);if(n){var l,c,d,u,p,f;s.on("touchstart"+r,function(e){u=!1,f=1,p=e.originalEvent?e.originalEvent.touches[0]:e.touches[0],c=p.clientX,d=p.clientY,I.on("touchmove"+r,function(e){p=e.originalEvent?e.originalEvent.touches:e.touches,f=p.length,p=p[0],(Math.abs(p.clientX-c)>10||Math.abs(p.clientY-d)>10)&&(u=!0,i())}).on("touchend"+r,function(e){i(),u||f>1||(a=!0,e.preventDefault(),clearTimeout(l),l=setTimeout(function(){a=!1},t),o())})})}s.on("click"+r,function(){a||o()})})},e.fn.destroyMfpFastClick=function(){e(this).off("touchstart"+r+" click"+r),n&&I.off("touchmove"+r+" touchend"+r)}}(),_()})(window.jQuery||window.Zepto);;/**
 * jQuery Nested v1.03
 *
 * For a (total) gap free, multi column, grid layout experience.
 * http://suprb.com/apps/nested/
 * By Andreas Pihlström and additional brain activity by Jonas Blomdin
 *
 * Licensed under the MIT license.
 */

// Debouncing function from John Hann
// http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
// Copy pasted from http://paulirish.com/2009/throttled-smartresize-jquery-event-handler/

(function ($, sr) {
    var debounce = function (func, threshold, execAsap) {
        var timeout;
        return function debounced() {
            var obj = this,
                args = arguments;

            function delayed() {
                if (!execAsap) func.apply(obj, args);
                timeout = null;
            };
            if (timeout) clearTimeout(timeout);
            else if (execAsap) func.apply(obj, args);

            timeout = setTimeout(delayed, threshold || 150);
        };
    };
    jQuery.fn[sr] = function (fn) {
        return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr);
    };

})(jQuery, 'smartresize');

// Simple count object properties

if (!Object.keys) {
    Object.keys = function (obj) {
        var keys = [],
            k;
        for (k in obj) {
            if (Object.prototype.hasOwnProperty.call(obj, k)) {
                keys.push(k);
            }
        }
        return keys;
    };
}

// The Nested magic

(function ($) {

    $.Nested = function (options, element) {
        this.element = $(element);
        this._init(options);
    };

    $.Nested.settings = {
        selector: '.box',
        minWidth: 50,
        minColumns: 1,
        gutter: 1,
        centered: false,
        resizeToFit: true, // will resize block bigger than the gap
        resizeToFitOptions: {
            resizeAny: true // will resize any block to fit the gap         
        },
        animate: true,
        animationOptions: {
            speed: 20,
            duration: 100,
            queue: true,
            complete: function () {}
        }
    };

    $.Nested.prototype = {

        _init: function (options) {
            var container = this;
            this.box = this.element;
            $(this.box).css('position', 'relative');
            this.options = $.extend(true, {}, $.Nested.settings, options);
            this.elements = [];
            this._isResizing = false;
            this._update = true;
            this.maxy = new Array();

            // add smartresize
            $(window).smartresize(function () {
                container.resize();
            });

            // build box dimensions
            this._setBoxes();
        },

        _setBoxes: function ($els, method) {
            var self = this;
            this.idCounter = 0;
            this.counter = 0;
            this.t = 0;
            this.maxHeight = 0;
            this.currWidth = 0;
            this.total = this.box.find(this.options.selector);
            this.matrix = {};
            this.gridrow = new Object;

            var calcWidth = !this.options.centered ? this.box.innerWidth() : $(window).width();

            this.columns = Math.max(this.options.minColumns, parseInt(calcWidth / (this.options.minWidth + this.options.gutter)) + 1);

            // build columns
            var minWidth = this.options.minWidth;
            var gutter = this.options.gutter;
            var display = "block";

            $els = this.box.find(this.options.selector);

            $.each($els, function () {

                var dim = parseInt($(this).attr('class').replace(/^.*size([0-9]+).*$/, '$1')).toString().split('');
                var x = (dim[0] == "N") ? 1 : parseFloat(dim[0]);
                var y = (dim[1] == "a") ? 1 : parseFloat(dim[1]);

                var currWidth = minWidth * x + gutter * (x - 1);
                var currHeight = minWidth * y + gutter * (y - 1);

                $(this).css({
                    'display': display,
                    'position': 'absolute',
                    'width': currWidth,
                    'height': currHeight,
                    'top': $(this).position().top,
                    'left': $(this).position().left
                }).removeClass('nested-moved').attr('data-box', self.idCounter).attr('data-width', currWidth);

                self.idCounter++;

                // render grid
                self._renderGrid($(this), method);

            });

            // position grid
            if (self.counter == self.total.length) {

                // if option resizeToFit is true
                if (self.options.resizeToFit) {
                    self.elements = self._fillGaps();
                }
                self._renderItems(self.elements);
                // reset elements
                self.elements = [];
            }
        },

        _addMatrixRow: function (y) {
            if (this.matrix[y]) {
                return false;
            } else this.matrix[y] = {};

            for (var c = 0; c < (this.columns - 1); c++) {
                var x = c * (this.options.minWidth + this.options.gutter);
                this.matrix[y][x] = 'false';
            }
        },

        _updateMatrix: function (el) {
            var height = 0;
            var t = parseInt(el['y']);
            var l = parseInt(el['x']);
            for (var h = 0; h < el['height']; h += (this.options.minWidth + this.options.gutter)) {
                for (var w = 0; w < el['width']; w += (this.options.minWidth + this.options.gutter)) {
                    var x = l + w;
                    var y = t + h;
                    if (!this.matrix[y]) {
                        this._addMatrixRow(y);
                    }
                    this.matrix[y][x] = 'true';
                }
            }
        },

        _getObjectSize: function (obj) { // Helper to get size of object, should probably be moved
            var size = 0;
            $.each(obj, function (p, v) {
                size++;
            });
            return size;
        },


        _fillGaps: function () {
            var self = this;
            var box = {};

            $.each(this.elements, function (index, el) {
                self._updateMatrix(el);
            });

            var arr = this.elements;
            arr.sort(function (a, b) {
                return a.y - b.y;
            });
            arr.reverse();

            // Used to keep the highest y value for a box in memory
            var topY = arr[0]['y'];

            // Used for current y with added offset
            var actualY = 0;

            // Current number of rows in matrix
            var rowsLeft = this._getObjectSize(this.matrix);

            $.each(this.matrix, function (y, row) {
                rowsLeft--;
                actualY = parseInt(y); // + parseInt(self.box.offset().top);
                $.each(row, function (x, col) {

                    if (col === 'false' && actualY < topY) {
                        if (!box.y) box.y = y;
                        if (!box.x) box.x = x;
                        if (!box.w) box.w = 0;
                        if (!box.h) box.h = self.options.minWidth;
                        box.w += (box.w) ? (self.options.minWidth + self.options.gutter) : self.options.minWidth;

                        var addonHeight = 0;
                        for (var row = 1; row < rowsLeft; row++) {
                            var z = parseInt(y) + parseInt(row * (self.options.minWidth + self.options.gutter));
                            if (self.matrix[z] && self.matrix[z][x] == 'false') {
                                addonHeight += (self.options.minWidth + self.options.gutter);
                                self.matrix[z][x] = 'true';
                            } else break;
                        }

                        box.h + (parseInt(addonHeight) / (self.options.minWidth + self.options.gutter) == rowsLeft) ? 0 : parseInt(addonHeight);
                        box.ready = true;

                    } else if (box.ready) {

                        $.each(arr, function (i, el) {
                            if (box.y <= arr[i]['y'] && (self.options.resizeToFitOptions.resizeAny || box.w <= arr[i]['width'] && box.h <= arr[i]['height'])) {
                                arr.splice(i, 1);
                                $(el['$el']).addClass('nested-moved');
                                self.elements.push({
                                    $el: $(el['$el']),
                                    x: parseInt(box.x),
                                    y: parseInt(box.y),
                                    col: i,
                                    width: parseInt(box.w),
                                    height: parseInt(box.h)
                                });

                                return false;
                            }
                        });
                        box = {};
                    }
                });

            });

            self.elements = arr;
            return self.elements;

        },

        _renderGrid: function ($box, method) {

            this.counter++;
            var ypos, gridy = ypos = 0;
            var tot = 0;
            var direction = !method ? "append" : "prepend";

            // Width & height
            var width = $box.width();
            var height = $box.height();

            // Calculate row and col
            var col = Math.ceil(width / (this.options.minWidth + this.options.gutter));
            var row = Math.ceil(height / (this.options.minWidth + this.options.gutter));

            // lock widest box to match minColumns
            if (col > this.options.minColumns) {
                this.options.minColumns = col;
            }

            while (true) {

                for (var y = col; y >= 0; y--) {
                    if (this.gridrow[gridy + y]) break;
                    this.gridrow[gridy + y] = new Object;
                    for (var x = 0; x < this.columns; x++) {
                        this.gridrow[gridy + y][x] = false;
                    }
                }

                for (var column = 0; column < (this.columns - col); column++) {

                    // Add default empty matrix, used to calculate and update matrix for each box
                    matrixY = gridy * (this.options.minWidth + this.options.gutter);
                    this._addMatrixRow(matrixY);

                    var fits = true;

                    for (var y = 0; y < row; y++) {
                        for (var x = 0; x < col; x++) {

                            if (!this.gridrow[gridy + y]) {
                                break;
                            }

                            if (this.gridrow[gridy + y][column + x]) {
                                fits = false;
                                break;
                            }
                        }
                        if (!fits) {
                            break;
                        }
                    }
                    if (fits) {
                        // Set as taken
                        for (var y = 0; y < row; y++) {
                            for (var x = 0; x < col; x++) {

                                if (!this.gridrow[gridy + y]) {
                                    break;
                                }
                                this.gridrow[gridy + y][column + x] = true;
                            }
                        }

                        // Push to elements array
                        this._pushItem($box, column * (this.options.minWidth + this.options.gutter), gridy * (this.options.minWidth + this.options.gutter), width, height, col, row, direction);
                        return;
                    }
                }
                gridy++;
            }
        },

        _pushItem: function ($el, x, y, w, h, cols, rows, method) {

            if (method == "prepend") {
                this.elements.unshift({
                    $el: $el,
                    x: x,
                    y: y,
                    width: w,
                    height: h,
                    cols: cols,
                    rows: rows
                });
            } else {
                this.elements.push({
                    $el: $el,
                    x: x,
                    y: y,
                    width: w,
                    height: h,
                    cols: cols,
                    rows: rows
                });
            }
        },

        _setHeight: function ($els) {
            var self = this;
            $.each($els, function (index, value) {
                // set maxHeight
                var colY = (value['y'] + value['height']);
                if (colY > self.maxHeight) {
                    self.maxHeight = colY;
                }
            });
            return self.maxHeight;
        },

        _setWidth: function ($els) {
            var self = this;
            $.each($els, function (index, value) {
                // set maxWidth
                var colX = (value['x'] + value['width']);
                if (colX > self.currWidth) {
                    self.currWidth = colX;
                }
            });
            return self.currWidth;
        },

        _renderItems: function ($els) {
            var self = this;

            // set container height and width
            this.box.css('height', this._setHeight($els));
            if (this.options.centered) {
                this.box.css({'width' : this._setWidth($els), 'margin-left' : 'auto', 'margin-right' : 'auto'});
            }

            $els.reverse();
            var speed = this.options.animationOptions.speed;
            var effect = this.options.animationOptions.effect;
            var duration = this.options.animationOptions.duration;
            var queue = this.options.animationOptions.queue;
            var animate = this.options.animate;
            var complete = this.options.animationOptions.complete;
            var item = this;
            var i = 0;
            var t = 0;

            $.each($els, function (index, value) {

                $currLeft = $(value['$el']).position().left;
                $currTop = $(value['$el']).position().top;
                $currWidth = $(value['$el']).width();
                $currHeight = $(value['$el']).width();

                value['$el'].attr('data-y', $currTop).attr('data-x', $currLeft);
                
                //if animate and queue
                if (animate && queue && ($currLeft != value['x'] || $currTop != value['y'])) {
                    setTimeout(function () {
                        value['$el'].css({
                            'display': 'block',
                            'width': value['width'],
                            'height': value['height']
                        }).animate({
                            'left': value['x'],
                            'top': value['y']
                        }, duration);
                        t++;
                        if (t == i) {
                            complete.call(undefined, $els)
                        }
                    }, i * speed);
                    i++;
                }

                //if animate and no queue
                if (animate && !queue && ($currLeft != value['x'] || $currTop != value['y'])) {
                    setTimeout(function () {
                        value['$el'].css({
                            'display': 'block',
                            'width': value['width'],
                            'height': value['height']
                        }).animate({
                            'left': value['x'],
                            'top': value['y']
                        }, duration);
                        t++;
                        if (t == i) {
                            complete.call(undefined, $els)
                        }
                    }, i);
                    i++;
                }

                //if no animation and no queue
                if (!animate && ($currLeft != value['x'] || $currTop != value['y'])) {
                    value['$el'].css({
                        'display': 'block',
                        'width': value['width'],
                        'height': value['height'],
                        'left': value['x'],
                        'top': value['y']
                    });
                    t++;
                    if (t == i) {
                        complete.call(undefined, $els)
                    }
                }
            });
            if (i == 0) {
                complete.call(undefined, $els)
            }
        },

        append: function ($els) {
            this._isResizing = true;
            this._setBoxes($els, 'append');
            this._isResizing = false;
        },

        prepend: function ($els) {
            this._isResizing = true;
            this._setBoxes($els, 'prepend');
            this._isResizing = false;
        },

        resize: function ($els) {
            if (Object.keys(this.matrix[0]).length % Math.floor(this.element.width() / (this.options.minWidth + this.options.gutter)) > 0) {
                this._isResizing = true;
                this._setBoxes(this.box.find(this.options.selector));
                this._isResizing = false;
            }
        },
      
        refresh: function(options) {
        	
        	options = options || this.options;
        
            this.options = $.extend(true, {}, $.Nested.settings, options);
            this.elements = [];
            this._isResizing = false;

            // build box dimensions
            this._setBoxes();
        },
        
        destroy: function() {
			
			var container = this;

            $(window).unbind("resize", function () {
                container.resize();
            });
	        
	        // unbind the resize event
            $els = this.box.find(this.options.selector);
            $($els).removeClass('nested-moved').removeAttr('style data-box data-width data-x data-y').removeData();
            
            this.box.removeAttr("style").removeData();
        }
        
    }


	var methods =
	{
		refresh: function(options) {
			return this.each(function(){
				var $this=$(this);
				var nested = $this.data('nested');
				
				nested.refresh(options);
			});
		},
		
		destroy: function() {
			return this.each(function(){
				var $this=$(this);
				var nested = $this.data('nested');
				
				nested.destroy();
			});
		}
	};
	
	

    $.fn.nested = function (options, e) {

		if(methods[options]) {
			return methods[options].apply(this, Array.prototype.slice.call(arguments, 1));
		}        
		
		if (typeof options === 'string') {
            this.each(function () {
                var container = $.data(this, 'nested');
                container[options].apply(container, [e]);
            });
        } else {
            this.each(function () {
                $.data(this, 'nested', new $.Nested(options, this));
            });
        }
        return this;
    }

})(jQuery);
;/* ========================================================================
 * bootstrap3-confirmation.js v1.0.1
 * Adaptation of bootstrap-confirmation.js 
 * from Nimit Suwannagate <ethaizone@hotmail.com>
 * http://ethaizone.github.io/Bootstrap-Confirmation/
 * ========================================================================
 * Copyright 2013 Thomas Jacquart <thomas.jacquart@gmail.com>.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ======================================================================== */


+function ($) { "use strict";

  // COMFIRMATION PUBLIC CLASS DEFINITION
  // ====================================
  var Confirmation = function (element, options) {
    // First init from popover
    this.init('confirmation', element, options)
    
    var options = this.options
    
    if (options.singleton) {
      // remove others when I show me
    }
    var that = this;
    if (options.popout) {
      // close when I click outside the box
      var $tip = this.tip()
//      $('html').on('click', function(){
//	  that.leave(that)
//      })
    }
  }

  if (!$.fn.popover || !$.fn.tooltip) throw new Error('Confirmation requires popover.js and tooltip.js')

  Confirmation.DEFAULTS = $.extend({} , $.fn.popover.Constructor.DEFAULTS, {
    placement	    : 'top'
    , title	    : 'Are you sure ?'
    , btnOkClass    : 'btn btn-primary btn-sm'
    , btnOkLabel    : 'Yes'
    , btnOkIcon	    : 'glyphicon glyphicon-ok' 
    , btnCancelClass: 'btn btn-default btn-sm'
    , btnCancelLabel: 'No'
    , btnCancelIcon : 'glyphicon glyphicon-remove' 
    , singleton	    : false
    , popout	    : false
    , href	    : '#'
    , target	    : '_self'
    , onConfirm	    : function(){}
    , onCancel	    : function(){}
    , template	    :   '<div class="popover">'
		      + '<div class="arrow"></div>'
		      + '<h3 class="popover-title"></h3>'
		      + '<div class="popover-content">'
		      + '<a data-apply="confirmation">Yes</a>'
		      + ' <a data-dismiss="confirmation">No</a>'
		      + '</div>'
		      + '</div>'
  })


  // NOTE: CONFIRMATION EXTENDS popover.js
  // ================================

  Confirmation.prototype = $.extend({}, $.fn.popover.Constructor.prototype)

  Confirmation.prototype.constructor = Confirmation

  Confirmation.prototype.getDefaults = function () {
    return Confirmation.DEFAULTS
  }
  
  Confirmation.prototype.setContent = function () {
    var that	    = this;
    var $tip	    = this.tip()
    var title	    = this.getTitle()
    var $btnOk	    = $tip.find('[data-apply="confirmation"]');
    var $btnCancel  = $tip.find('[data-dismiss="confirmation"]');
    var options	    = that.options
    
    $btnOk.addClass(this.getBtnOkClass())
      .html(this.getBtnOkLabel())
      .prepend($('<i></i>').addClass(this.getBtnOkIcon()), " ")
      .attr('href', this.getHref())
      .attr('target', this.getTarget())
      .one('click', function() {
        options.onConfirm()
        that.leave(that)
	  })
    
    $btnCancel.addClass(this.getBtnCancelClass())
	      .html(this.getBtnCancelLabel())
	      .prepend($('<i></i>').addClass(this.getBtnCancelIcon()), " ")      
	      .one('click', function(){
          options.onCancel()
          that.leave(that)
	      })
    
    $tip.find('.popover-title')[this.options.html ? 'html' : 'text'](title)

    $tip.removeClass('fade top bottom left right in')

    // IE8 doesn't accept hiding via the `:empty` pseudo selector, we have to do
    // this manually by checking the contents.
    if (!$tip.find('.popover-title').html()) $tip.find('.popover-title').hide()
  }

  Confirmation.prototype.getBtnOkClass = function () {
    var $e = this.$element
    var o  = this.options

    return $e.attr('data-btnOkClass')
      || (typeof o.btnOkClass == 'function' ? 
	    o.btnOkClass.call($e[0]) : 
	    o.btnOkClass)
  }
  
  Confirmation.prototype.getBtnOkLabel = function () {
    var $e = this.$element
    var o  = this.options

    return $e.attr('data-btnOkLabel')
      || (typeof o.btnOkLabel == 'function' ?
            o.btnOkLabel.call($e[0]) :
            o.btnOkLabel)
  }
  
  Confirmation.prototype.getBtnOkIcon = function () {
    var $e = this.$element
    var o  = this.options

    return $e.attr('data-btnOkIcon')
      || (typeof o.btnOkIcon == 'function' ?
            o.btnOkIcon.call($e[0]) :
            o.btnOkIcon)
  }

  Confirmation.prototype.getBtnCancelClass = function () {
    var $e = this.$element
    var o  = this.options

    return $e.attr('data-btnCancelClass')
      || (typeof o.btnCancelClass == 'function' ? 
	    o.btnCancelClass.call($e[0]) : 
	    o.btnCancelClass)
  }
  
  Confirmation.prototype.getBtnCancelLabel = function () {
    var $e = this.$element
    var o  = this.options

    return $e.attr('data-btnCancelLabel')
      || (typeof o.btnCancelLabel == 'function' ?
            o.btnCancelLabel.call($e[0]) :
            o.btnCancelLabel)
  }
  
  Confirmation.prototype.getBtnCancelIcon = function () {
    var $e = this.$element
    var o  = this.options

    return $e.attr('data-btnCancelIcon')
      || (typeof o.btnCancelIcon == 'function' ?
            o.btnCancelIcon.call($e[0]) :
            o.btnCancelIcon)
  }
  
  Confirmation.prototype.getHref = function () {
    var $e = this.$element
    var o  = this.options

    return $e.attr('data-href')
      || (typeof o.href == 'function' ?
            o.href.call($e[0]) :
            o.href)
  }

  Confirmation.prototype.getTarget = function () {
    var $e = this.$element
    var o  = this.options

    return $e.attr('data-target')
      || (typeof o.target == 'function' ?
            o.target.call($e[0]) :
            o.target)
  }

  // CONFIRMATION PLUGIN DEFINITION
  // ==============================

  var old = $.fn.confirmation

  $.fn.confirmation = function (option) {
    var that = this
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.confirmation')
      var options = typeof option == 'object' && option

      if (!data) $this.data('bs.confirmation', (data = new Confirmation(this, options)))
      if (typeof option == 'string') data[option]()
    })
  }

  $.fn.confirmation.Constructor = Confirmation


  // CONFIRMATION NO CONFLICT
  // ===================

  $.fn.confirmation.noConflict = function () {
    $.fn.confirmation = old
    return this
  }

}(jQuery);
;/**
 * jQuery Unveil
 * A very lightweight jQuery plugin to lazy load images
 * http://luis-almeida.github.com/unveil
 *
 * Licensed under the MIT license.
 * Copyright 2013 Luís Almeida
 * https://github.com/luis-almeida
 */

;(function($) {

  $.fn.unveil = function(threshold, callback) {

    var $w = $(window),
        th = threshold || 0,
        retina = window.devicePixelRatio > 1,
        attrib = retina? "data-src-retina" : "data-src",
        images = this,
        loaded;

    this.one("unveil", function() {
      var source = this.getAttribute(attrib);
      source = source || this.getAttribute("data-src");
      if (source) {
        this.setAttribute("src", source);
        if (typeof callback === "function") callback.call(this);
      }
    });

    function unveil() {
      var inview = images.filter(function() {
        var $e = $(this);
        if ($e.is(":hidden")) return;

        var wt = $w.scrollTop(),
            wb = wt + $w.height(),
            et = $e.offset().top,
            eb = et + $e.height();

        return eb >= wt - th && et <= wb + th;
      });

      loaded = inview.trigger("unveil");
      images = images.not(loaded);
    }

    $w.scroll(unveil);
    $w.resize(unveil);

    unveil();

    return this;

  };

})(window.jQuery || window.Zepto);
;(function($) {


$(document).ready(function(){

    var panelVisible;

    // Variables

    var
    $body                = $('body'),
    $window              = $(window),
    $textarea            = $("textarea"),
    $articleInputBody    = $(".article-input-body"),
    $articleInputTitle   = $(".article-input-title"),
    $editForm            = $(".edit-article-form"),
    $createForm          = $(".new-article-form"),
    $editingTools        = $(".editing-tools"),
    $updateArticleButton = $(".update-button"),
    $createArticleButton = $(".create-button"),
    $miniIcons           = $(".mini-icon"),
    $articleBody         = $(".article-main").find(".article-body"),
    $articleList         = $(".article-list"),
    $indexWrapper        = $(".index-wrapper"),
    $editingButtons      = $(".editing-button"),
    $gallery             = $(".gallery-wrapper"),
    $lamp                = $(".lamp-button"),
    $imageLinks          = $(".show-img"),
    $adminPanel          = $(".admin-panel"),
    $adminToggle         = $adminPanel.find(".admin-subrosa a"),
    // base thumbnail size for gallery
    thumbSize            = 200,
    // variable referring to whether editing window is darkened
    dark                 = false,
    // variables referring to color of input fields in article edit
    articleTitleLight    = "#191919",
    articleBodyLight     = "#666",
    articleTitleDark     = "#b7b7b7",
    articleBodyDark      = "#848383",
    adminPanelVisible    = true,
    wWidth               = null,
    wHeight              = null,
    fadeoutIntVal        = null,
    fadeout              = false,
    // width of window where most responsive events are occuring
    majorBreakpoint      = 740,
    adminPanelWidthSmall = 240,
    tocTemplate = "\
      <div class='toc'>\
        <div class='toc-header'><h3>Table of Contents</h3></div>\
        <ul class='toc-body list-unstyled'>\
        </ul>\
      </div>"


    // initialization function
    // =======================


    function init(){

        wWidth  = $window.width();
        wHeight = $window.height();

        panelVisible = getToggleState();
        if (panelVisible == null){
            panelVisible = 1;
        };

        if (panelVisible == 0){

            $adminPanel.find('.hideable')
            .hide()
            .end()
            .css('width', '20px').show()
        } else {
            $adminPanel.show()
        }

        $updateArticleButton.click(function(e){
            e.preventDefault();
            $editForm.submit();
        });

        matchIndexContents();

        $createArticleButton.click(function(e){
            e.preventDefault();
            $createForm.submit();
        });
        $articleBody.createToC();
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

        positionFooter();


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
        $("a, button").one("click", function() {
            $(this).click(function () { return false; });
        });

    };

    //functions to be initialised when window has loaded

    function start(){

        processGalleryImages($gallery);
        $textarea.autogrow();
        $miniIcons.tooltip();
        $editingButtons.tooltip();
        $articleInputBody.focusin(function(){;
            fadeout = true;
            checkFadeout()
        }
        ).focusout(function(){
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
        $('.cheatsheet-button').magnificPopup({
            midClick: true,
            type: 'inline'
        });
        $adminToggle.click(function(e){
            e.preventDefault();
            toggleAdminPanel();
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

    };

    function getToggleState(){
        return localStorage.getItem('adminPanelVisible')
    };

    function setToggleState(state){
        localStorage.setItem('adminPanelVisible', state)

    };

    function matchIndexContents(){
        if(wWidth > majorBreakpoint){
            if($articleList.height() > $indexWrapper.height()){
                $indexWrapper.height($articleList.height());
            };
        }

    };

    // ========================================

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


     function positionFooter(){
        // Sticky footer code
        if($(document.body).height() < $(window).height()){
            $('#footer').css({
                position: 'absolute',
                top:  ( $(window).scrollTop() + $(window).height()
                  - $("#footer").height() ) + "px",
                width: "100%"
            });
        } else {
            $('#footer').css({
                position: 'relative'
            });
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


    function toggleAdminPanel(){

        if  (wWidth > majorBreakpoint){
            panelVisible = getToggleState();

            if (panelVisible === null){
                panelVisible = 1
            };

            if (panelVisible == 1){
                $adminPanel
                .find('.hideable')
                .stop()
                .hide()
                .end()
                .delay(200)
                .css('width', 20);
                setToggleState(0);
            } else {
                $adminPanel
                .stop()
                .css('width', adminPanelWidthSmall)
                .find('.hideable')
                .delay(100)
                .show()
                setToggleState(1);
            }

        }
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

// ================================================================================

init();

$window.load(function(){
    start();
});

$window.bind('resize scroll', function(){
    positionFooter();
});

$window.resize(function(){
    wHeight = $window.height();
    wWidth = $window.width();
    console.log(wWidth);
    matchIndexContents();
    if(wWidth < majorBreakpoint){
        $adminPanel.removeAttr('style').show().find('.hideable').show();
        setToggleState(1);
    }

});

$window.scroll(positionFooter);

});



})(jQuery);



