## require

# region header

# Copyright Torben Sickert 16.12.2012

# License
#    This library written by Torben Sickert stand under a creative commons
#    naming 3.0 unported license.
#    see http://creativecommons.org/licenses/by/3.0/deed.de

# vim: set tabstop=4 shiftwidth=4 expandtab:
# vim: foldmethod=marker foldmarker=region,endregion:

# endregion

## standalone
## this.jQuery.noConflict(true) (jQuery) ->
##     jQuery.Documentation window.OPTIONS
this.require.noConflict = true
this.require.asyncronModulePatternHandling =
    '^.+\.coffee$': (coffeeScriptCode, module) =>
        module = if module[0] then module[0] else module[1]
        this.console.log "Run coffee script module \"#{module}\"."
        try
            this.CoffeeScript.run coffeeScriptCode
        catch exception
            this.console.log this.CoffeeScript.compile coffeeScriptCode
            throw exception
this.require(
    [['jQuery.Documentation', 'jquery-documentation-1.0.coffee']],
(jQuery) ->
    ###
        Embedd jQuery and require full compatible to all other
        JavaScripts.
        The global scope is clean after this sequence. The given
        function is called when the dom-tree was loaded.
    ###
    # Production mode:
    # jQuery.noConflict(true) (jQuery) -> jQuery.Documentation window.OPTIONS
    jQuery (jQuery) -> jQuery.Documentation window.OPTIONS)
##
