$(function () {
    // 1. for dropdown menu with easyui-menu
    $('li.dropdown-submenu').on('click', function(){
        var left = $(this).offset().left
            ,top = 50
            ,target = $(this).attr('_target');
        if(!target) return;
        $('#'+target).menu('show', {left: left, top: top, hideOnUnhover: true});
    });

    // 1. extend jquery gen urlparm form location
    jQuery.gen_urlparam = function (url, params){
        var queries = [];
        $.each(params, function (k, v) {
            queries.push(k+'='+v)
        });
        if(queries.length == 0){
            return url;
        }
        return url+'?'+queries.join('&');
    };

    // 1. extend jquery get urlparm form location
    jQuery.get_urlparam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return decodeURI(r[2]); return null;
    };

    // 1. extend array for sum/cur/min/max/avg
    Array.prototype.remove = function(val) {
        var index = this.indexOf(val);
        if (index > -1) {
            this.splice(index, 1);
        }
    };
    Array.prototype.cur = function () {
        return this[this.length-1];
    };
    Array.prototype.max = function() {
        return Math.max.apply({}, this)
    };
    Array.prototype.min = function() {
        return Math.min.apply({}, this)
    };
    Array.prototype.sum = function () {
        return this.reduce(function(previousValue, currentValue, index, array){
            return previousValue + currentValue;
        });
    };
    Array.prototype.avg = function () {
        return parseInt(this.sum()/this.length);
    }
});