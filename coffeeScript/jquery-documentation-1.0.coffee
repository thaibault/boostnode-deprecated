## standalone

# region modline

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

# region header

# Copyright Torben Sickert 16.12.2012

# License
#    This library written by Torben Sickert stand under a creative commons
#    naming 3.0 unported license.
#    see http://creativecommons.org/licenses/by/3.0/deed.de

###!
    jQuery plugin for "jquery-1.9.1".

    Copyright see require on https://github.com/thaibault/require

    Conventions see require on https://github.com/thaibault/require

    @author t.sickert@gmail.com (Torben Sickert)
    @version 1.0 stable
    @fileOverview
    This module provides common reusable logic a simple project documentation
    web page.
###

###*
    @name jQuery
    @see www.jquery.com
###
## require
## this.window.require([
##     ['jQuery.Website', 'jquery-website-1.0.coffee'],
##     ['jQuery.fn.carousel', 'bootstrap-2.3.1']],
## (jQuery) ->
((jQuery) ->
##

# endregion

# region plugins

    ###*
        @memberOf jQuery
        @class
    ###
    class Documentation extends jQuery.Website.class

    # region private properties

        __name__: 'Documentation'

    # endregion

    # region protected properties 

        ###*
            Saves default options for manipulating the default behaviour.

            @property {Object}
        ###
        _options:
            domNodeSelectorPrefix: 'body.{1}'
            domNodes:
                tableOfContentLinks: 'div.toc a[href^="#"]'
                imprintLink: 'a[href="#imprint"]'
                imprintContent: 'section.imprint'
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
            this._domNodes.imprintContent.hide()
            this.on this._domNodes.tableOfContentLinks, 'click', ->
                jQuery.scrollTo jQuery(this).attr('href'), 'slow'
            this.on this._domNodes.imprintLink, 'click', =>
                this._domNodes.mainContent.fadeOut 'slow', =>
                    this._domNodes.imprintContent.fadeIn 'slow'

        # endregion

    # endregion

    ###* @ignore ###
    jQuery.Documentation = ->
        self = new Documentation
        self._controller.apply self, arguments
    ###* @ignore ###
    jQuery.Documentation.class = Documentation

# endregion

## require )
).call this, this.jQuery
