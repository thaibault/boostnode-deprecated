## require

# region header

# Copyright Torben Sickert 16.12.2012

# License
#    This library written by Torben Sickert stand under a creative commons
#    naming 3.0 unported license.
#    see http://creativecommons.org/licenses/by/3.0/deed.de

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

###!
    jQuery plugin for "jquery-1.9.1".

    Copyright see require on https://github.com/thaibault/require

    Conventions see require on https://github.com/thaibault/require

    @author t.sickert@gmail.com (Torben Sickert)
    @version 1.0 stable
    @fileOverview
    This module provides common resuable logic a simple project documentation
    webpage.
###

###*
    @name jQuery
    @see www.jquery.com
###
## standalone
## ((jQuery) ->
this.window.require([
    ['less', 'less-1.3.3'],

    ['jQuery.Tools', 'jquery-tools-1.0.coffee'],

    ['jQuery.fn.carousel', 'bootstrap-2.3.1'],

    ['jQuery.scrollTo', 'jquery-scrollTo-1.4.3.1']],
(less, jQuery) ->
##

# endregion

# region plugins

    ###*
        @memberOf jQuery
        @class
    ###
    class Documentation extends jQuery.Tools.class

    # region private properties

        __name__: 'Documentation'
        __googleAnalyticsCode: "
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
ga('create', '{1}', 'github.io');ga('send', 'pageview');"

    # endregion

    # region protected properties 

        ###*
            Saves default options for manipulating the default behaviour.

            @property {Object}
        ###
        _options:
            logging: false
            domNodeSelectorPrefix: 'body.documentation'
            domNodes:
                tableOfContentLinks: 'div.toc a[href^="#"]'
                imprintLink: 'a[href="#imprint"]'
                imprintContent: 'section#imprint'
                mainContent: 'section#main_content'
            trackingCode: 'UA-0-0'
        ###*
            Holds all needed dom nodes.

            @property {Object}
        ###
        _domNodes: {}

    # endregion

    # region public methods

        # region special methods

        ###*
            @description Initializes the interactive web app.

            @param {Object} options An options object.

            @returns {jQuery.Tools} Returns the current instance.
        ###
        initialize: (options) ->
            super options
            this._domNodes = this.grapDomNodes this._options.domNodes
            this.on this._domNodes.tableOfContentLinks, 'click', ->
                jQuery.scrollTo jQuery(this).attr('href'), 'slow'
            this.on this._domNodes.imprintLink, 'click', =>
                this._domNodes.mainContent.fadeOut 'slow', =>
                    this._domNodes.imprintContent.fadeIn 'slow'
            this._handleGooleAnalytics(this._options.trackingCode)

        # endregion

    # endregion

    # region protected methods

        _handleGooleAnalytics: (trackingCode) ->
            window.eval this.stringFormat(
                this.__googleAnalyticsCode, trackingCode)
            this

    # endregion

    ###* @ignore ###
    jQuery.Documentation = ->
        self = new Documentation
        self._controller.apply self, arguments

# endregion

## standalone ).call this, this.jQuery
)
