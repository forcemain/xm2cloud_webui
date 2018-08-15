Array.prototype.clean = function(deleteValue) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == deleteValue) {
            this.splice(i, 1);
            i--;
        }
    }
    return this;
};

String.prototype.startswith = function (prefix){
    return this.slice(0, prefix.length) === prefix;
};

String.prototype.len = function (){
    var real_len = 0, len = this.length, char_code = -1;
    for (var i = 0; i < len; i++) {
        char_code = this.charCodeAt(i);
        if (char_code >= 0 && char_code <= 128){
            real_len += 1;
        }else{
            real_len += 2;
        }
    }
    return real_len;
};

String.prototype.cut = function (len){
    var str_len = 0
        ,real_len = 0
        ,str_cut = new String()
        ,str_len = this.length;
    for (var i = 0; i < str_len; i++) {
        a = this.charAt(i);
        real_len++;
        if (escape(a).length > 4) {
            //中文字符的长度经编码之后大于4
            real_len++;
        }
        str_cut = str_cut.concat(a);
        if (real_len >= len) {
            str_cut = str_cut.concat("...");
            return str_cut;
        }
    }
    if (real_len < len) {
        return this;
    }
};

function exit_fullscreen() {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    }
    else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
    }
    else if (document.webkitCancelFullScreen) {
        document.webkitCancelFullScreen();
    }
    else if (document.msExitFullscreen) {
        document.msExitFullscreen();
    }
}

function enter_fullscreen(p) {
    var docElm = document.getElementById(p) || document.documentElement;
    //W3C
    if (docElm.requestFullscreen) {
        docElm.requestFullscreen();
    }
    //FireFox
    else if (docElm.mozRequestFullScreen) {
        docElm.mozRequestFullScreen();
    }
    //Chrome
    else if (docElm.webkitRequestFullScreen) {
        docElm.webkitRequestFullScreen();
    }
    //IE11
    else if (elem.msRequestFullscreen) {
        elem.msRequestFullscreen();
    }
}
